from typing import List

from google.cloud.bigquery import QueryJobConfig, Row, ScalarQueryParameter

from base_job import BaseJob

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
        5;
"""


class Job(BaseJob):
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


def main():
    job = Job()
    rows = job.retrieve_port_closest_to_distress_call(32.610982, -38.706256)
    first_row = rows[0]
    print(
        first_row.country,
        first_row.port_name,
        first_row.port_latitude,
        first_row.port_longitude,
        sep="\t",
    )


if __name__ == "__main__":
    main()
