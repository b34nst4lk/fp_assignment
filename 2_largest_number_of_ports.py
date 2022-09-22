from typing import List

from google.cloud.bigquery import Row, SchemaField, Table

from base_job import BaseETLJob

PROJECT_ID = "silicon-glyph-363112"
DATASET = "foodpanda_exercise"
INPUT_TABLE_NAME = "world_port_index"

COUNT_PORTS_WITH_CARGO_WHARF_BY_COUNTRY = """
    WITH group_by_country as (
        SELECT
            country,
            COUNT(*) as port_count
        FROM
            `foodpanda_exercise.world_port_index`
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

TABLE_ID = "country_with_most_cargo_wharf"

TABLE_SCHEMA = [
    SchemaField("country", "STRING", mode="required"),
    SchemaField("port_count", "INTEGER", mode="required"),
]


class Job(BaseETLJob):
    OUTPUT_TABLE_NAME = f"{PROJECT_ID}.{DATASET}.{TABLE_ID}"

    def extract(self):
        rows = self.retrieve_country_with_most_ports_with_cargo_wharf()
        return [
            {
                "country": row.country,
                "port_count": row.port_count,
            }
            for row in rows
        ]

    def load(self, rows: List[dict]):
        self.create_table()
        self.insert_rows(rows)

    def retrieve_country_with_most_ports_with_cargo_wharf(self) -> List[Row]:
        query_job = self.client.query(COUNT_PORTS_WITH_CARGO_WHARF_BY_COUNTRY)
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
