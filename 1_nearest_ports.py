from typing import List

from google.cloud.bigquery import QueryJobConfig, Row, ScalarQueryParameter

from base_job import BaseJob

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


class Job(BaseJob):
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


def main():
    job = Job()
    row = job.retrieve_index_number_and_port_geom_by_port_name("JURONG ISLAND")
    nearest_ports = job.retrieve_nearest_ports(row.index_number, row.port_geom)
    for port in nearest_ports:
        print(port.port_name, port.distance_in_meters, sep="\t")


if __name__ == "__main__":
    main()
