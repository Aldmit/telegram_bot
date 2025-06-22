from aiogram import Bot, types
from aiogram import F # магические функции - позволяют вытаскивать всю нужную инфу с минимумом кода

from aiogram.filters.command import Command, CommandObject, CommandStart # Позволяет ловить команды в обработчик по схеме Command('команда')
from aiogram.types import Message,MessageEntity,FSInputFile, URLInputFile, BufferedInputFile, InputTextMessageContent, InlineQueryResultArticle # Работа с файлами
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.utils.keyboard import ReplyKeyboardBuilder # Подстрочные кнопки
from aiogram.utils.keyboard import InlineKeyboardBuilder # Инлайновые кнопки

from aiogram import Router

from src import *



# Инициализируем роутер уровня модуля
router = Router()


# Состояния здесь нужны, чтобы понимать, какие из обработчиков слушать (у обработчиков могут быть одинакоые команды, но нам важно, какой у них при этом статус состояния)
class ChiStatus(StatesGroup):
    MAO_ON_0 = State()
    MAO_ON_1 = State()
    MAO_ON_2 = State()
    MAO_ON_3 = State()
    MAO_ON_4 = State()
    MAO_OFF = State()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    Database(message.chat.id).create_tables()
    User(message.chat.id).checking_existing_user()

    def get_keyboard():
            buttons = [
                [types.InlineKeyboardButton(text="Русский", callback_data="lang_1")],
                [types.InlineKeyboardButton(text="汉语", callback_data="lang_2")],
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
            return keyboard
    await message.answer(f"На данный момент доступна только одна игра: MAO\n\nЧтобы поиграть в неё, тебе нужно установить китайскую расскладку клавиатуры 'Пиньинь - упрощённый'\n\n После этого выбрать язык приложения для старта :3", reply_markup=get_keyboard())
    


# УСТАНОВКА ЯЗЫКА ПРИЛОЖЕНИЯ

@router.callback_query(F.data == "lang_1")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChiStatus.MAO_ON_0)
    User(callback.from_user.id).set_language('ru') 
    await callback.message.answer(f"Выбран русский язык приложения. Для перехода в основное меню используй команду /mao\n")

@router.callback_query(F.data == "lang_2")
async def start_chinese_train_1(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(ChiStatus.MAO_ON_0)
    User(callback.from_user.id).set_language('zh') 
    await callback.message.answer(f"您选择了中文。要进入主菜单，请使用命令: /eyu\n")
