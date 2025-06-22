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
    MAO_ON_ZH_0 = State()
    MAO_ON_ZH_1 = State()
    MAO_ON_ZH_2 = State()
    MAO_ON_ZH_3 = State()
    MAO_ON_ZH_4 = State()
    MAO_OFF = State()


@router.message(Command("eyu"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer_sticker(r'CAACAgQAAxkBAAEL241mESWkgPb6zmSag044fXsFfVdnFQACQwcAAluO6VN4345BS4i5szQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
    await message.answer(f"{Comment().get_comment(User(message.chat.id)._language,0)}, <b>{message.from_user.first_name}</b> :3")
    await state.set_state(ChiStatus.MAO_ON_ZH_0)
    User(message.chat.id).set_language('zh') 
    
    flag = User(message.chat.id).checking_existing_user()

    if flag == True:
        def get_keyboard():
                buttons = [
                    [types.InlineKeyboardButton(text=Comment().get_comment(User(message.chat.id)._language,1), callback_data="russian_train_1")],
                    [types.InlineKeyboardButton(text=Comment().get_comment(User(message.chat.id)._language,2), callback_data="russian_train_2")],
                    [types.InlineKeyboardButton(text=Comment().get_comment(User(message.chat.id)._language,3), callback_data="russian_train_3")],
                    [ types.InlineKeyboardButton(text=Comment().get_comment(User(message.chat.id)._language,4), callback_data="russian_train_4")]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                return keyboard
    else:
        def get_keyboard():
                buttons = [
                    [types.InlineKeyboardButton(text=Comment().get_comment(User(message.chat.id)._language,1), callback_data="russian_train_1")],
                    [types.InlineKeyboardButton(text=Comment().get_comment(User(message.chat.id)._language,3), callback_data="russian_train_3")]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
                return keyboard

    await message.answer(Comment().get_comment(User(message.chat.id)._language,5), reply_markup=get_keyboard())


# ПЕРВЫЙ РЕЖИМ РАБОТЫ

@router.callback_query(F.data == "russian_train_1")
async def start_russian_train_1(callback: types.CallbackQuery, state: FSMContext):

    word = WordGenerator(callback.from_user.id).get_random_word()
    
    await callback.message.answer(f"{Comment().get_comment(User(callback.from_user.id)._language,6)}:\n{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler>\n")
    await state.set_state(ChiStatus.MAO_ON_ZH_1)
    await callback.answer(text=Comment().get_comment(User(callback.from_user.id)._language,7), show_alert=True)

@router.message(ChiStatus.MAO_ON_ZH_1, F.text)
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
                answer += Comment().get_comment(User(message.chat.id)._language,7)+"!\n" + new_word.ru + " - " + new_word.zh

            # elif answer == 'HSK 1 позади, поздравляю!':
            #     await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее

            # elif answer == 'HSK 2 взят, добро пожаловать в HSK 3. Поздравляю!':
            #     await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
            
            # elif answer == 'HSK 3 взят, можешь смело переходить к HSK 4. Это большое достижение!':
            #     await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
            
            # elif answer == 'HSK 3 взят, можешь смело переходить к HSK 4. Это большое достижение!':
            #     await message.answer_sticker(r'CAACAgQAAxkBAAEL251mEShg8lEOQ_SDLXIQvXjGaz-QfgAC5gkAAhCmAVE9qaLjc1JouTQE') #  В качетсве аргумента sticker передаем id стикера который мы получили раннее
    

            await message.answer(f'{answer}')

        word = WordGenerator(message.chat.id).get_random_word()
        await message.answer(f"{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler>\n")
        
        

    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.MAO_OFF)
        await message.answer(f"{Comment().get_comment(User(message.chat.id)._language,9)}:3")


    elif message.text.lower() == '/status':
        user_data = User(message.chat.id)._data.get_data(User(message.chat.id)._language+"_settings")
        await message.answer(f"@{message.chat.username}-{message.chat.id}\n\n{Comment().get_comment(User(message.chat.id)._language,10)}: {user_data['level']}\n{Comment().get_comment(User(message.chat.id)._language,11)}: {user_data['sub-level']}\n{Comment().get_comment(User(message.chat.id)._language,12)}: {user_data['progress']}\n{Comment().get_comment(User(message.chat.id)._language,13)}: {user_data['streak']}")
        await message.answer(f"{Comment().get_comment(User(message.chat.id)._language,14)}")


    elif message.text.lower() == '/wordlist':
        wordlist = User(message.chat.id).update_wordlist(0,'-',User(message.chat.id)._language)
        await message.answer(f"{', '.join(wordlist.values())} \n\n你添加的总计: {len(wordlist.values())-1}")


    elif message.text.lower() == '/skip':
        word = User(message.chat.id)._data.get_data('word')
        wordlist = User(message.chat.id).update_wordlist(1,word['word'],User(message.chat.id)._language)
        await message.answer(f"{wordlist}")
        # await message.answer(f"单词 {word['word']} 成功隐藏:3")

        word = WordGenerator(message.chat.id).get_random_word()
        await message.answer(f"{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler>\n")
    

    elif '/restore' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("错误：没有传递参数")
                return

            wordlist = User(message.chat.id).update_wordlist(0,'-',User(message.chat.id)._language)
            list_with_words = ', '.join(wordlist.values())
            if split_message[1] not in list_with_words:
                await message.answer(
                    "错误：该单词不在单词列表中。检查正确的单词:\n"
                    "/restore [word]\n"
                    "/restore хорошо"
                )
                return
        except:
            await message.answer(
                "错误：命令格式无效。例子:\n"
                "/restore [word]\n"
                "/restore хорошо"
            )
            return
        User(message.chat.id).update_wordlist(-1,split_message[1],User(message.chat.id)._language)
        
        await message.answer(f"单词 {split_message[1]} 已成功恢复并可供重播 :3")

    # Получение информации об иероглифе
    elif '/info' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("错误：没有传递参数")
                return
        
            answer = WordGenerator(message.chat.id).get_word_info(split_message[1])  
            await message.answer(f'{answer.zh} -> {answer.py}')

        except:
            await message.answer(
                "错误：命令格式无效。例子：\n"
                "/info [word]\n"
                "/info хорошо"
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
            await message.answer(f"不正确, {word['word']}")


@router.message(ChiStatus.MAO_ON_ZH_1, F)
async def free_user_text(message: types.Message, bot: Bot, state: FSMContext):
        print(f'\n🫢🫢🫢',end="")
        for i in message.from_user:
            print(i)
        print(F.sti)




# ВТОРОЙ РЕЖИМ РАБОТЫ

@router.callback_query(F.data == "russian_train_2")
async def start_russian_train_2(callback: types.CallbackQuery, state: FSMContext):
    word = WordGenerator(callback.from_user.id).get_random_word("wordlist")

    if type(word) == str:
        await callback.answer(
            text=str(word),
            show_alert=True
        )
        await state.set_state(ChiStatus.MAO_OFF)
    
    else:
        await callback.message.answer(f"输入汉字:\n{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler>\n")
        await state.set_state(ChiStatus.MAO_ON_ZH_2)
        await callback.answer(
            text="重复你之前学过的单词！\n\n通过拼音输入 “хорошо” 等汉字。\n\n如果你忘记了, 请点击剧透查看。\n\n离你的梦想更近)",
            show_alert=True
        )


@router.message(ChiStatus.MAO_ON_ZH_2, F.text)
async def get_message_base(message: types.Message, bot: Bot, state: FSMContext):
    word = User(message.chat.id)._data.get_data('word')

    if message.text.lower() == word['word']:
        word = WordGenerator(message.chat.id).get_random_word('wordlist')
        await message.answer(f"{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler>\n")
        


    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.MAO_OFF)
        await message.answer(f"游戏结束，再回来吧:3")


    elif message.text.lower() == '/skip':
        await message.answer(f"该命令在此模式下不可用.")


    elif message.text.lower() == '/status':
        user_data = User(message.chat.id)._data.get_data(User(message.chat.id)._language+"_settings")
        await message.answer(f"@{message.chat.username}-{message.chat.id}\n\n{Comment().get_comment(User(message.chat.id)._language,10)}: {user_data['level']}\n{Comment().get_comment(User(message.chat.id)._language,11)}: {user_data['sub-level']}\{Comment().get_comment(User(message.chat.id)._language,12)}: {user_data['progress']}\n{Comment().get_comment(User(message.chat.id)._language,13)}: {user_data['streak']}")
        await message.answer(f"使用字典的命令：\n/wordlist – 隐藏单词\n/restore [word] – 返回单词")


    elif message.text.lower() == '/wordlist':
        wordlist = User(message.chat.id).update_wordlist(0,'-',User(message.chat.id)._language)
        await message.answer(', '.join(wordlist.values()))


    elif '/restore' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("错误：没有传递参数")
                return

            wordlist = User(message.chat.id).update_wordlist(0,'-',User(message.chat.id)._language)
            list_with_words = ', '.join(wordlist.values())
            if split_message[1] not in list_with_words:
                await message.answer(
                    "错误：该单词不在单词列表中。检查正确的单词:\n"
                    "/restore [word]\n"
                    "/restore хорошо"
                )
                return
        except:
            await message.answer(
                "错误：命令格式无效。例子:\n"
                "/restore [word]\n"
                "/restore хорошо"
            )
            return
        User(message.chat.id).update_wordlist(-1,split_message[1],User(message.chat.id)._language)
        
        await message.answer(f"单词 {split_message[1]} 已成功恢复并可供重播 :3")

    # Получение информации об иероглифе
    elif '/info' in message.text.lower():
        split_message = message.text.lower().split(' ', maxsplit=1)

        try:
            if split_message[1] is None:
                await message.answer("错误：没有传递参数")
                return
        
            answer = WordGenerator(message.chat.id).get_word_info(split_message[1])  
            await message.answer(f'{answer.zh} -> {answer.py}')

        except:
            await message.answer(
                "错误：命令格式无效。例子:\n"
                "/info [word]\n"
                "/info хорошо"
            )
            return    
    


@router.message(ChiStatus.MAO_ON_ZH_2, F)
async def free_user_text(message: types.Message, bot: Bot, state: FSMContext):
        print(f'\n🫢🫢🫢',end="")
        for i in message.from_user:
            print(i)
        print(F.sti)



# ТРЕТИЙ РЕЖИМ РАБОТЫ

@router.callback_query(F.data == "russian_train_3")
async def start_russian_train_3(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.answer(f"输入文本格式:\n\n* 好的 - хорошо\n* 好的 - хорошо\n* 好的 - хорошо\n\n用符号 * 开始一个新单词，并用适当的数字分隔数据 -空间，以便一切都被认为是正确的。")
    await state.set_state(ChiStatus.MAO_ON_ZH_3)

@router.message(ChiStatus.MAO_ON_ZH_3, F.text)
async def upload_user_dictionary(message: types.Message, bot: Bot, state: FSMContext):
    
    msg = User(message.chat.id).update_user_dictionary(message.text)
    await state.set_state(ChiStatus.MAO_OFF)
    await message.answer(f"{msg}")
        


# ЧЕТВЕРТЫЙ РЕЖИМ РАБОТЫ

@router.callback_query(F.data == "russian_train_4")
async def start_russian_train_4(callback: types.CallbackQuery, state: FSMContext):

    word = WordGenerator(callback.from_user.id).get_random_word("user_dictionary")

    if word[0] is not 'not_dictionary':
        await callback.message.answer(f"输入一个词:\n{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler>\n")
        await state.set_state(ChiStatus.MAO_ON_ZH_4)
        await callback.answer(
            text="输入俄语单词 “хорошо”。\n\n如果您忘记了, 请点击剧透查看。\n\n祝您好运!",
            show_alert=True
        )
    else:
        await callback.answer(
            text=word[1],
            show_alert=True
        )

@router.message(ChiStatus.MAO_ON_ZH_4, F.text)
async def get_message_user_dictionary(message: types.Message, bot: Bot, state: FSMContext):
    word = User(message.chat.id)._data.get_data('word')

    if message.text.lower() == word['translate']:

        word =  WordGenerator(message.chat.id).get_random_word("user_dictionary")
        await message.answer(f"{word[0]} - <tg-spoiler>{word[1]}</tg-spoiler>\n")
        

    elif message.text.lower() == '/exit':
        await state.set_state(ChiStatus.MAO_OFF)
        await message.answer(f"游戏结束，再回来吧 :3")


    elif message.text.lower() == '/status':
        user_data = User(message.chat.id)._data.get_data(User(message.chat.id)._language+"_settings")
        await message.answer(f"@{message.chat.username}-{message.chat.id}\n\n{Comment().get_comment(User(message.chat.id)._language,10)}: {user_data['level']}\n{Comment().get_comment(User(message.chat.id)._language,11)}: {user_data['sub-level']}\n{Comment().get_comment(User(message.chat.id)._language,12)}: {user_data['progress']}\n{Comment().get_comment(User(message.chat.id)._language,13)}: {user_data['streak']}")
        await message.answer(f"字典命令:\n/wordlist – 隐藏词\n/restore [хандзи] – 返回单词")


    elif message.text.lower() == '/wordlist':
        wordlist = User(message.chat.id).get_user_dictionary()
        text = ''
        text += '* ' + wordlist[0][0] + ' - ' + wordlist[0][1]
        for i in range(len(wordlist)-1):
            text += '\n* ' + wordlist[i+1][0] + ' - ' + wordlist[i+1][1]
        await message.answer(text)
        
    else:
        await message.answer(f"不正确, {word['translate']}")



@router.message(ChiStatus.MAO_ON_ZH_4, F)
async def free_user_dictionary_text(message: types.Message, bot: Bot, state: FSMContext):
        print(f'\n🫢🫢🫢',end="")
        for i in message.from_user:
            print(i)
        print(F.sti)


