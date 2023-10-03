import mysql.connector

db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "test",
}
conn = mysql.connector.connect(**db_config)