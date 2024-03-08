from dataclasses import dataclass

from environs import Env

@dataclass
class Bot:
    token: str  # Токен для доступа к телеграм-боту

@dataclass
class Config:
    bot: Bot

# Создаем функцию, которая будет читать файл .env и возвращать экземпляр
# класса Config с заполненными полями token и admin_ids
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(bot=Bot(token=env('BOT_TOKEN')))