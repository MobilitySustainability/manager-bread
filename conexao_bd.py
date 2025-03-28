import mysql.connector
from mysql.connector import Error

def conectar_mysql():
    try:
        
        conn = mysql.connector.connect(
            host="sql.freedb.tech",
            user="freedb_mobilityunip",
            password="U6gwA8HQ3s&erwF",
            database="freedb_ManagerBreadAd"
        )

        if conn.is_connected():
            return conn
        else:
            return None

    except Error as e:
        return None

