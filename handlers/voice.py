# handlers/voice.py
import os
import tempfile
import speech_recognition as sr
from telebot import types

def register_voice_handler(bot):
    @bot.message_handler(content_types=['voice'])
    def handle_voice(message):
        try:
            # Получаем информацию о голосовом сообщении
            file_info = bot.get_file(message.voice.file_id)
            
            # Создаем временный файл для сохранения голосового сообщения
            with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as voice_file:
                downloaded_file = bot.download_file(file_info.file_path)
                voice_file.write(downloaded_file)
                voice_path = voice_file.name

            # Конвертируем голос в текст
            recognizer = sr.Recognizer()
            with sr.AudioFile(voice_path) as source:
                audio = recognizer.record(source)
                text = recognizer.recognize_google(audio, language='ru-RU')
                
            # Отправляем распознанный текст
            bot.reply_to(message, f"Распознанный текст: {text}")
            
            # Удаляем временный файл
            os.unlink(voice_path)
            
        except Exception as e:
            bot.reply_to(message, f"Ошибка при обработке голосового сообщения: {str(e)}")