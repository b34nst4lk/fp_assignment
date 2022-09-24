import logging
from datetime import datetime
from typing import List

from google.cloud.bigquery import (
    QueryJobConfig,
    Row,
    ScalarQueryParameter,
    SchemaField,
    Table,
)
from psycopg2 import sql

from base_job import BaseETLJob, parse_args

OUTPUT_TABLE_SCHEMA = [
    SchemaField("port_name", "STRING", mode="required"),
    SchemaField("distance_in_meters", "FLOAT64", mode="required"),
]


class Job(BaseETLJob):
    def extract(self):
        row = self.retrieve_index_number_and_port_geom_by_port_name("JURONG ISLAND")
        nearest_ports = self.retrieve_nearest_ports(row.index_number, row.port_geom)

        return [
            {
                "port_name": port.port_name,
                "distance_in_meters": port.distance_in_meters,
            }
            for port in nearest_ports
        ]

    def load(self, rows: List[dict]) -> List[dict]:
        self.create_table()
        self.insert_rows(rows)
        return rows

    def retrieve_index_number_and_port_geom_by_port_name(self, port_name: str) -> Row:
        QUERY_INDEX_NUMBER_AND_PORT_GEOM_BY_PORT_NAME = f"""
            SELECT
                index_number,
                port_geom
            FROM
                `{sql.Identifier(self.input_table_name).string}`
            WHERE
                port_name = @port_name;
        """

        job_config = QueryJobConfig(
            query_parameters=[
                ScalarQueryParameter("port_name", "STRING", port_name),
            ],
        )
        query_job = self.client.query(
            QUERY_INDEX_NUMBER_AND_PORT_GEOM_BY_PORT_NAME, job_config
        )
        rows = [row for row in query_job]
        if not rows:
            raise ValueError(
                f"No ports found. Errors may have occured when copying {self.input_table_name}."
            )
        elif len(rows) > 1:
            raise ValueError(
                "More than 1 port with the same name. Expected only 1 port"
            )

        return rows[0]

    def retrieve_nearest_ports(self, port_index_number: str, point: str) -> List[Row]:
        QUERY_FOR_NEAREST_PORTS_TO_PORT = f"""
            SELECT
                port_name,
                ST_DISTANCE(ST_GEOGFROMTEXT(@point), port_geom) AS distance_in_meters
            FROM
                `{sql.Identifier(self.input_table_name).string}`
            WHERE
                index_number <> @index_number
            ORDER BY
                distance_in_meters ASC
            LIMIT
                5;
        """

        job_config = QueryJobConfig(
            query_parameters=[
                ScalarQueryParameter("index_number", "STRING", port_index_number),
                ScalarQueryParameter("point", "STRING", point),
            ],
        )
        query_job = self.client.query(QUERY_FOR_NEAREST_PORTS_TO_PORT, job_config)
        rows = [row for row in query_job]
        return rows

    def create_table(self):
        table = Table(self.output_table_name, schema=OUTPUT_TABLE_SCHEMA)
        self.client.create_table(table)
        logging.info(f"Table created: {table}")

    def insert_rows(self, rows: List[Row]):
        self.client.insert_rows_json(self.output_table_name, rows)


def main():
    arguments = parse_args(
        description="This job searches the 5 nearest ports to JURONG ISLAND, and creates an output job table on BigQuery"
    )
    if not arguments:
        return
    results = Job(**arguments).execute()
    logging.info("port_name, distance_in_meters")
    for row in results:
        logging.info(f"{row['port_name']}, {row['distance_in_meters']}")


if __name__ == "__main__":
    main()
