import logging
import config
import asyncio
import aioschedule
import connect_to_bd as db
import subscribers as sub
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

record = db.get_empl_collection()
pos_db = db.get_position_collection()
subscribers_colllection = db.get_subscribers_collection()

@dp.message_handler(commands=['start'])
async def add_to_bot(message: types.Message):
    await bot.send_message(message.chat.id, 'Здраствуйте, {} \n Введите команду для получения информации'.format(message.from_user.full_name))

@dp.message_handler(commands=['today'])
async def send_today_arrival(message: types.Message):
    list_of_employees = get_arrival_today()
    await bot.send_message(message.chat.id, list_of_employees)

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not sub.subscriber_exists(message.chat.id)):
        # если юзера нет, добавлем его
        sub.add_subscriber(message.chat.id, message.from_user.full_name)
        await message.reply('Бот успешно подписались на рассылку')
    else:
        sub.update_subsription(message.chat.id, True)
        await message.reply('Вы снова подписались на рассылку')

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not sub.subscriber_exists(message.chat.id)):
        # если юзера нет, добавлем его
        sub.add_subscriber(message.chat.id, message.from_user.full_name, False)
        await message.reply('Вы и так не попидсаны на рассылку')
    else:
        sub.update_subsription(message.chat.id, False)
        await message.reply('Вы успешно отписались от рассылки')


def get_arrival_today():
    current_date = datetime.today().strftime("%d.%m.%Y")
    list_of_employees = record.find({'current_date': current_date, 'status': True})
    list_arrival_today = 'Список сотрудников на рабочем месте:\n'
    i = 0
    for item in list_of_employees:
        i += 1
        list_arrival_today += '{}. {} - {}\n'.format(i, item['fullname'], item['arrival_time'])

    return list_arrival_today

#
async def send_laters():
    position = pos_db.find_one({'position_name': 'Преподаватель МА'})
    print(position['_id'])
    query = {'status': False, 'position': position['_id']}
    if record.count_documents(query) != 0:
        list_of_employees = record.find(query)
        list_arrival_today = 'Список сотрудников НЕ на рабочем месте:\n'
        i = 0
        for item in list_of_employees:
            i += 1
            list_arrival_today += '{}. {}\n'.format(i, item['fullname'])

        tg_user_id = sub.get_subscribers()
        for id in tg_user_id:
            await bot.send_message(id, list_arrival_today)
            print(id, list_arrival_today)
    else:
        print('Опоздавших нет')

async def scheduler():
    aioschedule.every().day.at("16:42").do(send_laters)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())

# Запускаем бота
if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
    
