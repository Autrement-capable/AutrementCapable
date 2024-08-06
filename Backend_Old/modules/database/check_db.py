from pymongo import MongoClient

# Connect to MongoDB server
client = MongoClient("mongodb://localhost:27017/")

# Check if the database exists
db_name = "mydatabase"
existing_dbs = client.list_database_names()
print(f"Existing databases: {existing_dbs}")

if db_name in existing_dbs:
    print(f"Database '{db_name}' still exists.")
else:
    print(f"Database '{db_name}' has been deleted.")

# Close the connection
client.close()