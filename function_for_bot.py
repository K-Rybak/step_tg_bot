from datetime import datetime
import connect_to_bd as db
record = db.get_empl_collection()

def get_arrival_today():
    current_date = datetime.today().strftime("%d.%m.%Y")
    list_of_employees = record.find({'current_date': current_date, 'status': True})
    list_arrival_today = 'Список сотрудников на рабочем месте:\n'
    i = 0
    for item in list_of_employees:
        i += 1
        list_arrival_today += '{}. {} - {}\n'.format(i, item['fullname'], item['arrival_time'])

    return list_arrival_today

def get_laters_employees(list_of_employees):
    list_not_arrival = 'Список сотрудников НЕ на рабочем месте:\n'
    i = 0
    for item in list_of_employees:
        i += 1
        list_not_arrival += '{}. {}\n'.format(i, item['fullname'])

    return list_not_arrival

def reset_status_emploees():
    record.update_many({'status': True}, {'$set': {'status': False}})