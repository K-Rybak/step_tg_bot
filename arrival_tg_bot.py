import logging
import config
import asyncio
import aioschedule
import connect_to_bd as db
import subscribers as sub
import function_for_bot as fb
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
    list_of_employees = fb.get_arrival_today()
    await bot.send_message(message.chat.id, list_of_employees)

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not sub.subscriber_exists(message.chat.id)):
        # если юзера нет, добавлем его
        sub.add_subscriber(message.chat.id, message.from_user.full_name)
        await message.reply('Вы успешно подписались на рассылку')
    else:
        sub.update_subscription(message.chat.id, True)
        await message.reply('Вы снова подписались на рассылку')

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not sub.subscriber_exists(message.chat.id)):
        # если юзера нет, добавлем его
        sub.add_subscriber(message.chat.id, message.from_user.full_name, False)
        await message.reply('Вы и так не попидсаны на рассылку')
    else:
        sub.update_subscription(message.chat.id, False)
        await message.reply('Вы успешно отписались от рассылки')

# отправка всех опоздавших преподавателей
async def send_laters():
    position = pos_db.find_one({'position_name': 'Преподаватель МА'})
    query = {'status': False, 'position': position['_id']}
    tg_user_id = sub.get_subscribers()

    if record.count_documents(query) != 0:
        list_of_employees = record.find(query)
        list_not_arrival = fb.get_laters_employees(list_of_employees)
      
        for id in tg_user_id:
            await bot.send_message(id, list_not_arrival)
    else:
        for id in tg_user_id:
            await bot.send_message(id, 'Опоздавших нет')

async def scheduler():
    aioschedule.every().friday.at("02:50").do(send_laters)
    aioschedule.every().saturday.at("03:20").do(send_laters)
    aioschedule.every().sunday.at("03:20").do(send_laters)
    
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())

# Запускаем бота
if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
    
