import os
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
import subprocess

def create_blob_container(container_name):
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise Exception("AZURE_STORAGE_CONNECTION_STRING not set")
    client = BlobServiceClient.from_connection_string(conn_str)
    client.create_container(container_name)
    print(f"Created blob container: {container_name}")

def upload_blob(container_name, file_path, blob_name=None):
    conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn_str:
        raise Exception("AZURE_STORAGE_CONNECTION_STRING not set")
    client = BlobServiceClient.from_connection_string(conn_str)
    blob_client = client.get_blob_client(container=container_name, blob=blob_name or os.path.basename(file_path))
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)
    print(f"Uploaded {file_path} to {container_name}/{blob_name or os.path.basename(file_path)}")

def create_cosmos_db(db_name, container_name, partition_key):
    url = os.getenv("AZURE_COSMOS_URL")
    key = os.getenv("AZURE_COSMOS_KEY")
    if not url or not key:
        raise Exception("AZURE_COSMOS_URL or AZURE_COSMOS_KEY not set")
    client = CosmosClient(url, credential=key)
    db = client.create_database_if_not_exists(id=db_name)
    db.create_container_if_not_exists(id=container_name, partition_key=partition_key)
    print(f"Created Cosmos DB: {db_name}, container: {container_name}")

def register_iot_device(hub_name, device_id):
    # Requires Azure CLI installed and logged in
    result = subprocess.run([
        "az", "iot", "hub", "device-identity", "create",
        "--hub-name", hub_name,
        "--device-id", device_id
    ], capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Registered IoT device: {device_id}")
        print(result.stdout)
    else:
        print(f"Failed to register device: {result.stderr}") 