import pyodbc


def create_db(server, database, driver="{ODBC Driver 17 for SQL Server}"):
    conn = pyodbc.connect(
        f"DRIVER={driver};SERVER={server};Trusted_Connection=yes;",
        autocommit=True
    )
    cursor = conn.cursor()

    cursor.execute(
        f"IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = '{database}') CREATE DATABASE {database}"
    )

    cursor.close()
    conn.close()
