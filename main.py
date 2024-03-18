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
import sqlite3 as sq

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


async def irg_generate(name,password):
    sub_level = await db_get_data(name,password)
    wordlist = await db_update_wordlist(name, password,'-',0)

    # print(f'Проверка числа в генераторе {sub_level[3]},{sub_level[4]} += Проверка данныз из wordlist: {wordlist}')
    if sub_level[3] > 15:
        r = random.randint(sub_level[3]-15, sub_level[3])
        if hsk[r]["hanzi"] not in wordlist.values():
            a = hsk[r]["hanzi"]
            b = hsk[r]["pinyin"]
            c = hsk[r]["translations"]["rus"][0]
            db_update_hanzi(a,b,name,password)
            print('Работает sub_level')
            return [a, b, c]
        else:
            return await irg_generate(name,password)
    else:
        r = random.randint(0, sub_level[3])
        if hsk[r]["hanzi"] not in wordlist.values():
            a = hsk[r]["hanzi"]
            b = hsk[r]["pinyin"]
            c = hsk[r]["translations"]["rus"][0]
            db_update_hanzi(a,b,name,password)
            print('Работает else')
            return [a, b, c]
        else:
            return await irg_generate(name,password)



async def db_create(): # Создание базы
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50), level int(1), sub_level int(4), progress int(5), streak int(8), hanzi varchar(50), pinyin varchar(50))")
    conn.commit()
    cur.close()
    conn.close()

    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS wordlist(id int auto_increment primary key, name varchar(50), pass varchar(50), hanzi varchar(100))")
    conn.commit()
    cur.close()
    conn.close()


async def db_insert_user(name, password): # Заведение нового пользователя
    name = name
    password = password
    level = 1
    sub_level = 10
    progress = 0 
    streak = 0
    hanzi = '-'
    pinyin = '-'

    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name,pass,level,sub_level,progress,streak,hanzi,pinyin) VALUES ('%s', '%s', '%i', '%i', '%i', '%i', '%s', '%s')" %(name,password,level,sub_level,progress,streak,hanzi,pinyin))
    conn.commit()
    cur.close()
    conn.close()

async def db_insert_wordlist(name, password): # Заведение новой таблицы слов
    name = name
    password = password
    hanzi = {0:'-'}
    hanzi_json = json.dumps(hanzi)
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("INSERT INTO wordlist(name,pass,hanzi) VALUES ('%s', '%s', '%s')" %(name,password,hanzi_json))
    conn.commit()
    cur.close()
    conn.close()


async def db_get_data(name, password):
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("SELECT name,pass,level,sub_level,progress,streak,hanzi,pinyin FROM users WHERE name='%s' AND pass='%s'" %(name,password))
    users = cur.fetchall()
    cur.close()
    conn.close()
    # print('Get data ==-')
    return users[0]


async def db_update_data(name,password,level,sub_level,progress,streak):
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("UPDATE users SET level = '%s',sub_level = '%s',progress = '%s',streak = '%s' WHERE name='%s' AND pass='%s'" %(level,sub_level,progress,streak,name,password))
    conn.commit()
    cur.close()
    conn.close()
    # print('Update data ==-')


def db_update_hanzi(hanzi,pinyin,name,password): # 
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("UPDATE users SET hanzi = '%s',pinyin = '%s' WHERE name='%s' AND pass='%s'" %(hanzi,pinyin,name,password))
    conn.commit()
    cur.close()
    conn.close()
    # print('Update hanzi ==-')


    # Добавить режимы "добавить", "удалить" 
async def db_update_wordlist(name,password,hanzi,func_mode):
    # Отдаёт готовый список значений
    if func_mode == 0:
        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("SELECT hanzi FROM wordlist WHERE name='%s' AND pass='%s'" %(name,password))
        user_wordlist_json = cur.fetchall()
        cur.close()
        conn.close()

        hanzi_list = json.loads(user_wordlist_json[0][0])
        return hanzi_list
    
    # Добавляет новое слово в вордлист
    elif func_mode == 1:
        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("SELECT hanzi FROM wordlist WHERE name='%s' AND pass='%s'" %(name,password))
        user_wordlist_json = cur.fetchall()
        cur.close()
        conn.close()

        # print(f"JSON -- {user_wordlist_json[0][0]}")

        hanzi_list = json.loads(user_wordlist_json[0][0]) # Распаковать из json
        hanzi_list[len(hanzi_list)] = hanzi
        # print(f"NO JSON -- {hanzi_list}")
        json_hanzi = json.dumps(hanzi_list) # Упаковать в json

        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("UPDATE wordlist SET hanzi = '%s' WHERE name='%s' AND pass='%s'" %(json_hanzi,name,password))
        conn.commit()
        cur.close()
        conn.close()
        return f"Слово {hanzi} добавлено в словарь."
    
    # Удаляет слово из wordlist
    elif func_mode == -1:
        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("SELECT hanzi FROM wordlist WHERE name='%s' AND pass='%s'" %(name,password))
        user_wordlist_json = cur.fetchall()
        cur.close()
        conn.close()

        # print(f"JSON -- {user_wordlist_json[0][0]}")
        hanzi_list = json.loads(user_wordlist_json[0][0]) # Распаковать из json

        new_list = dict()
        for i in hanzi_list:
            if i == 0 and hanzi_list[i] != hanzi: 
                print(i,' >> ',hanzi_list[i],' >> ',hanzi)
                new_list[len(new_list)] = hanzi_list[i]

            if hanzi_list[i] != hanzi:
                print(i,' => ',hanzi_list[i],' => ',hanzi)
                new_list[len(new_list)] = hanzi_list[i]

        # print(f"NO JSON -- {new_list}")
        
        json_hanzi = json.dumps(new_list) # Упаковать в json

        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("UPDATE wordlist SET hanzi = '%s' WHERE name='%s' AND pass='%s'" %(json_hanzi,name,password))
        conn.commit()
        cur.close()
        conn.close()
        return f"Слово {hanzi} удалено из словаря."



class ChiStatus(StatesGroup):
    CHI_ON = State()
    CHI_OFF = State()



async def sub_level(name,password,count):
    user_data = await db_get_data(name,password)
    diff = user_data[3] + count
    
    if diff == 5000:
        level = 7
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'HSK 6 завершен. Поздравляю, мне больше нечему вас учить.'
    
    elif diff == 2500:
        level = 6
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'Открыт HSK 6. Вы на пути к вершине мастерства.'
    
    elif diff == 1200:
        level = 5
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'Открыт HSK 5. Ваш путь к верщине начинается здесь.'

    elif diff == 599:
        level = 4
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'Вы переходите на HSK 4. Ваше упорство поражает.'

    elif diff == 300:
        level = 3
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'HSK 2 взят, добро пожаловать в HSK 3. Поздравляю!'

    elif diff == 150:
        level = 2
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'HSK 1 позади, поздравляю!'
    
    elif count == 1:
        await db_update_data(name,password,user_data[2],diff,user_data[4],user_data[5])
        return 'Вы открыли новое слово!'
    
    elif count == -1:
        await db_update_data(name,password,user_data[2],diff,user_data[4],user_data[5])
        return 'Одно из новых слов стало недоступно.'
    
    elif count == 0:
        await db_update_data(name,password,user_data[2],diff,user_data[4],user_data[5])
        return "Я не могу опустить уровень ещё ниже 😅, пожалуйста пробуй с тем что есть)"



async def progress(name,password,count):
    user_data = await db_get_data(name,password)
    diff = user_data[4] + count

    if diff >= 5:
        diff = 0
        await db_update_data(name,password,user_data[2],user_data[3],diff,user_data[5])
        return await sub_level(name,password,1)

    elif diff <= -5:
        diff = 0
        if user_data[3] <= 10:
            await db_update_data(name,password,user_data[2],user_data[3],diff,user_data[5])
            return await sub_level(name,password,0)
        else:
            await db_update_data(name,password,user_data[2],user_data[3],diff,user_data[5])
            return await sub_level(name,password,-1)

    else:
        await db_update_data(name,password,user_data[2],user_data[3],diff,user_data[5])
        return count


async def streak(name,password,count):
    user_data = await db_get_data(name,password)
    print(f'Получение данынх в стрике: {user_data}')
    diff = user_data[5] + count

    if diff >= 10:
        diff = 0
        await db_update_data(name,password,user_data[2],user_data[3],user_data[4],diff)
        return await progress(name,password,1)

    elif diff <= -10:
        diff = 0
        await db_update_data(name,password,user_data[2],user_data[3],user_data[4],diff)
        return await progress(name,password,-1)
    
    else:
        await db_update_data(name,password,user_data[2],user_data[3],user_data[4],diff)
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
    await db_update_data(message.from_user.username, message.chat.id, level, sub_level, progress, streak)
    await message.answer(f"Уровень изменён:\nlevel : {level}\nsub_level: {sub_level}\nprogress: {progress}\nstreak: {streak}")



@dp.message(Command("chi"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(f"Рад тебя видеть здесь, <b>{message.from_user.first_name}</b> :3")

    # Проверить наличие бд, если бд нет - создать, если есть - идём дальше
    await db_create()
    
    try:
        await db_get_data(message.from_user.username, message.chat.id)
    except:
        await db_insert_user(message.from_user.username, message.chat.id)


    try:
        await db_update_wordlist(message.from_user.username, message.chat.id, "-", 0)
    except:
        await db_insert_wordlist(message.from_user.username, message.chat.id)
    

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

    print(f'Начало работы, дб_гет: {await db_get_data(callback.from_user.username, callback.from_user.id)}')
    # print(f"{callback.from_user.username} === И === {callback.from_user.id}")

    hanzi = await irg_generate(callback.from_user.username, callback.from_user.id)
    await callback.message.answer(f"Напиши пиньинь ироглифа:\n{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
    await state.set_state(ChiStatus.CHI_ON)
    await callback.answer(
        text="Вводи кандзи вида ‘爱’ через пиньинь.\n\nЕсли забыл - нажми на спойлер, чтобы подсмотреть.\n\nКаждый правильный ответ даёт тебе +1 балл, каждый неправильный отнимает -1.\n\nУспехов!",
        show_alert=True
    )

@dp.message(ChiStatus.CHI_ON, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    user_data = await db_get_data(message.from_user.username, message.chat.id)
    
    if message.text.lower() == user_data[6]:
        answer = await streak(message.from_user.username, message.chat.id,1)
        if answer == 1:
            print('Стрик увеличен')
        else:
            await message.answer(f'{answer}')

        hanzi = await irg_generate(message.from_user.username, message.chat.id)
        await message.answer(f"{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
        
    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.CHI_OFF)
        await message.answer(f"Игра завершена, возвращайся ещё:3")

    elif message.text.lower() == '/status':
        user_data = await db_get_data(message.from_user.username, message.chat.id)
        print(user_data)
        await message.answer(f"{user_data[0]}-{user_data[1]}\n\nТекущий уровень: {user_data[2]}\nУровень открытых слов: {user_data[3]}\nПрогресс: {user_data[4]}\nДействующий стрик: {user_data[5]}")
        await message.answer(f"Если хочешь посмотреть скрытые слова, набери:\n/wordlist\n\nЕсли хочешь скрыть слово из генератора:\n/skip\n\nЕсли хочешь вернуть слово:\n/restore [хандзи]")

    elif message.text.lower() == '/wordlist':
        wordlist = await db_update_wordlist(message.from_user.username, message.chat.id,'-',0)
        await message.answer(', '.join(wordlist.values()))

    elif message.text.lower() == '/skip':
        user_data = await db_get_data(message.from_user.username, message.chat.id)
        wordlist = await db_update_wordlist(message.from_user.username, message.chat.id,user_data[6],1)
        await message.answer(f"Кандзи {user_data[6]} успешно скрыто :3")

        hanzi = await irg_generate(message.from_user.username, message.chat.id)
        await message.answer(f"{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
    
    elif '/restore' in message.text.lower():
        user_data = await db_get_data(message.from_user.username, message.chat.id)
        wordlist = await db_update_wordlist(message.from_user.username, message.chat.id,user_data[6],1)

        split_message = message.text.lower().split(' ', maxsplit=1)
        await db_update_wordlist(message.from_user.username, message.chat.id, split_message[1], -1)
        await message.answer(f"Кандзи {split_message[1]} успешно восстановлено :3")

        hanzi = await irg_generate(message.from_user.username, message.chat.id)
        await message.answer(f"{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")

    else:
        if await streak(message.from_user.username, message.chat.id,-1) == -1:
            print('Стрик уменьшен')
        await message.answer(f"Не верно, {user_data[7]}")



# @dp.message(ChiStatus.CHI_ON, Command("restore"))
# async def set_user_status(message: Message,command: CommandObject):
#     if command.args is None:
#         await message.answer("Ошибка: не переданы аргументы")
#         return
    
#     try:
#         hanzi = command.args

#     except ValueError:
#         await message.answer(
#             "Ошибка: неправильный формат команды. Пример:\n"
#             "/restore hanzi\n"
#             "/restore 爱"
#         )
#         return
#     word = await db_update_wordlist(message.from_user.username, message.chat.id, hanzi, -1)
#     await message.answer(f"Слово {hanzi} восстановлено и доступно для повторения")



@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(f"На данный момент доступна только одна игра: CHI\n\nЧтобы поиграть в неё, тебе нужно установить китайскую расскладку клавиатуры 'Пиньинь - упрощённый'\n\n После этого набирай /chi для старта :3")



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
