
from aiogram.filters.command import Command, CommandObject, CommandStart # Позволяет ловить команды в обработчик по схеме Command('команда')
from aiogram.types import Message,MessageEntity,FSInputFile, URLInputFile, BufferedInputFile, InputTextMessageContent, InlineQueryResultArticle # Работа с файлами

from ..db_functions import *


from aiogram import Router

# Инициализируем роутер уровня модуля
router = Router()


@router.message(Command("set_status"))
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

