from typing import List

from google.cloud import bigquery
from google.oauth2 import service_account


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
        20;

"""


class Job:
    def __init__(self, client: bigquery.Client):
        self.client = client

    def retrieve_port_closest_to_distress_call(
        self, lat: float, lng: float
    ) -> List[bigquery.Row]:
        point = f"POINT({lng} {lat})"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("point", "STRING", point),
            ],
        )

        query_job = self.client.query(DISTRESS_CALL, job_config)
        rows = [row for row in query_job]
        return rows


def main():
    credentials = service_account.Credentials.from_service_account_file(
        "./key.json", scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    job = Job(client)
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
