from typing import List

from google.cloud.bigquery import Row

from base_job import BaseJob

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


class Job(BaseJob):
    def retrieve_country_with_most_ports_with_cargo_wharf(self) -> List[Row]:
        query_job = self.client.query(COUNT_PORTS_WITH_CARGO_WHARF_BY_COUNTRY)
        rows = [row for row in query_job]
        return rows


def main():
    job = Job()
    rows = job.retrieve_country_with_most_ports_with_cargo_wharf()
    first_row = rows[0]
    print(first_row.country, first_row.port_count, sep="\t")


if __name__ == "__main__":
    main()
