from typing import List

from google.cloud import bigquery
from google.oauth2 import service_account


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
        10
"""


class Job:
    def __init__(self, client: bigquery.Client):
        self.client = client

    def retrieve_country_with_most_ports_with_cargo_wharf(self) -> List[bigquery.Row]:
        query_job = self.client.query(COUNT_PORTS_WITH_CARGO_WHARF_BY_COUNTRY)
        rows = [row for row in query_job]
        return rows


def main():
    credentials = service_account.Credentials.from_service_account_file(
        "./key.json", scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    job = Job(client)
    rows = job.retrieve_country_with_most_ports_with_cargo_wharf()
    first_row = rows[0]
    print(first_row.country, first_row.port_count, sep="\t")


if __name__ == "__main__":
    main()
