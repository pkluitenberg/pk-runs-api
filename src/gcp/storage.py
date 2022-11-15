import json

from google.cloud import storage

GCP_PROJECT='pk-runs'

def read_json_from_google_cloud_storage(bucket: str, filename: str):
    storage_client = storage.Client(project=GCP_PROJECT)
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(filename)

    # download as string is getting deprecated so this needs to get updated
    return json.loads(blob.download_as_string())