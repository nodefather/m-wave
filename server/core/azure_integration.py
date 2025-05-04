import os
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient
from azure.iot.device import IoTHubDeviceClient

# Azure Storage Blob Example
storage_conn_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
if storage_conn_str:
    blob_service_client = BlobServiceClient.from_connection_string(storage_conn_str)
    # Example: List containers
    containers = list(blob_service_client.list_containers())
    print(f"Azure Storage Containers: {[c['name'] for c in containers]}")

# Azure Cosmos DB Example
cosmos_url = os.getenv("AZURE_COSMOS_URL")
cosmos_key = os.getenv("AZURE_COSMOS_KEY")
if cosmos_url and cosmos_key:
    cosmos_client = CosmosClient(cosmos_url, credential=cosmos_key)
    # Example: List databases
    databases = list(cosmos_client.list_databases())
    print(f"Azure Cosmos DBs: {[db['id'] for db in databases]}")

# Azure IoT Hub Device Example
iot_conn_str = os.getenv("AZURE_IOTHUB_DEVICE_CONNECTION_STRING")
if iot_conn_str:
    device_client = IoTHubDeviceClient.create_from_connection_string(iot_conn_str)
    # Example: Connect and send a test message
    device_client.connect()
    device_client.send_message("Hello from M-WAVE device!")
    print("Test message sent to Azure IoT Hub.")
    device_client.disconnect() 