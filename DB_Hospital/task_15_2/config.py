# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Указываем путь к .env файлу в текущей директории
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """Класс с настройками подключения к базе данных"""

    # Параметры подключения из .env файла
    DRIVER = os.getenv('MS_SQL_DRIVER')
    SERVER = os.getenv('MS_SQL_SERVER')
    DATABASE = 'Hospital'  # Используем базу Hospital
    USER = os.getenv('MS_SQL_USER')
    PASSWORD = os.getenv('MS_SQL_KEY')

    @classmethod
    def get_connection_string(cls):
        """Формирование строки подключения"""
        return f"""
            DRIVER={{{cls.DRIVER}}};
            SERVER={cls.SERVER};
            DATABASE={cls.DATABASE};
            UID={cls.USER};
            PWD={cls.PASSWORD};
            TrustServerCertificate=yes;
        """

    @classmethod
    def print_config(cls):
        """Вывод конфигурации"""
        print("📁 Конфигурация:")
        print(f"   Сервер: {cls.SERVER}")
        print(f"   База данных: {cls.DATABASE}")
        print(f"   Пользователь: {cls.USER}")
        print(f"   Драйвер: {cls.DRIVER}")
        print(f"   Файл .env: {env_path}")