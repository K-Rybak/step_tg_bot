from datetime import datetime
import connect_to_bd as db
record = db.get_empl_collection()

def get_arrival_today():
    current_date = datetime.today().strftime("%d.%m.%Y")
    list_of_employees = record.find({'current_date': current_date, 'status': True})
    list_arrival_today = 'Список сотрудников на рабочем месте:\n'
    count = 0
    for item in list_of_employees:
        count += 1
        list_arrival_today += '{}. {} - {}\n'.format(count, item['fullname'], item['arrival_time'])

    return list_arrival_today

def get_daily_report():
    current_date = datetime.today().strftime("%d.%m.%Y")
    list_of_employees = record.find({'current_date': current_date, 'status': False})
    list_arrival_today = 'Список сотрудников за {}:\n'.format(current_date)

    count = 0
    for empl in list_of_employees:
        count += 1
        list_arrival_today += '{}. {} - пришел: {}, ушел: {}\n'.format(count, empl['fullname'], empl['arrival_time'], empl['leaving_time'])


def get_laters_employees(list_of_employees):
    list_not_arrival = 'Список сотрудников НЕ на рабочем месте:\n'
    i = 0
    for item in list_of_employees:
        i += 1
        list_not_arrival += '{}. {}\n'.format(i, item['fullname'])

    return list_not_arrival

async def reset_status_emploees():
    await record.update_many({'status': True}, {'$set': {'status': False}})