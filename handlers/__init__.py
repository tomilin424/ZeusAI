# handlers/__init__.py
import httpx
from openai import OpenAI
from telebot import types
from config import OPENAI_API_KEY, PROXY_URL
from .voice import register_voice_handler

print(f"Debug: Creating HTTP client with proxy: {PROXY_URL}")

http_client = httpx.Client(
    proxies={
        "http://": PROXY_URL,
        "https://": PROXY_URL
    },
    verify=False,
    timeout=30.0,
    follow_redirects=True
)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    http_client=http_client,
    max_retries=5
)

def setup_handlers(bot, user_messages, user_message_ids):
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.InlineKeyboardMarkup()
        webapp_btn = types.InlineKeyboardButton(
            text="Открыть ZeusAI",
            web_app=types.WebAppInfo(url="https://zeus-ai.vercel.app")  # Ваш URL с Vercel
        )
        markup.add(webapp_btn)
        
        welcome_text = """
🌟 Добро пожаловать в ZeusAI!

Нажмите кнопку ниже, чтобы открыть приложение:
    """
        
        bot.send_message(
            message.chat.id,
            welcome_text,
            reply_markup=markup
        )

    @bot.message_handler(func=lambda message: message.text == "💬 Новый чат")
    def new_chat(message):
        chat_number = len(user_messages.get(message.chat.id, [])) // 2 + 1
        user_messages[message.chat.id] = []
        
        bot.reply_to(
            message, 
            f"✨ Чат #{chat_number} начат\nОтправьте ваше сообщение..."
        )

    @bot.message_handler(func=lambda message: message.text == "🎤 Голосовой ассистент")
    def voice_mode(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back_button = types.KeyboardButton("↩️ Вернуться в меню")
        markup.add(back_button)
        
        bot.send_message(
            message.chat.id,
            "🎤 Режим голосового ассистента активирован\n\nОтправьте голосовое сообщение или нажмите 'Вернуться в меню'",
            reply_markup=markup
        )

    @bot.message_handler(func=lambda message: message.text == "⚙️ Настройки")
    def settings(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        model_button = types.KeyboardButton("🤖 Модель AI")
        lang_button = types.KeyboardButton("🌐 Язык")
        back_button = types.KeyboardButton("↩️ Вернуться в меню")
        markup.add(model_button, lang_button)
        markup.add(back_button)
        
        bot.send_message(
            message.chat.id,
            "⚙️ Настройки ZeusAI\n\nВыберите параметр для настройки:",
            reply_markup=markup
        )

    @bot.message_handler(func=lambda message: message.text == "↩️ Вернуться в меню")
    def back_to_main(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        voice_button = types.KeyboardButton("🎤 Голосовой ассистент")
        new_chat_button = types.KeyboardButton("💬 Новый чат")
        settings_button = types.KeyboardButton("⚙️ Настройки")
        markup.add(voice_button)
        markup.add(new_chat_button)
        markup.add(settings_button)
        
        bot.send_message(
            message.chat.id,
            "🏠 Главное меню ZeusAI\n\nВыберите действие:",
            reply_markup=markup
        )

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        try:
            if message.chat.id not in user_messages:
                user_messages[message.chat.id] = []
            
            user_messages[message.chat.id].append({"role": "user", "content": message.text})
            
            print("Debug: Sending request to OpenAI")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=user_messages[message.chat.id]
            )
            
            reply = response.choices[0].message.content
            user_messages[message.chat.id].append({"role": "assistant", "content": reply})
            
            bot.reply_to(message, reply)
        except Exception as e:
            print(f"Debug: Error occurred: {str(e)}")
            bot.reply_to(message, f"❌ Произошла ошибка: {str(e)}")

    @bot.message_handler(commands=['app'])
    def open_webapp(message):
        markup = types.InlineKeyboardMarkup()
        webapp_btn = types.InlineKeyboardButton(
            text="Открыть ZeusAI",
            web_app=types.WebAppInfo(url="URL_ВАШЕГО_WEBAPP")  # Замените на реальный URL
        )
        markup.add(webapp_btn)
        bot.send_message(
            message.chat.id,
            "Нажмите кнопку ниже, чтобы открыть ZeusAI",
            reply_markup=markup
        )

    # Регистрируем обработчик голосовых сообщений
    register_voice_handler(bot)