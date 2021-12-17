from pymongo import MongoClient
import uuid
import os


class Variables:

    def __init__(self, db_host: str, db_port: int, db_pass: str, db_user: str, db_name: str):
        self.db_host = db_host  # <-- dependency is injected
        self.db_port = db_port  # <-- dependency is injected
        self.db_pass = db_pass  # <-- dependency is injected
        self.db_user = db_user  # <-- dependency is injected
        self.db_name = db_name  # <-- dependency is injected


class ConnectDB:

    def __init__(self, requisites: Variables):
        self.requisites = requisites  # <-- dependency is injected

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


def main(db_connection: ConnectDB):   # <-- dependency is injected
    db = db_connection.connect()

    uid = str(uuid.uuid4())
    db["testcollection"].insert_one({"msg": "Hello", "uid": uid})
    res = db["testcollection"].find_one({"uid": uid})
    print(res)


if __name__ == "__main__":
    """
        Класс Variables не зависит от того, откуда берутся переменные. Они могут, например, читаться из environment,
    из конфига, вводиться через консоль и тд и тп.
    
        Класс ConnectDB не зависит от Variables, в том смысле, что он больше его не создаёт. Variables можно заменить
    на другой совместимый объект.
    
        Функция main также не зависит от ConnectDB, она его не создаёт, а принимает как аргумент.
    """
    main(
        db_connection=ConnectDB(
            requisites=Variables(
                db_host=os.getenv("DB_HOST"),
                db_port=int(os.getenv("DB_PORT")),
                db_pass=os.getenv("DB_PASS"),
                db_user=os.getenv("DB_USER"),
                db_name=os.getenv("DB_NAME"),
            ),
        ),
    )