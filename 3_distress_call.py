from typing import List

from google.cloud.bigquery import (
    QueryJobConfig,
    Row,
    ScalarQueryParameter,
    SchemaField,
    Table,
)

from base_job import BaseETLJob

PROJECT_ID = "silicon-glyph-363112"
DATASET = "foodpanda_exercise"
INPUT_TABLE_NAME = "world_port_index"

DISTRESS_CALL = """
    SELECT
        country,
        port_name,
        port_latitude,
        port_longitude,
        ST_DISTANCE(ST_GEOGFROMTEXT(@point), port_geom) AS distance_in_meters
    FROM
        `foodpanda_exercise.world_port_index`
    WHERE
        provisions is TRUE
        AND water is TRUE
        AND fuel_oil is TRUE
        AND diesel is TRUE
    ORDER BY
        distance_in_meters ASC
    LIMIT
        1;
"""

TABLE_ID = "distress_call"

TABLE_SCHEMA = [
    SchemaField("country", "STRING", mode="required"),
    SchemaField("port_name", "STRING", mode="required"),
    SchemaField("port_latitude", "FLOAT64", mode="required"),
    SchemaField("port_longitude", "FLOAT64", mode="required"),
]


class Job(BaseETLJob):
    OUTPUT_TABLE_NAME = f"{PROJECT_ID}.{DATASET}.{TABLE_ID}"

    def __init__(self, lat, lng):
        super().__init__()
        self.lat = lat
        self.lng = lng

    def extract(self):
        rows = self.retrieve_port_closest_to_distress_call(self.lat, self.lng)
        return [
            {
                "country": row.country,
                "port_name": row.port_name,
                "port_latitude": row.port_latitude,
                "port_longitude": row.port_longitude,
            }
            for row in rows
        ]

    def load(self, rows: List[dict]):
        self.create_table()
        self.insert_rows(rows)

    def retrieve_port_closest_to_distress_call(
        self, lat: float, lng: float
    ) -> List[Row]:
        point = f"POINT({lng} {lat})"
        job_config = QueryJobConfig(
            query_parameters=[
                ScalarQueryParameter("point", "STRING", point),
            ],
        )

        query_job = self.client.query(DISTRESS_CALL, job_config)
        rows = [row for row in query_job]
        return rows

    def create_table(self):
        table = Table(self.output_table_name, schema=TABLE_SCHEMA)
        self.client.create_table(table)

    def insert_rows(self, rows: List[Row]):
        self.client.insert_rows_json(self.output_table_name, rows)



def main():
    lat, lng = (32.610982, -38.706256)
    Job(lat, lng).execute()

if __name__ == "__main__":
    main()
