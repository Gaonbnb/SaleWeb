from pyhive import hive

connection = hive.Connection(host="127.0.0.1", port = 10000, username= "hive",  database="default")
cursor = connection.cursor()
cursor.execute("SELECT * FROM myexchange limit 10")
print(cursor.fetchall())