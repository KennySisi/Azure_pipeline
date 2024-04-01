import os
from fastapi import FastAPI

# from azure.applicationinsights import applicationinsights

import pyodbc

conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sql-srv-kenny-all-ea.database.windows.net;"
    "DATABASE=sql-db-main-kenny-all-ea;"
    "UID=zhangsi@kennyisagoodman.top;"
    "PWD=Zs850605:);"
    "Authentication=ActiveDirectoryPassword;"
)


app = FastAPI()

# instrumentation_key = os.environ.get('INSTRUMENTATION_KEY')

# if instrumentation_key:
#     azure_app_insights = applicationinsights(instrumentation_key=instrumentation_key)
#     azure_app_insights.init_app(app)

@app.get("/")
def rootFunction():
    return "Hello, visitor new deploy triggered"


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
