from fastapi import FastAPI
import pyodbc
# from azure.applicationinsights import applicationinsights

from azure.storage.blob import BlobServiceClient

app = FastAPI()
# instrumentation_key = os.environ.get('INSTRUMENTATION_KEY')
# if instrumentation_key:
#     azure_app_insights = applicationinsights(instrumentation_key=instrumentation_key)
#     azure_app_insights.init_app(app)

# from azure.applicationinsights import applicationinsights

# @app.get("/storagetest")
# def queryStorageAccount():
#     account_name = "stvmkennymyappea"
#     container_name = "testcontainer"
#     blob_service_client = BlobServiceClient(f"https://{account_name}.blob.core.windows.net/", credential=)
#     container_client = blob_service_client.get_container_client(container_name)
#     blob_list = container_client.list_blob_names()
#     return blob_list

@app.get("/Add/{number1}")
def add_two(number1):
    return {f"backend2: Your input is: {number1}"}

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sql-srv-kenny-all-ea.database.windows.net;"
    "DATABASE=sql-db-main-kenny-all-ea;"
    "Authentication=ActiveDirectoryMSI;"
    #"Authentication=ActiveDirectoryPassword;"
)

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

@app.get("/")
def rootFunction():
    return "Hello, visitor new deploy triggered"

