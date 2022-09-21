from typing import List

from google.cloud import bigquery
from google.oauth2 import service_account


QUERY_INDEX_NUMBER_AND_PORT_GEOM_BY_PORT_NAME = """
    SELECT
        index_number,
        port_geom
    FROM
        `foodpanda_exercise.world_port_index`
    WHERE
        port_name = @port_name;
"""


QUERY_FOR_NEAREST_PORTS_TO_PORT = """
    SELECT
        port_name,
        ST_DISTANCE(ST_GEOGFROMTEXT(@point), port_geom) AS distance_in_meters
    FROM
        `foodpanda_exercise.world_port_index`
    WHERE
        index_number <> @index_number
    ORDER BY
        distance_in_meters ASC
    LIMIT
        5;
"""


class Job:
    def __init__(self, client: bigquery.Client):
        self.client = client

    def retrieve_index_number_and_port_geom_by_port_name(
        self, port_name: str
    ) -> bigquery.Row:
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("port_name", "STRING", port_name),
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

    def retrieve_nearest_ports(
        self, port_index_number: str, point: str
    ) -> List[bigquery.Row]:
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "index_number", "STRING", port_index_number
                ),
                bigquery.ScalarQueryParameter("point", "STRING", point),
            ],
        )
        query_job = self.client.query(QUERY_FOR_NEAREST_PORTS_TO_PORT, job_config)
        rows = [row for row in query_job]
        return rows


def main():
    credentials = service_account.Credentials.from_service_account_file(
        "./key.json", scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    job = Job(client)
    row = job.retrieve_index_number_and_port_geom_by_port_name("JURONG ISLAND")
    nearest_ports = job.retrieve_nearest_ports(row.index_number, row.port_geom)
    for port in nearest_ports:
        print(port.port_name, port.distance_in_meters, sep="\t")


if __name__ == "__main__":
    main()
