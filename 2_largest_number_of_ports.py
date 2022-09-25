import logging
from typing import List

from google.cloud.bigquery import Row, SchemaField, Table
from psycopg2 import sql

from base_job import BaseETLJob, parse_args

OUTPUT_TABLE_SCHEMA = [
    SchemaField("country", "STRING", mode="required"),
    SchemaField("port_count", "INTEGER", mode="required"),
]


class Job(BaseETLJob):
    def extract(self):
        rows = self.retrieve_country_with_most_ports_with_cargo_wharf()
        return [
            {
                "country": row.country,
                "port_count": row.port_count,
            }
            for row in rows
        ]

    def load(self, rows: List[dict]) -> List[dict]:
        self.create_table()
        self.insert_rows(rows)
        return rows

    def retrieve_country_with_most_ports_with_cargo_wharf(self) -> List[Row]:
        COUNT_PORTS_WITH_CARGO_WHARF_BY_COUNTRY = f"""
            WITH group_by_country as (
                SELECT
                    country,
                    COUNT(*) as port_count
                FROM
                    `{sql.Identifier(self.input_table_name).string}`
                WHERE
                    cargo_wharf is TRUE
                GROUP BY
                    country
            )
            SELECT
                country,
                port_count
            FROM
                group_by_country
            ORDER BY
                port_count DESC
            LIMIT
                1
        """

        query_job = self.client.query(COUNT_PORTS_WITH_CARGO_WHARF_BY_COUNTRY)
        rows = [row for row in query_job]
        return rows

    def create_table(self):
        table = Table(self.output_table_name, schema=OUTPUT_TABLE_SCHEMA)
        self.client.create_table(table)

    def insert_rows(self, rows: List[Row]):
        self.client.insert_rows_json(self.output_table_name, rows)


def main():
    arguments = parse_args(
        description="This job searches for the country with the most number of ports with cargo wharves, and creates an output job table on BigQuery"
    )
    if not arguments:
        return
    results = Job(**arguments).execute()
    logging.info("country, port_count")
    for row in results:
        logging.info(f"{row['country']}, {row['port_count']}")


if __name__ == "__main__":
    main()
