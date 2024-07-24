
from aiogram import Bot, types
from aiogram import F # магические функции - позволяют вытаскивать всю нужную инфу с минимумом кода

from aiogram.filters.command import Command, CommandObject, CommandStart # Позволяет ловить команды в обработчик по схеме Command('команда')
from aiogram.types import Message,MessageEntity,FSInputFile, URLInputFile, BufferedInputFile, InputTextMessageContent, InlineQueryResultArticle # Работа с файлами

from aiogram.utils.keyboard import ReplyKeyboardBuilder # Подстрочные кнопки
from aiogram.utils.keyboard import InlineKeyboardBuilder # Инлайновые кнопки

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from ..db_functions import *
from ..word_generator import *
from ..level_system import *

# Было бы круто вынести обработчики каждой отдельной тренировки в отдельный файл, чтобы с этим было удобнее работать

from aiogram import Router

# Инициализируем роутер уровня модуля
router = Router()

# Состояния здесь нужны, чтобы понимать, какие из обработчиков слушать (у обработчиков могут быть одинакоые команды, но нам важно, какой у них при этом статус состояния)
class ChiStatus(StatesGroup):
    CHI_ON_1 = State()
    CHI_ON_2 = State()
    CHI_ON_3 = State()
    CHI_ON_4 = State()
    CHI_OFF = State()


@router.message(Command("chi"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer_sticker(r'CAACAgQAAxkBAAEL241mESWkgPb6zmSag044fXsFfVdnFQACQwcAAluO6VN4345BS4i5szQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
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
    
    try:
        await db_get_textgen(message.from_user.username, message.chat.id)
    except:
        await db_insert_textlist(message.from_user.username, message.chat.id)

    # print(f'🫢🫢🫢',end="")
    # for i in message.chat:
    #     print(i)
    
    # print(f'\n🫢🫢🫢',end="")
    # for i in message.from_user:
    #     print(i)


    # builder = InlineKeyboardBuilder()
    # builder.row(width=2).add(
    #     types.InlineKeyboardButton( 
    #         text="Учить 汉语", callback_data="chinese_train_1"
    #     ),types.InlineKeyboardButton(
    #         text="Различать слова", callback_data="chinese_train_2"
    #     ),types.InlineKeyboardButton(
    #         text="Повторять слова", callback_data="chinese_train_3"
    #     ),types.InlineKeyboardButton(
    #         text="Учить пиньинь", callback_data="chinese_train_4"
    #     )
    # )

    def get_keyboard():
        buttons = [
            [
                types.InlineKeyboardButton(text="Учить 汉语", callback_data="chinese_train_1"),
                types.InlineKeyboardButton(text="Различать слова", callback_data="chinese_train_2")
            ],
            [
                types.InlineKeyboardButton(text="Повторять слова", callback_data="chinese_train_3"),
                types.InlineKeyboardButton(text="Учить тона", callback_data="chinese_train_4")
            ],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
 
    await message.answer(
        "Добро пожаловать в CHI!\n\nПравила очень просты: чем больше правильных ответов даёшь, тем выше твой уровень, и тем больше новых слов тебе доступно.\n\nВо время игры доступны следующие базовые конманды:\n\n/exit - закончить\n/status - узнать текущий уровень\n\nГотов узнать сегодня новые слова?", reply_markup=get_keyboard()
    )


# ПЕРВЫЙ ТИП ТРЕНИРОВКИ

@router.callback_query(F.data == "chinese_train_1")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    hanzi = await irg_generate(callback.from_user.username, callback.from_user.id)
    
    await callback.message.answer(f"Напиши пиньинь ироглифа:\n{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
    await state.set_state(ChiStatus.CHI_ON_1)
    await callback.answer(
        text="Вводи кандзи вида ‘爱’ через пиньинь.\n\nЕсли забыл - нажми на спойлер, чтобы подсмотреть.\n\nКаждый правильный ответ даёт тебе +1 балл, каждый неправильный отнимает -1.\n\nУспехов!",
        show_alert=True
    )

@router.message(ChiStatus.CHI_ON_1, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    user_data = await db_get_data(message.from_user.username, message.chat.id)
    
    if message.text.lower() == user_data[6]:
        answer = await streak(message.from_user.username, message.chat.id,1)

        if answer == 1:
            print('Стрик увеличен')
        else:
            if answer == 'Вы открыли новое слово!':
                await message.answer_sticker(r'CAACAgQAAxkBAAEL25ZmESgcK74UZ2GXiTRtOOXQLxtkwQACigkAAqDU6VPBDJvf9u5l1jQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее

            elif answer == 'HSK 1 позади, поздравляю!':
                await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее

            elif answer == 'HSK 2 взят, добро пожаловать в HSK 3. Поздравляю!':
                await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
            
            elif answer == 'HSK 3 взят, можешь смело переходить к HSK 4. Это большое достижение!':
                await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
    

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
        await message.answer(f"Команды работы со словарём:\n/wordlist – скрытые слова\n/skip – скрыть слово\n/restore [хандзи] – вернуть слово")

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
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return

            wordlist = await db_update_wordlist(message.from_user.username, message.chat.id,'-',0)
            list_with_words = ', '.join(wordlist.values())
            if split_message[1] not in list_with_words:
                await message.answer(
                    "Ошибка: в вордлисте слова нет. Проверьте правильность слова:\n"
                    "/restore [hanzi]\n"
                    "/restore 爱"
                )
                return
        except:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/restore hanzi\n"
                "/restore 爱"
            )
            return
        await db_update_wordlist(message.from_user.username, message.chat.id, split_message[1], -1)
        
        await message.answer(f"Кандзи {split_message[1]} успешно восстановлено и доступно для повторения :3")

        # hanzi = await irg_generate(message.from_user.username, message.chat.id)
        # await message.answer(f"{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
        
    # Получение информации об иероглифе
    elif '/info' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return
        
            answer = await get_hanzi_info(split_message[1])
            await message.answer(f'{answer[0]} -> {answer[1]} -> {answer[2]}')

        except:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/info hanzi\n"
                "/info 爱"
            )
            return
        
    else:
        if await streak(message.from_user.username, message.chat.id,-1) == -1:
            print('Стрик уменьшен')
        await message.answer(f"Не верно, {user_data[7]}")



@router.message(ChiStatus.CHI_ON_1, F)
async def free_user_text(message: types.Message, bot: Bot, state: FSMContext):
        print(f'\n🫢🫢🫢',end="")
        for i in message.from_user:
            print(i)

        print(F.sti)






# @router.message(ChiStatus.CHI_ON, Command("restore"))
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







# ВТОРОЙ ТИП ТРЕНИРОВКИ

@router.callback_query(F.data == "chinese_train_2")
async def start_chinese_train_2(callback: types.CallbackQuery, state: FSMContext):

    a = await db_update_textlist(callback.from_user.username, callback.from_user.id)

    await callback.message.answer(f"{(await db_get_textgen(callback.from_user.username, callback.from_user.id)).replace(',', '')}")
    
    await state.set_state(ChiStatus.CHI_ON_2)
    await callback.answer(
        text="Перед тобой случайный китайский текст из иероглифов, которые ты уже знаешь. Перепиши его, чтобы закрепить своё знание.\n\nУспехов!",
        show_alert=True
    )


@router.message(ChiStatus.CHI_ON_2, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    text_gen = await db_get_textgen(message.from_user.username, message.chat.id)
    text_gen = text_gen.replace(',','')

    if message.text.lower() == text_gen:
        await db_update_textlist(message.from_user.username, message.chat.id)
        await message.answer(f"{(await db_get_textgen(message.from_user.username, message.chat.id)).replace(',', '')}")

        
    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.CHI_OFF)
        await message.answer(f"Игра завершена, возвращайся ещё:3")

    # Получение информации об иероглифе
    elif '/info' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return
        
            answer = await get_hanzi_info(split_message[1])
            await message.answer(f'{answer[0]} -> {answer[1]} -> {answer[2]}')

        except:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/info hanzi\n"
                "/info 爱"
            )
            return
        
    # Показывает список выученных пользователем слов
    elif message.text.lower() == '/wordlist':
        wordlist = await db_update_wordlist(message.from_user.username, message.chat.id,'-',0)
        await message.answer(', '.join(wordlist.values()))

    # Восстанавливает слово в режиме обучения из режима практики
    elif '/restore' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return

            wordlist = await db_update_wordlist(message.from_user.username, message.chat.id,'-',0)
            list_with_words = ', '.join(wordlist.values())
            if split_message[1] not in list_with_words:
                await message.answer(
                    "Ошибка: в вордлисте слова нет. Проверьте правильность слова:\n"
                    "/restore [hanzi]\n"
                    "/restore 爱"
                )
                return
        except:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/restore hanzi\n"
                "/restore 爱"
            )
            return
       
        await db_update_wordlist(message.from_user.username, message.chat.id, split_message[1], -1)
        
        await message.answer(f"Кандзи {split_message[1]} успешно восстановлено и доступно для повторения :3")

        # hanzi = await irg_generate(message.from_user.username, message.chat.id)
        # await message.answer(f"{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
        
    else:
        answer = list()
        user_message = ""
        i = 0

        got_hanzi_text = (await db_get_textgen(message.from_user.username, message.chat.id)).split(',')

        while i < len(got_hanzi_text):
            answer = await get_hanzi_info(got_hanzi_text[i])
            user_message += f"▫ {answer[0]} > {answer[1]} > {answer[2]}\n"
            i +=1

        await message.answer(f"Не верно, попробуй ещё раз:3\n\n= = = Подсказка = = =\n{user_message}")






# ТРЕТИЙ ТИП ТРЕНИРОВКИ

@router.callback_query(F.data == "chinese_train_3")
async def start_chinese_train_3(callback: types.CallbackQuery, state: FSMContext):
    hanzi = await irg_generate(callback.from_user.username, callback.from_user.id,"off")
    
    await callback.message.answer(f"Введи кандзи:\n{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
    await state.set_state(ChiStatus.CHI_ON_3)
    await callback.answer(
        text="Повтори выученные ранее слова!\n\nВводи кандзи вида ‘爱’ через пиньинь.\n\nЕсли забыл - нажми на спойлер, чтобы подсмотреть.\n\nСтань ещё ближе к мечте)",
        show_alert=True
    )

@router.message(ChiStatus.CHI_ON_3, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    user_data = await db_get_data(message.from_user.username, message.chat.id)
    
    if message.text.lower() == user_data[6]:

        hanzi = await irg_generate(message.from_user.username, message.chat.id, "off")
        await message.answer(f"{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
        


    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.CHI_OFF)
        await message.answer(f"Игра завершена, возвращайся ещё:3")

    elif message.text.lower() == '/status':
        user_data = await db_get_data(message.from_user.username, message.chat.id)
        print(user_data)
        await message.answer(f"{user_data[0]}-{user_data[1]}\n\nТекущий уровень: {user_data[2]}\nУровень открытых слов: {user_data[3]}\nПрогресс: {user_data[4]}\nДействующий стрик: {user_data[5]}")
        await message.answer(f"Команды работы со словарём:\n/wordlist – скрытые слова\n/skip – скрыть слово\n/restore [хандзи] – вернуть слово")

    elif message.text.lower() == '/wordlist':
        wordlist = await db_update_wordlist(message.from_user.username, message.chat.id,'-',0)
        await message.answer(', '.join(wordlist.values()))
    
    # Получение информации об иероглифе
    elif '/info' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return
        
            answer = await get_hanzi_info(split_message[1])
            await message.answer(f'{answer[0]} -> {answer[1]} -> {answer[2]}')

        except:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/info hanzi\n"
                "/info 爱"
            )
            return
        
    else:
        await message.answer(f"Не верно, {user_data[7]}")



@router.message(ChiStatus.CHI_ON_3, F)
async def free_user_text(message: types.Message, bot: Bot, state: FSMContext):
        print(f'\n🫢🫢🫢',end="")
        for i in message.from_user:
            print(i)

        print(F.sti)




# ЧЕТВЁРТЫЙ ТИП ТРЕНИРОВКИ

@router.callback_query(F.data == "chinese_train_4")
async def start_chinese_train_4(callback: types.CallbackQuery, state: FSMContext):
    hanzi = await irg_generate(callback.from_user.username, callback.from_user.id,"off")
    
    await callback.message.answer(f"Введи пиньинь ироглифа:\n{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
    await state.set_state(ChiStatus.CHI_ON_4)
    await callback.answer(
        text="Вводи пиньинь вида [huǒ chē zhàn] с тонами.\n\nИспользуй открытые иероглиф и перевод.\n\nЕсли забыл - нажми на спойлер, чтобы подсмотреть.\n\n\n\nБудь терпелив)",
        show_alert=True
    )

@router.message(ChiStatus.CHI_ON_4, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    user_data = await db_get_data(message.from_user.username, message.chat.id)
    
    if message.text.lower() == user_data[7]:

        hanzi = await irg_generate(message.from_user.username, message.chat.id, "off")
        await message.answer(f"{hanzi[0]} - <tg-spoiler>{hanzi[1]}</tg-spoiler> - {hanzi[2]}\n")
        


    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.CHI_OFF)
        await message.answer(f"Игра завершена, возвращайся ещё:3")

    elif message.text.lower() == '/status':
        user_data = await db_get_data(message.from_user.username, message.chat.id)
        print(user_data)
        await message.answer(f"{user_data[0]}-{user_data[1]}\n\nТекущий уровень: {user_data[2]}\nУровень открытых слов: {user_data[3]}\nПрогресс: {user_data[4]}\nДействующий стрик: {user_data[5]}")
        await message.answer(f"Команды работы со словарём:\n/wordlist – скрытые слова\n/skip – скрыть слово\n/restore [хандзи] – вернуть слово")

    elif message.text.lower() == '/wordlist':
        wordlist = await db_update_wordlist(message.from_user.username, message.chat.id,'-',0)
        await message.answer(', '.join(wordlist.values()))
    
    # Получение информации об иероглифе
    elif '/info' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return
        
            answer = await get_hanzi_info(split_message[1])
            await message.answer(f'{answer[0]} -> {answer[1]} -> {answer[2]}')

        except:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/info hanzi\n"
                "/info 爱"
            )
            return
        
    else:
        await message.answer(f"Не верно, {user_data[7]}")



@router.message(ChiStatus.CHI_ON_4, F)
async def free_user_text(message: types.Message, bot: Bot, state: FSMContext):
        print(f'\n🫢🫢🫢',end="")
        for i in message.from_user:
            print(i)

        print(F.sti)



@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(f"На данный момент доступна только одна игра: CHI\n\nЧтобы поиграть в неё, тебе нужно установить китайскую расскладку клавиатуры 'Пиньинь - упрощённый'\n\n После этого набирай /chi для старта :3")




