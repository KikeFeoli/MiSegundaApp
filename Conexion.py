import pyodbc

print(pyodbc.drivers())

try:
    print(pyodbc.drivers())
except Exception as error:
    print(error)

def Conectar():

    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=MiPrimeraApp;"
        "Trusted_Connection=yes;"
    )

