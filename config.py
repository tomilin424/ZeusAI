# config.py
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токенов из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Настройки прокси
PROXY_HOST = os.getenv('PROXY_HOST')
PROXY_PORT = os.getenv('PROXY_PORT')
PROXY_USER = os.getenv('PROXY_USER')
PROXY_PASS = os.getenv('PROXY_PASS')

# Формируем строку прокси
PROXY_URL = None
if PROXY_HOST and PROXY_PORT:
    if PROXY_USER and PROXY_PASS:
        PROXY_URL = f"socks5://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
    else:
        PROXY_URL = f"socks5://{PROXY_HOST}:{PROXY_PORT}"

print(f"Debug: PROXY_URL = {PROXY_URL}")  # Для отладки

# Проверка наличия токенов
if not TOKEN:
    raise ValueError("Не указан TELEGRAM_BOT_TOKEN в файле .env")
if not OPENAI_API_KEY:
    raise ValueError("Не указан OPENAI_API_KEY в файле .env")