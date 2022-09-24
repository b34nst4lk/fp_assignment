import logging
from argparse import ArgumentParser
from datetime import datetime
from typing import List

from google.cloud import bigquery
from google.oauth2 import service_account

logging.root.setLevel(logging.INFO)


def formatted_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def parse_args(
    description: str = (
        "This is the default description."
        "Provide a description for the parse_args function to overwrite it."
    ),
):
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--service_account_key_path", help="Path to the service account credentials key"
    )
    parser.add_argument("--project_id", help="GCP Project ID", required=True)
    parser.add_argument("--dataset", help="Name of dataset", required=True)
    parser.add_argument("--input_table", help="Name of input table", required=True)
    parser.add_argument("--output_table", help="Name of output table", required=True)

    try:
        return vars(parser.parse_args())
    except Exception as e:
        parser.print_help()
        return None


class BaseETLJob:
    def __init__(
        self,
        service_account_key_path: str,
        project_id: str,
        dataset: str,
        input_table: str,
        output_table: str,
    ):
        prefix = f"{project_id}.{dataset}"
        self.output_table_name = f"{prefix}.{output_table}_{formatted_timestamp()}"
        self.input_table_name = f"{prefix}.{input_table}"

        credentials = service_account.Credentials.from_service_account_file(
            service_account_key_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.client = bigquery.Client(
            credentials=credentials, project=credentials.project_id
        )

    def extract(self) -> List[dict]:
        raise NotImplemented

    def transform(self, rows: List[dict]) -> List[dict]:
        return rows

    def load(self, rows: List[dict]):
        raise NotImplemented

    def execute(self) -> List[dict]:
        extracted_rows = self.extract()
        transformed_rows = self.transform(extracted_rows)
        return self.load(transformed_rows)
