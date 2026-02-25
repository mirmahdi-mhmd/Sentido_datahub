# a class for connecting to database
class Connection:

    @staticmethod
    def connect():
        import pyodbc
        conn_string = (f"Driver=SQL Server;"
        "Server=DESKTOP-AOHSA5I\\EC_STORAGE;"
        "Database=Sentido_datahub;"
        "Trusted_Connection=yes;")
        connection = pyodbc.connect(conn_string)

        return connection
