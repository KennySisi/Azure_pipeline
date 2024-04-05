import os
from fastapi import FastAPI
import pyodbc
# from azure.applicationinsights import applicationinsights

from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient

credential = DefaultAzureCredential()

subscription_id = 'd90899a9-7716-4f55-88fe-22720fe4d18a'
resource_group = 'rg-spoke-kenny-myapp-ea'
server_name = 'sql-srv-kenny-all-ea'
database_name = 'sql-db-main-kenny-all-ea'

sql_client = SqlManagementClient(credential, subscription_id)

server = sql_client.servers.get(resource_group, server_name)
connection_string = f"Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{server.fully_qualified_domain_name};Database={database_name};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentication=ActiveDirectoryMSI"

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sql-srv-kenny-all-ea.database.windows.net;"
    "DATABASE=sql-db-main-kenny-all-ea;"
    #"UID=zhangsi@kennyisagoodman.top;"
    #"PWD=Zs850605:);"
    "Authentication=ActiveDirectoryMsi;"
    #"Authentication=ActiveDirectoryPassword;"
)

app = FastAPI()
# instrumentation_key = os.environ.get('INSTRUMENTATION_KEY')
# if instrumentation_key:
#     azure_app_insights = applicationinsights(instrumentation_key=instrumentation_key)
#     azure_app_insights.init_app(app)

@app.get("/Add/{number1}")
def add_two(number1):
    return {f"backend env: Your input is: {number1}"}

@app.get("env/{env_name}")
def queryDBString(env_name: str):
    return os.environ.get(env_name)

@app.get("/dbtest")
def queryDataBase():
    # @Microsoft.KeyVault(SecretUri=https://test-key-vault-ea.vault.azure.net/secrets/DB-Kenny-Conn-Str/63abcb49cb264a1a852cd192f4377ffd)
    connection_str_from_env = os.environ.get('DB_KENNY_CONN_STR')
    conn = pyodbc.connect(connection_str_from_env)
    curor = conn.cursor()
    curor.execute("select * from students") 
    rows = curor.fetchall()
    for row in rows:
        print(row)

    curor.close()
    conn.close()

    return str(rows)

@app.get("/storagetest/{item_name}")
def queryStorageAccount(item_name: str):
    account_name = "stvmkennymyappea"
    container_name = "testcontainer"
    blob_name = item_name #"stex_initial_setup.ps1"
    #account_key="+cXhEDQmxmUafIp4qHtc7qkx7GdRwUXBrdec1bfJveOfyv5Wb6dLa9kAI/Y8uuBFXWBUjhZE4+PV+AStrzKApQ=="

    #AccountKey={account_key};
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};EndpointSuffix=core.windows.net"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string, credential=credential) 
    #(f"https://{account_name}.blob.core.windows.net/", credential)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob() #container_client.list_blobs("stex_") #list_blob_names()
    content = blob_data.readall()
    return content

    # ret = ''
    # for blob_name in blob_list:
    #     ret = ret + blob_name + ";<br>"
    
    # return ret

@app.get("/")
def rootFunction():
    return "Hello 3, visitor new deploy triggered"



