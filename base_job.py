from typing import List
from datetime import datetime

from google.cloud import bigquery
from google.oauth2 import service_account


def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


class BaseETLJob:
    OUTPUT_TABLE_NAME = None

    def __init__(self, service_account_key_path: str = "./key.json"):
        if not self.OUTPUT_TABLE_NAME:
            raise ValueError(
                f"{self.__class__.__name__}.OUTPUT_TABLE_NAME cannot be None"
            )

        self.output_table_name = f"{self.OUTPUT_TABLE_NAME}_{timestamp()}"
        credentials = service_account.Credentials.from_service_account_file(
            service_account_key_path,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.client = bigquery.Client(
            credentials=credentials, project=credentials.project_id
        )

    def extract(self) -> List[dict]:
        ...

    def transform(self, rows: List[dict]) -> List[dict]:
        return rows

    def load(self, rows: List[dict]):
        ...

    def execute(self):
        extracted_rows = self.extract()
        transformed_rows = self.transform(extracted_rows)
        self.load(transformed_rows)
