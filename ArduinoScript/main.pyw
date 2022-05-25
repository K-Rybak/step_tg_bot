import serial
import time
import connect_to_db
from datetime import datetime

# Функция для записи времени прихиода и ухода сотрудника в бд
def update_time_in_db(emloyee_id, field_in_bd, arrival_or_leaving_time, status, current_date):
    record.update_one({'_id': emloyee_id}, {'$set':
            {field_in_bd: arrival_or_leaving_time, 
            'status': status,
            'current_date': current_date
            }})

def check_connection(con):
    count = 0
    while not con.connect_to_db():
        time.sleep(1)
        count += 1
        print(f'Попытка переподключения - {count}')

def add_employee(record, uid):
    # Если сотрудник есть в базе, то обновляем его данные
    if record.count_documents({"uid":uid}) == 1:
        employee = record.find_one({"uid":uid})
        current_date = datetime.today().strftime("%d.%m.%Y")
        today_time = datetime.today().strftime("%H:%M")
        field_in_bd = ''
        if employee['status'] == False:
            field_in_bd = 'arrival_time'
            update_time_in_db(employee['_id'], field_in_bd, today_time, True, current_date)
            print('Сотрудник {} пришел в {}'.format(employee['fullname'], today_time))
        else:
            field_in_bd = 'leaving_time'
            update_time_in_db(employee['_id'], field_in_bd, today_time, False, current_date)
            print('Сотрудник {} ушел в {}'.format(employee['fullname'], today_time))
    # Иначе сообщаем
    else:
        print('Данного сотрудника нет в базе данных')

def app_loop(serial, record):
    while True:
        inp = str(serial.read())[2]
        if inp:
            uid = '' + inp
            for _ in range(27):
                uid += str(serial.read())[2]
            uid = uid[uid.find("UID:"):uid.find("\\\\Card SAK")]
            uid = uid[5:] 
            add_employee(record, uid)
        # задержка что бы не перегружать процессор
        time.sleep(5)


if __name__ == '__main__':
    con = connect_to_db.Connection()
    check_connection(con)

    record = con.db.eml_test
    ser = serial.Serial("COM7")
    print(ser.name)
    app_loop(ser, record=record)


