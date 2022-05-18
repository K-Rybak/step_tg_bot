from pymongo import MongoClient

def connect_to_db():
    global db
    try:
        client = MongoClient("mongodb+srv://user_rybak_test:dad454221@cluster0.c4w91.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true")
        db = client.get_database('test_db')
        print('Подключение к базе прошло успешно!')
        return True
    except:
        print('!!!Не удалось подключиться к базе!!!')
        return False
