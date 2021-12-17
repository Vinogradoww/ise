from pymongo import MongoClient
import uuid
import os


class Variables:

    def __init__(self):
        self.db_host = os.getenv("DB_HOST")  # <-- dependency
        self.db_port = os.getenv("DB_PORT")  # <-- dependency
        self.db_pass = os.getenv("DB_PASS")  # <-- dependency
        self.db_user = os.getenv("DB_USER")  # <-- dependency
        self.db_name = os.getenv("DB_NAME")  # <-- dependency


class ConnectDB:

    def __init__(self):
        self.requisites = Variables()  # <-- dependency

    def connect(self):
        if self.requisites.db_user:
            mongo_client = MongoClient(
                f"mongodb://{self.requisites.db_user}:{self.requisites.db_pass}@{self.requisites.db_host}:{self.requisites.db_port}"
            )
        else:
            mongo_client = MongoClient(
                f"mongodb://{self.requisites.db_host}:{self.requisites.db_port}"
            )
        try:
            return mongo_client[self.requisites.db_name]
        except:
            raise Exception("Wrong DB_NAME")


def main():
    db_connection = ConnectDB()  # <-- dependency

    db = db_connection.connect()
    uid = str(uuid.uuid4())
    db["testcollection"].insert_one({"msg": "Hello", "uid": uid})
    res = db["testcollection"].find_one({"uid": uid})
    print(res)


if __name__ == "__main__":
    main()