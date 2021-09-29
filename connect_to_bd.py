from pymongo import MongoClient

try:
    client = MongoClient("mongodb+srv://user_rybak_test:dad454221@cluster0.c4w91.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.get_database('test_db')
except Exception as e:
    print('Не удалось подключится к базе данных')
    print(e)


def get_empl_collection():
    record = db.eml_test
    return record

def get_position_collection():
    record = db.position_test
    return record

def get_subscribers_collection():
    record = db.subscribers
    return record
