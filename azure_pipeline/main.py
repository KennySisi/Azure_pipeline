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
    "Trusted_Connection=yes;"
)

app = FastAPI()
# instrumentation_key = os.environ.get('INSTRUMENTATION_KEY')
# if instrumentation_key:
#     azure_app_insights = applicationinsights(instrumentation_key=instrumentation_key)
#     azure_app_insights.init_app(app)

@app.get("/Add/{number1}")
def add_two(number1):
    return {f"backend2: Your input is: {number1}"}



@app.get("/dbtest")
def queryDataBase():
    conn = pyodbc.connect(conn_str)
    curor = conn.cursor()
    curor.execute("select * from students") 
    rows = curor.fetchall()
    for row in rows:
        print(row)

    curor.close()
    conn.close()

    return str(rows)

@app.get("/storagetest")
def queryStorageAccount():
    account_name = "stvmkennymyappea"
    container_name = "testcontainer"
    account_key="+cXhEDQmxmUafIp4qHtc7qkx7GdRwUXBrdec1bfJveOfyv5Wb6dLa9kAI/Y8uuBFXWBUjhZE4+PV+AStrzKApQ=="

    connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string) 
    #(f"https://{account_name}.blob.core.windows.net/", credential)
    container_client = blob_service_client.get_container_client(container_name)
    blob_list = container_client.list_blob_names()
    return blob_list

@app.get("/")
def rootFunction():
    return "Hello 3, visitor new deploy triggered"

