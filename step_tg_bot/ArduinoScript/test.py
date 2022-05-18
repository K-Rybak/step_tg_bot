
from datetime import datetime
import time


import connect_to_db as con

count = 0
while not con.connect_to_db():
    time.sleep(1)
    count += 1
    print(f'Попытка переподключения - {count}')


time_arrival = con.db.test
record = con.db.eml_test
pos_empl = con.db.position_test

def get_arrival_today():
    current_date = datetime.today().strftime("%d.%m.%Y")
    list_of_employees = record.find({'current_date': current_date, 'status': True})
    list_arrival_today = 'Список сотрудников на рабочем месте:\n'
    count = 0
    for item in list_of_employees:
        count += 1
        list_arrival_today += '{}. {} - {}\n'.format(count, item['fullname'], item['arrival_time'])

    return list_arrival_today


print(get_arrival_today())