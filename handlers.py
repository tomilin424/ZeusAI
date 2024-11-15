import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def setup_handlers(bot, user_messages, user_message_ids):
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.reply_to(message, "Привет! Я бот с GPT. Отправьте мне сообщение, и я отвечу на него.")

    @bot.message_handler(func=lambda message: True)
    def handle_message(message):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": message.text}
                ]
            )
            bot.reply_to(message, response.choices[0].message.content)
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {str(e)}") 