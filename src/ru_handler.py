from aiogram import Bot, types
from aiogram import F # магические функции - позволяют вытаскивать всю нужную инфу с минимумом кода

from aiogram.filters.command import Command, CommandObject, CommandStart # Позволяет ловить команды в обработчик по схеме Command('команда')
from aiogram.types import Message,MessageEntity,FSInputFile, URLInputFile, BufferedInputFile, InputTextMessageContent, InlineQueryResultArticle # Работа с файлами
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.utils.keyboard import ReplyKeyboardBuilder # Подстрочные кнопки
from aiogram.utils.keyboard import InlineKeyboardBuilder # Инлайновые кнопки

from aiogram import Router

from .database import *
from .user import *
from .level_system_controller import *
from .dictionary import *

# Инициализируем роутер уровня модуля
router = Router()


# Состояния здесь нужны, чтобы понимать, какие из обработчиков слушать (у обработчиков могут быть одинакоые команды, но нам важно, какой у них при этом статус состояния)
class ChiStatus(StatesGroup):
    MAO_ON_RU__0 = State()
    MAO_ON_RU__1 = State()
    MAO_ON_RU__2 = State()
    MAO_ON_RU__3 = State()
    MAO_ON_RU__4 = State()
    MAO_OFF = State()


@router.message(Command("mao"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer_sticker(r'CAACAgQAAxkBAAEL241mESWkgPb6zmSag044fXsFfVdnFQACQwcAAluO6VN4345BS4i5szQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
    await message.answer(f"Рад тебя видеть здесь, <b>{message.from_user.first_name}</b> :3")
    await state.set_state(ChiStatus.MAO_ON_RU__0)
    User(message.chat.id).set_language('ru') 

    flag = User(message.chat.id).checking_existing_user()

    if flag == True:
        def get_keyboard():
                buttons = [
                    [types.InlineKeyboardButton(text="Учить 汉语(hanyu)", callback_data="chinese_train_1")],
                    [types.InlineKeyboardButton(text="Повторять слова", callback_data="chinese_train_2")],
                    [types.InlineKeyboardButton(text="Загрузить свой список", callback_data="chinese_train_3")],
                    [ types.InlineKeyboardButton(text="Учить свои слова", callback_data="chinese_train_4")]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                return keyboard
    else:
        def get_keyboard():
                buttons = [
                    [types.InlineKeyboardButton(text="Учить 汉语(hanyu)", callback_data="chinese_train_1")],
                    [types.InlineKeyboardButton(text="Загрузить свой список", callback_data="chinese_train_3")]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                return keyboard

    await message.answer(
        "Добро пожаловать в CHI!\n\nПравила очень просты: чем больше правильных ответов даёшь, тем выше твой уровень, и тем больше новых слов тебе доступно.\n\nВо время игры доступны следующие базовые конманды:\n\n/exit - закончить\n/status - узнать текущий уровень\n\nГотов узнать сегодня новые слова?", reply_markup=get_keyboard()
    )


# ПЕРВЫЙ РЕЖИМ РАБОТЫ

@router.callback_query(F.data == "chinese_train_1")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):

    word = WordGenerator(callback.from_user.id).get_random_word()
    
    await callback.message.answer(f"Напиши пиньинь ироглифа:\n{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler> - {word[2]}\n")
    await state.set_state(ChiStatus.MAO_ON_RU__1)
    await callback.answer(
        text="Вводи кандзи вида ‘爱’ через пиньинь.\n\nЕсли забыл - нажми на спойлер, чтобы подсмотреть.\n\nКаждый правильный ответ даёт тебе +1 балл, каждый неправильный отнимает -1.\n\nУспехов!",
        show_alert=True
    )

@router.message(ChiStatus.MAO_ON_RU__1, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    word = User(message.chat.id)._data.get_data('word')

    if message.text.lower() == word['word']:
        answer = LevelSystemController(message.chat.id).streak(1)

        if answer == 1:
            print('Стрик увеличен')
        else:
            if answer == 'Вы открыли новое слово!':
                await message.answer_sticker(r'CAACAgQAAxkBAAEL25ZmESgcK74UZ2GXiTRtOOXQLxtkwQACigkAAqDU6VPBDJvf9u5l1jQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
                
                user_data = User(message.chat.id)._data.get_data(User(message.chat.id)._language+"_settings")
                new_word = WordGenerator(message.chat.id).get_word_by_index(user_data['sub-level']+1)
                answer += "\n" + new_word.zh + " - " + new_word.py + " - " + new_word.translate['ru']

            elif answer == 'HSK 1 позади, поздравляю!':
                await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее

            elif answer == 'HSK 2 взят, добро пожаловать в HSK 3. Поздравляю!':
                await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
            
            elif answer == 'HSK 3 взят, можешь смело переходить к HSK 4. Это большое достижение!':
                await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
            
            elif answer == 'HSK 3 взят, можешь смело переходить к HSK 4. Это большое достижение!':
                await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
    

            await message.answer(f'{answer}')

        word = WordGenerator(message.chat.id).get_random_word()
        await message.answer(f"{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler> - {word[2]}\n")
        
        

    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.MAO_OFF)
        await message.answer(f"Игра завершена, возвращайся ещё:3")


    elif message.text.lower() == '/status':
        user_data = User(message.chat.id)._data.get_data(User(message.chat.id)._language+"_settings")
        await message.answer(f"@{message.chat.username}-{message.chat.id}\n\nТекущий уровень: {user_data['level']}\nУровень открытых слов: {user_data['sub-level']}\nПрогресс: {user_data['progress']}\nДействующий стрик: {user_data['streak']}")
        await message.answer(f"Команды работы со словарём:\n/wordlist – скрытые слова\n/skip – скрыть слово\n/restore [хандзи] – вернуть слово")


    elif message.text.lower() == '/wordlist':
        wordlist = User(message.chat.id).update_wordlist(0,'-',User(message.chat.id)._language)
        await message.answer(f"{', '.join(wordlist.values())} \n\nВсего ты добавил: {len(wordlist.values())-1}")


    elif message.text.lower() == '/skip':
        word = User(message.chat.id)._data.get_data('word')
        wordlist = User(message.chat.id).update_wordlist(1,word['word'],User(message.chat.id)._language)
        await message.answer(f"{wordlist}")
        # await message.answer(f"Кандзи {word['word']} успешно скрыто :3")

        word = WordGenerator(message.chat.id).get_random_word()
        await message.answer(f"{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler> - {word[2]}\n")
    

    elif '/restore' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return

            wordlist = User(message.chat.id).update_wordlist(0,'-',User(message.chat.id)._language)
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
        User(message.chat.id).update_wordlist(-1,split_message[1],User(message.chat.id)._language)
        
        await message.answer(f"Кандзи {split_message[1]} успешно восстановлено и доступно для повторения :3")

    # Получение информации об иероглифе
    elif '/info' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return
        
            answer = WordGenerator(message.chat.id).get_word_info(split_message[1])  
            await message.answer(f'{answer.zh} -> {answer.py} -> {answer.translate["ru"]}')

        except:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/info hanzi\n"
                "/info 爱"
            )
            return    
        
    elif '/slvl' in message.text.lower():
        '''Пример запроса: /slvl 1 100 0 0'''
        split_message = message.text.lower().split(' ', maxsplit=4)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return
            
            level = int(split_message[1])
            sub_level = int(split_message[2])
            progress = int(split_message[3])
            streak = int(split_message[4])
            LevelSystemController(message.chat.id).set_level(level, sub_level, progress, streak)
            user_data = User(message.chat.id)._data.get_data(User(message.chat.id)._language+"_settings")
            await message.answer(f"Обновлённый уровень: {user_data['level']}\nУровень открытых слов: {user_data['sub-level']}\nПрогресс: {user_data['progress']}\nДействующий стрик: {user_data['streak']}")
        

        except:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/slvl set_level\n"
                "/slvl 1 20 4 6"
            )
            return    

    
    else:
        if LevelSystemController(message.chat.id).streak(-1) == -1:
            print('Стрик уменьшен')
            await message.answer(f"Не верно, {word['transcription']}")


@router.message(ChiStatus.MAO_ON_RU__1, F)
async def free_user_text(message: types.Message, bot: Bot, state: FSMContext):
        print(f'\n🫢🫢🫢',end="")
        for i in message.from_user:
            print(i)
        print(F.sti)




# ВТОРОЙ РЕЖИМ РАБОТЫ

@router.callback_query(F.data == "chinese_train_2")
async def start_chinese_train_2(callback: types.CallbackQuery, state: FSMContext):
    word = WordGenerator(callback.from_user.id).get_random_word("wordlist")

    if type(word) == str:
        await callback.answer(
            text=str(word),
            show_alert=True
        )
        await state.set_state(ChiStatus.MAO_OFF)
    
    else:
        await callback.message.answer(f"Введи кандзи:\n{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler> - {word[2]}\n")
        await state.set_state(ChiStatus.MAO_ON_RU__2)
        await callback.answer(
            text="Повтори выученные ранее слова!\n\nВводи кандзи вида ‘爱’ через пиньинь.\n\nЕсли забыл - нажми на спойлер, чтобы подсмотреть.\n\nСтань ещё ближе к мечте)",
            show_alert=True
        )


@router.message(ChiStatus.MAO_ON_RU__2, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    word = User(message.chat.id)._data.get_data('word')

    if message.text.lower() == word['word']:
        word = WordGenerator(message.chat.id).get_random_word('wordlist')
        await message.answer(f"{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler> - {word[2]}\n")
        


    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.MAO_OFF)
        await message.answer(f"Игра завершена, возвращайся ещё:3")


    elif message.text.lower() == '/skip':
        await message.answer(f"В этом режиме данная команда недоступна.")


    elif message.text.lower() == '/status':
        user_data = User(message.chat.id)._data.get_data(User(message.chat.id)._language+"_settings")
        await message.answer(f"@{message.chat.username}-{message.chat.id}\n\nТекущий уровень: {user_data['level']}\nУровень открытых слов: {user_data['sub-level']}\nПрогресс: {user_data['progress']}\nДействующий стрик: {user_data['streak']}")
        await message.answer(f"Команды работы со словарём:\n/wordlist – скрытые слова\n/restore [хандзи] – вернуть слово")


    elif message.text.lower() == '/wordlist':
        wordlist = User(message.chat.id).update_wordlist(0,'-',User(message.chat.id)._language)
        await message.answer(', '.join(wordlist.values()))


    elif '/restore' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return

            wordlist = User(message.chat.id).update_wordlist(0,'-',User(message.chat.id)._language)
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
        User(message.chat.id).update_wordlist(-1,split_message[1],User(message.chat.id)._language)
        
        await message.answer(f"Кандзи {split_message[1]} успешно восстановлено и доступно для повторения :3")

    # Получение информации об иероглифе
    elif '/info' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("Ошибка: не переданы аргументы")
                return
        
            answer = WordGenerator(message.chat.id).get_word_info(split_message[1])  
            await message.answer(f'{answer.zh} -> {answer.py} -> {answer.translate["ru"]}')

        except:
            await message.answer(
                "Ошибка: неправильный формат команды. Пример:\n"
                "/info hanzi\n"
                "/info 爱"
            )
            return    
    


@router.message(ChiStatus.MAO_ON_RU__2, F)
async def free_user_text(message: types.Message, bot: Bot, state: FSMContext):
        print(f'\n🫢🫢🫢',end="")
        for i in message.from_user:
            print(i)
        print(F.sti)



# ТРЕТИЙ РЕЖИМ РАБОТЫ

@router.callback_query(F.data == "chinese_train_3")
async def start_chinese_train_3(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.answer(f"Введите текст формата:\n\n* 爱 - ai - перевод\n* 爱 - ai - перевод\n* 爱 - ai - перевод\n\nНачинайте новый иероглиф с симфола * и разделяйте данные - c соответствующим числом пробелов, чтобы всё считалось корректно.")
    await state.set_state(ChiStatus.MAO_ON_RU__3)

@router.message(ChiStatus.MAO_ON_RU__3, F.text)
async def upload_user_dictionary(message: types.Message, bot: Bot, state: FSMContext):
    
    msg = User(message.chat.id).update_user_dictionary(message.text)
    await state.set_state(ChiStatus.MAO_OFF)
    await message.answer(f"{msg}")
        


# ЧЕТВЕРТЫЙ РЕЖИМ РАБОТЫ

@router.callback_query(F.data == "chinese_train_4")
async def start_chinese_train_4(callback: types.CallbackQuery, state: FSMContext):

    word = WordGenerator(callback.from_user.id).get_random_word("user_dictionary")

    if word[0] is not 'not_dictionary':
        await callback.message.answer(f"Введи иероглиф:\n{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler> - {word[2]}\n")
        await state.set_state(ChiStatus.MAO_ON_RU__4)
        await callback.answer(
            text="Вводи кандзи вида ‘爱’ через пиньинь.\n\nЕсли забыл - нажми на спойлер, чтобы подсмотреть.\n\nУспехов!",
            show_alert=True
        )
    else:
        await callback.answer(
            text=word[1],
            show_alert=True
        )

@router.message(ChiStatus.MAO_ON_RU__4, F.text)
async def get_message_user_dictionary(message: types.Message, bot: Bot, state: FSMContext):
    word = User(message.chat.id)._data.get_data('word')

    if message.text.lower() == word['word']:

        word =  WordGenerator(message.chat.id).get_random_word("user_dictionary")
        await message.answer(f"{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler> - {word[2]}\n")
        

    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.MAO_OFF)
        await message.answer(f"Игра завершена, возвращайся ещё:3")


    elif message.text.lower() == '/status':
        user_data = User(message.chat.id)._data.get_data(User(message.chat.id)._language+"_settings")
        await message.answer(f"@{message.chat.username}-{message.chat.id}\n\nТекущий уровень: {user_data['level']}\nУровень открытых слов: {user_data['sub-level']}\nПрогресс: {user_data['progress']}\nДействующий стрик: {user_data['streak']}")
        await message.answer(f"Команды работы со словарём:\n/wordlist – скрытые слова\n/restore [хандзи] – вернуть слово")


    elif message.text.lower() == '/wordlist':
        wordlist = User(message.chat.id).get_user_dictionary()
        text = ''
        text += '* ' + wordlist[0][0] + ' - ' + wordlist[0][1] + ' - ' + wordlist[0][2]
        for i in range(len(wordlist)-1):
            text += '\n* ' + wordlist[i+1][0] + ' - ' + wordlist[i+1][1] + ' - ' + wordlist[i+1][2]
        await message.answer(text)
        
    else:
        await message.answer(f"Не верно, {word['transcription']}")



@router.message(ChiStatus.MAO_ON_RU__4, F)
async def free_user_dictionary_text(message: types.Message, bot: Bot, state: FSMContext):
        print(f'\n🫢🫢🫢',end="")
        for i in message.from_user:
            print(i)
        print(F.sti)


