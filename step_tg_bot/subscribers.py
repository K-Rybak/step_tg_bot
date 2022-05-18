#from arrival_tg_bot import subscribers_collection
from connect_to_bd import get_subscribers_collection

subscribers_collection = get_subscribers_collection()
# проверяем есть ли уже юзер базе
def subscriber_exists(tg_user_id):
    return subscribers_collection.count_documents({'tg_user_id': tg_user_id})

# добавляем id нового подписчика
def add_subscriber(tg_user_id, tg_username, status=True):
    return subscribers_collection.insert_one({
            'tg_user_id': tg_user_id, 'tg_username': tg_username, 'status': status
        })

# обновляем статус подписки
def update_subscription(tg_user_id, status):
    return subscribers_collection.update_one({'tg_user_id': tg_user_id}, {'$set': {'status': status}})


# Получаем все id юзеров
def get_subscribers():
    subscribers = subscribers_collection.find({'status': True})
    tg_id_subscriber = []
    for id in subscribers:
        tg_id_subscriber.append(id['tg_user_id'])

    return tg_id_subscriber

def get_all_users():
    users = subscribers_collection.find()
    tg_id_users = []

    for id in users:
        tg_id_users.append(id['tg_user_id'])
    
    return tg_id_users
    

