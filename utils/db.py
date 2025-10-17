from pymongo import MongoClient


_db = None


def get_db(uri=None):
    global _db
    if _db is None:
        if uri is None:
            raise RuntimeError('MONGO_URI not provided for DB connection')
        client = MongoClient(uri)
        _db = client.get_default_database()
    return _db