import pyodbc

server = "sql-srv-kenny-all-ea.database.windows.net"
database = "sql-db-main-kenny-all-ea"
username = "zhangsi@kennyisagoodman.top"
password = "Zs850605:)"
driver = '{ODBC Driver 17 for SQL Server}'


conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=sql-srv-kenny-all-ea.database.windows.net;"
    "DATABASE=sql-db-main-kenny-all-ea;"
    "UID=zhangsi@kennyisagoodman.top;"
    "PWD=Zs850605:);"
    "Authentication=ActiveDirectoryPassword;"
)

conn = pyodbc.connect(conn_str)
curor = conn.cursor()
curor.execute("select * from students")
rows = curor.fetchall()
for row in rows:
    print(row)

curor.close()
conn.close()