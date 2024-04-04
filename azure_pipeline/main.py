from fastapi import FastAPI
import pyodbc
# from azure.applicationinsights import applicationinsights

from azure.storage.blob import BlobServiceClient

app = FastAPI()
# instrumentation_key = os.environ.get('INSTRUMENTATION_KEY')
# if instrumentation_key:
#     azure_app_insights = applicationinsights(instrumentation_key=instrumentation_key)
#     azure_app_insights.init_app(app)

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

