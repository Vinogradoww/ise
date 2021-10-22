from pymongo import MongoClient


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    uri = ''
    client = None
    database = ''

    def get_client(self, host: str = '127.0.0.1', port: int = 27017, username: str = '', password: str = ''):
        if username:
            uri = "mongodb://%s:%s@%s:%s" % (
                username,
                password,
                host,
                port
            )
        else:
            uri = "mongodb://%s:%s" % (
                host,
                port
            )
        self.uri = uri
        self.client = MongoClient(self.uri)
        return self.client

    def set_db(self, database: str = ''):
        self.database = database
        return self.database

    def get_table(self, table: str = ''):
        if not self.database:
            return "Please select database (call method set_db())"
        return self.client[self.database][table]

    def _find(self, table: str = '', params=None):
        if params is None:
            params = {}
        table = self.get_table(table)
        if type(table) == str:
            return table
        return table.find(params)

    def _find_one(self, table: str = '', params=None):
        if params is None:
            params = {}
        table = self.get_table(table)
        if type(table) == str:
            return table
        return table.find_one(params)

    def _save(self, table: str = '', params=None):
        if params is None:
            params = {}
        table = self.get_table(table)
        if type(table) == str:
            return table
        return table.insert_one(params)


if __name__ == "__main__":
    s1 = Database()
    s2 = Database()

    print(s1, "\t", s1.get_client())
    print(s2.client)

    s1.set_db(database="mydb")
    #res = s1._save("testtable", {"username": "admin", "password": "12345"})
    #print(res)
    #res = s1._find_one(table="testtable", params={"username": "admin"})
    #print(res)


