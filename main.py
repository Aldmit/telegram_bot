import asyncio
import logging
import os
import random
import json

from aiogram import html
from aiogram import Bot, Dispatcher, types
from aiogram import F # магические функции - позволяют вытаскивать всю нужную инфу с минимумом кода

from aiogram.enums import ContentType # Позволяет уточнять и проверять получаемый контент
from aiogram.filters.command import Command, CommandObject, CommandStart # Позволяет ловить команды в обработчик по схеме Command('команда')
from aiogram.utils.formatting import Text, Bold
from aiogram.types import Message,MessageEntity,FSInputFile, URLInputFile, BufferedInputFile, InputTextMessageContent, InlineQueryResultArticle # Работа с файлами
from aiogram.utils.keyboard import ReplyKeyboardBuilder # Подстрочные кнопки
from aiogram.utils.keyboard import InlineKeyboardBuilder # Инлайновые кнопки

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from contextlib import suppress # Помогает отлавливать ошибки при работе с пользовательскими данными
from aiogram.exceptions import TelegramBadRequest # Позволяет обращатся к БадРеквестам и отрабатывать исключения

from typing import Optional
from aiogram.filters.callback_data import CallbackData # Добавляет объект для удобной работы и разбора каллбеков в айограме

import os
import sqlite3

from config import Config, load_config


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

config: Config = load_config()
BOT_TOKEN: str = config.bot.token

# Объект бота
bot = Bot(BOT_TOKEN, parse_mode="HTML")
# Диспетчер
dp = Dispatcher()

path = os.path.dirname(
    os.path.abspath(__file__)
)  # Отправка файлов пользователю картинка, музыка, видео
file = open(f"{path}/hsk.json", "rb")
hsk = json.load(file)  # Разбираем полученные JSON данные в читабельный формат
hanzi = ["爱", "ai", "любовь"]


async def irg_generate():
    sub_level = await db_get_data()
    print(f'Проверка числа в генераторе {sub_level[3]},{sub_level[4]}')
    if sub_level[3] > 15:
        r = random.randint(sub_level[3]-15, sub_level[3])
        a = hsk[r]["hanzi"]
        b = hsk[r]["pinyin"]
        c = hsk[r]["translations"]["rus"][0]
        db_update_hanzi(a,b)
        print('Работает sub_level')
        return [a, b, c]
    else:
        r = random.randint(0, sub_level[3])
        a = hsk[r]["hanzi"]
        b = hsk[r]["pinyin"]
        c = hsk[r]["translations"]["rus"][0]
        db_update_hanzi(a,b)
        print('Работает else')
        return [a, b, c]



async def db_create(): # Создание базы
    conn = sqlite3.connect("database.sql") # Работа с подключением к БД через встроенный import sqlite3
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50), level int(1), sub_level int(4), progress int(5), streak int(8), hanzi varchar(50), pinyin varchar(50))")
    conn.commit()
    cur.close()
    conn.close()


async def db_insert_user(name, password): # Заведение нового пользователя
    name = 'Aldmit'
    password = '1234'
    level = 1
    sub_level = 10
    progress = 0 
    streak = 0
    hanzi = '-'
    pinyin = '-'

    conn = sqlite3.connect("database.sql") # Работа с подключением к БД через встроенный import sqlite3
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name,pass,level,sub_level,progress,streak,hanzi,pinyin) VALUES ('%s', '%s', '%i', '%i', '%i', '%i', '%s', '%s')" %(name,password,level,sub_level,progress,streak,hanzi,pinyin))
    conn.commit()
    cur.close()
    conn.close()


async def db_get_data():
    conn = sqlite3.connect("database.sql") # Работа с подключением к БД через встроенный import sqlite3
    cur = conn.cursor()
    cur.execute("SELECT name,pass,level,sub_level,progress,streak,hanzi,pinyin FROM users WHERE name='Aldmit'")
    users = cur.fetchall()
    cur.close()
    conn.close()
    # print('Get data ==-')
    # print(users)
    return users[0]


async def db_update_data(name,password,level,sub_level,progress,streak):
    conn = sqlite3.connect("database.sql") # Работа с подключением к БД через встроенный import sqlite3
    cur = conn.cursor()
    cur.execute("UPDATE users SET level = '%s',sub_level = '%s',progress = '%s',streak = '%s' WHERE name='Aldmit'" %(level,sub_level,progress,streak))
    conn.commit()
    cur.close()
    conn.close()
    # print('Update data ==-')


def db_update_hanzi(hanzi,pinyin): # 
    conn = sqlite3.connect("database.sql") # Работа с подключением к БД через встроенный import sqlite3
    cur = conn.cursor()
    cur.execute("UPDATE users SET hanzi = '%s',pinyin = '%s' WHERE name='Aldmit'" %(hanzi,pinyin))
    conn.commit()
    cur.close()
    conn.close()
    # print('Update hanzi ==-')


class ChiStatus(StatesGroup):
    CHI_ON = State()
    CHI_OFF = State()



async def sub_level(name,password,count):
    user_data = await db_get_data()
    diff = user_data[3] + count
    
    if diff == 5000:
        level = 7
        await db_update_data('Aldmit','1234',level,diff,user_data[4],user_data[5])
        return 'HSK 6 завершен. Поздравляю, мне больше нечему вас учить.'
    
    elif diff == 2500:
        level = 6
        await db_update_data('Aldmit','1234',level,diff,user_data[4],user_data[5])
        return 'Открыт HSK 6. Вы на пути к вершине мастерства.'
    
    elif diff == 1200:
        level = 5
        await db_update_data('Aldmit','1234',level,diff,user_data[4],user_data[5])
        return 'Открыт HSK 5. Ваш путь к верщине начинается здесь.'

    elif diff == 599:
        level = 4
        await db_update_data('Aldmit','1234',level,diff,user_data[4],user_data[5])
        return 'Вы переходите на HSK 4. Ваше упорство поражает.'

    elif diff == 300:
        level = 3
        await db_update_data('Aldmit','1234',level,diff,user_data[4],user_data[5])
        return 'HSK 2 взят, добро пожаловать в HSK 3. Поздравляю!'

    elif diff == 150:
        level = 2
        await db_update_data('Aldmit','1234',level,diff,user_data[4],user_data[5])
        return 'HSK 1 позади, поздравляю!'
    
    elif count == 1:
        await db_update_data('Aldmit','1234',user_data[2],diff,user_data[4],user_data[5])
        return 'Вы открыли новое слово!'
    
    elif count == -1:
        await db_update_data('Aldmit','1234',user_data[2],diff,user_data[4],user_data[5])
        return 'Одно из новых слов стало недоступно.'
    
    elif count == 0:
        await db_update_data('Aldmit','1234',user_data[2],diff,user_data[4],user_data[5])
        return "Я не могу опустить уровень ещё ниже 😅, пожалуйста пробуй с тем что есть)"



async def progress(name,password,count):
    user_data = await db_get_data()
    diff = user_data[4] + count

    if diff >= 5:
        diff = 0
        await db_update_data('Aldmit','1234',user_data[2],user_data[3],diff,user_data[5])
        return await sub_level('Aldmit','1234',1)

    elif diff <= -5:
        diff = 0
        if user_data[3] <= 10:
            await db_update_data('Aldmit','1234',user_data[2],user_data[3],diff,user_data[5])
            return await sub_level('Aldmit','1234',0)
        else:
            await db_update_data('Aldmit','1234',user_data[2],user_data[3],diff,user_data[5])
            return await sub_level('Aldmit','1234',-1)

    else:
        await db_update_data('Aldmit','1234',user_data[2],user_data[3],diff,user_data[5])
        return count


async def streak(name,password,count):
    user_data = await db_get_data()
    print(f'Получение данынх в стрике: {user_data}')
    diff = user_data[5] + count

    if diff >= 10:
        diff = 0
        await db_update_data('Aldmit','1234',user_data[2],user_data[3],user_data[4],diff)
        return await progress('Aldmit','1234',1)

    elif diff <= -10:
        diff = 0
        await db_update_data('Aldmit','1234',user_data[2],user_data[3],user_data[4],diff)
        return await progress('Aldmit','1234',-1)
    
    else:
        await db_update_data('Aldmit','1234',user_data[2],user_data[3],user_data[4],diff)
        return count





async def start_bot(bot: Bot):
    print("\n\n🟢 Бот запущен\n\n\n")
async def stop_bot(bot: Bot):
    print("\n\n🔴 Бот остановлен\n\n\n")

dp.startup.register(start_bot)  # регистрируем в диспетчере функцию по запуску
dp.shutdown.register(stop_bot)  # регистрируем в диспетчере функцию по остановке



@dp.message(Command("set_status"))
async def set_user_status(message: Message,command: CommandObject):
    if command.args is None:
        await message.answer("Ошибка: не переданы аргументы")
        return
    
    try:
        level, sub_level, progress, streak = command.args.split(" ", maxsplit=3)

    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/set_status level sub_level progress streak\n"
            "/set_status 1 120 19 9"
        )
        return
    await db_update_data('Aldmit','1234', level, sub_level, progress, streak)
    await message.answer(f"Уровень изменён:\nlevel : {level}\nsub_level: {sub_level}\nprogress: {progress}\nstreak: {streak}")



@dp.message(Command("chi"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(f"Рад тебя видеть, <b>{message.from_user.first_name}</b> :3")

    # print(f'🫢🫢🫢',end="")
    # for i in message.chat:
    #     print(i)
    
    # print(f'\n🫢🫢🫢',end="")
    # for i in message.from_user:
    #     print(i)

    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(
            text="Начать игру", callback_data="chinese_train"
        )
    )
    await message.answer(
        "Добро пожаловать в CHI!\n\nПравила очень просты: чем больше правильных ответов даёшь, тем выше твой уровень, и тем больше новых слов тебе доступно.\n\nВо время игры доступны следующие базовые конманды:\n\n/exit - закончить\n/status - узнать текущий уровень\n\nГотов узнать сегодня новые слова?", reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "chinese_train")
async def send_chinese_train(callback: types.CallbackQuery, state: FSMContext):
    print(f'Начало работы, дб_гет: {await db_get_data()}')
    hanzi = await irg_generate()
    await callback.message.answer(f"Напиши пиньинь ироглифа:\n{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
    await state.set_state(ChiStatus.CHI_ON)
    await callback.answer(
        text="Вводи кандзи вида ‘爱’ через пиньинь.\n\nЕсли забыл - нажми на спойлер, чтобы подсмотреть.\n\nКаждый правильный ответ даёт тебе +1 бал, каждый неправильный отнимает -1.\n\nУспехов!",
        show_alert=True
    )

@dp.message(ChiStatus.CHI_ON, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    h = await db_get_data()
    print(h)
    if message.text.lower() == h[6]:
        answer = await streak('Aldmit','1234',1)
        if answer == 1:
            print('Стрик увеличен')
        else:
            await message.answer(f'{answer}')

        hanzi = await irg_generate()
        await message.answer(f"{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
        
    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.CHI_OFF)
        await message.answer(f"Тренировка завершена")

    elif message.text.lower() == '/status':
        user = await db_get_data()
        print(user)
        await message.answer(f"Текущий уровень: {user[2]}\nУровень открытых слов: {user[3]}\nПрогресс: {user[4]}\nДействующий стрик: {user[5]}")

    else:
        if await streak('Aldmit','1234',-1) == -1:
            print('Стрик уменьшен')
        await message.answer(f"Не верно, {h[7]}")





# Запуск процесса поллинга новых апдейтов
async def main():
    # await db_create()
    # await db_insert_user('Aldmit','1234')
    # print(await db_get_data())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())