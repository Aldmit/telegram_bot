import asyncio
import logging

from aiogram import Bot, Dispatcher
from config import Config, load_config
import core


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

config: Config = load_config()
BOT_TOKEN: str = config.bot.token

# Объект бота
bot = Bot(BOT_TOKEN, parse_mode="HTML")
# Диспетчер
dp = Dispatcher()


async def start_bot(bot: Bot):
    print("\n\n🟢 Бот запущен\n\n\n")
async def stop_bot(bot: Bot):
    print("\n\n🔴 Бот остановлен\n\n\n")

dp.startup.register(start_bot)  # регистрируем в диспетчере функцию по запуску
dp.shutdown.register(stop_bot)  # регистрируем в диспетчере функцию по остановке


dp.include_router(core.chi_help_func.router)
dp.include_router(core.chi_handlers.router)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
