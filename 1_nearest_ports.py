import logging
from typing import List
from datetime import datetime

from google.cloud.bigquery import (
    QueryJobConfig,
    Row,
    ScalarQueryParameter,
    SchemaField,
    Table,
)

from base_job import BaseETLJob, timestamp

PROJECT_ID = "silicon-glyph-363112"
DATASET = "foodpanda_exercise"
INPUT_TABLE_NAME = "world_port_index"

QUERY_INDEX_NUMBER_AND_PORT_GEOM_BY_PORT_NAME = f"""
    SELECT
        index_number,
        port_geom
    FROM
        `{DATASET}.{INPUT_TABLE_NAME}`
    WHERE
        port_name = @port_name;
"""


QUERY_FOR_NEAREST_PORTS_TO_PORT = f"""
    SELECT
        port_name,
        ST_DISTANCE(ST_GEOGFROMTEXT(@point), port_geom) AS distance_in_meters
    FROM
        `{DATASET}.{INPUT_TABLE_NAME}`
    WHERE
        index_number <> @index_number
    ORDER BY
        distance_in_meters ASC
    LIMIT
        5;
"""

TABLE_ID = "nearest_ports_to_jurong_island"

TABLE_SCHEMA = [
    SchemaField("port_name", "STRING", mode="required"),
    SchemaField("distance_in_meters", "FLOAT64", mode="required"),
]
OUTPUT_TABLE_NAME = f"{PROJECT_ID}.{DATASET}.{TABLE_ID}"


class Job(BaseETLJob):
    OUTPUT_TABLE_NAME = f"{PROJECT_ID}.{DATASET}.{TABLE_ID}"

    def extract(self):
        row = self.retrieve_index_number_and_port_geom_by_port_name("JURONG ISLAND")
        nearest_ports = self.retrieve_nearest_ports(row.index_number, row.port_geom)
        for port in nearest_ports:
            logging.info(f"{port.port_name}, {port.distance_in_meters}")

        return [
            {
                "port_name": port.port_name,
                "distance_in_meters": port.distance_in_meters,
            }
            for port in nearest_ports
        ]

    def load(self, rows):
        self.create_table()
        self.insert_rows(rows)

    def retrieve_index_number_and_port_geom_by_port_name(self, port_name: str) -> Row:
        job_config = QueryJobConfig(
            query_parameters=[
                ScalarQueryParameter("port_name", "STRING", port_name),
            ],
        )
        query_job = self.client.query(
            QUERY_INDEX_NUMBER_AND_PORT_GEOM_BY_PORT_NAME, job_config
        )
        rows = [row for row in query_job]
        if len(rows) != 1:
            raise ValueError(
                "More than 1 port with the same name. Expected only 1 port"
            )

        return rows[0]

    def retrieve_nearest_ports(self, port_index_number: str, point: str) -> List[Row]:
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
        table = Table(self.output_table_name, schema=TABLE_SCHEMA)
        self.client.create_table(table)

    def insert_rows(self, rows: List[Row]):
        self.client.insert_rows_json(self.output_table_name, rows)


def main():
    Job().execute()

if __name__ == "__main__":
    main()
