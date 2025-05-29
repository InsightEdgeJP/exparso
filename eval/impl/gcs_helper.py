import io
import tempfile

import pandas as pd
from google.cloud import storage


class GCSHelper:
    def __init__(self, bucket_name: str):

        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)

    def download_blob_to_df(self, source_blob_name: str) -> pd.DataFrame:
        blob = self.bucket.blob(source_blob_name)
        excel_data = io.BytesIO(blob.download_as_bytes())
        return pd.read_excel(excel_data)

    def upload_file_to_blob(self, path: str, blob_name: str):
        blob = self.bucket.blob(blob_name)
        with open(path, "rb") as f:
            blob.upload_from_file(f)

    def upload_df_to_blob(self, df: pd.DataFrame, blob_name: str):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = f"{temp_dir}/data.xlsx"
            df.to_excel(path, index=False)
            self.upload_file_to_blob(path, blob_name)

    def get_blob_list(self, prefix: str) -> list[str]:
        blobs = self.bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]
