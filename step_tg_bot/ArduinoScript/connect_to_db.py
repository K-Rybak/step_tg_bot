from pymongo import MongoClient
import datetime


class Connection():
    def connect_to_db(self):        
        try:
            client = MongoClient("mongodb+srv://user_rybak_test:dad454221@cluster0.c4w91.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=true")
            self.db = client.get_database('test_db')
            print('Подключение к базе прошло успешно!')
            return True
        except Exception as ex:
            print(datetime.datetime.today().strftime('%d.%m-%H:%M'), ex)
            return False
