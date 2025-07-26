from pyrogram import Client, filters
from pyrogram.types import Message

import os
import time
import random
import operator

import ollama
import requests, json
import buttons
import keyboards



from custom_filters import button_filter
from kinopoisk import config_request, print_film
from dotenv import load_dotenv


API_ID = 2040
API_HASH = 'b18441a1f7f8f7e10e9f9f91a5e62e627'
#BASE_URL = 'https://api.kinopoisk.dev'

file_path = 'C:\тг_апи.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    BOT_TOKEN = file.read()

bot = Client(
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    name='my_bot'
)


@bot.on_message(filters=filters.command('start') | button_filter(buttons.back_button))
async def start(client: Client, message: Message):
    await message.reply(
        "Писюнчик.\n"
        f"Нажми на кнопку {buttons.help_button.text} для получения списка команд.",
        reply_markup=keyboards.main_keyboard
    )


@bot.on_message(filters.command("фильм") | button_filter(buttons.random_button))
async def find_film_by_name(client, message):
    query = message.text.split(maxsplit=1)
    if len(query) < 2:
        await message.reply("Пожалуйста, укажите название фильма после команды /find_film")
        return
    film_name = query[1]
    params = {"name": film_name}
    response = config_request("", params=params)
    if 'error' in response or not response['docs']:
        await message.reply("Фильм не найден или произошла ошибка.")
        return
    film_message = print_film(response['docs'][0])
    await message.reply(film_message)


@bot.on_message(filters=filters.command('random_films') | button_filter(buttons.random_button))
async def send_random_film(client: Client, message: Message):
    response = config_request(random.randint(1, 666))
    if 'error' in response:
        await message.reply(response['error'])
        return
    film_message = print_film(response)
    await message.reply(film_message, reply_markup=keyboards.main_keyboard)


@bot.on_message(filters=filters.command('time') | button_filter(buttons.time_button))  # /time
async def time_command(client: Client, message: Message):
    current_time = time.strftime('%H:%M:%S')
    await message.reply(f'Текущее время: {current_time}', reply_markup=keyboards.main_keyboard)


@bot.on_message(filters=filters.command('calc'))  # /calc 1 + 2
async def calc_command(client: Client, message: Message):
    ops = {
        '+': operator.add, '-': operator.sub,
        '*': operator.mul, '/': operator.truediv
    }
    if len(message.command) != 4:
        return await message.reply('Пример использования:\n/calc 1 + 2\n')

    _, left, op, right = message.command  # /calc 1 + 2
    # /calc, 1, +, 2 = message.command

    op = ops.get(op)
    if op is None:git init

        return await message.reply('Неизвестный оператор')
    if not left.isdigit() or not right.isdigit():
        return await message.reply('Аргумент должен быть числом')

    left, right = int(left), int(right)
    await message.reply(f'Результат {op(left, right)}')

#......|--...--|..../--\....|.....|.../-----\.../-----\......#
#......|..\./..|...|....|...|.\...|...\-----|...|.....|......#
#......|...-...|...|----|...|...\.|.........|...|.....|......#
#......|.......|...|....|...|.....|...\----/....\-----/......#

zov = 2
if zov == 1:
    @bot.on_message(filters=filters.command('mango'))
    async def mango(client: Client, message: Message):
        mgs = await message.reply("РЕЖИМ МАНГО")
        response = ollama.chat(
            model="gemma:2b",
            messages=[
                {"role": "user", "content": 'ответь пользвателю безумно на прозьбу манго'}
            ]
        )
        gemma_reply = response['message']['content']
        await client.delete_messages(chat_id=message.chat.id, message_ids=mgs.id)
        await message.reply(gemma_reply)
        while True:
            await client.send_sticker(
                chat_id=message.chat.id,
                sticker="CAACAgIAAxkBAAEBTANoMHtQgFsdMzldrZaZcKuscxcmnwACcFQAAt5n0Em45N6kqHU3djYE"  # замените на ID нужного стикера
            )

    #goida = " "

    @bot.on_message()
    async def gemma(client: Client, message: Message):
        global goida
        user_message = message.text
        mgs = await message.reply("думаю...")
        response = ollama.chat(
            model="gemma:2b",
            messages=[
                #{"role": "system", "content": goida},
                {"role": "user", "content": message.text}
            ]
        )
        gemma_reply = response['message']['content']
        await client.delete_messages(chat_id=message.chat.id, message_ids=mgs.id)
        await message.reply(gemma_reply)

elif zov == 2:

    API_KEY = "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"
    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    

    @bot.on_message(filters.text & ~filters.command("start"))  # Отвечать только на текстовые сообщения
    async def gemma(client: Client, message: Message):
        try:
            user_message = message.text
            # Отправляем "типизирующее" сообщение
            mgs = await message.reply("Думаю...")

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            with open("save_text.txt","a", encoding="utf-8") as file:
                file.write("\n" + user_message)

            # Правильно формируем запрос с пользовательским сообщением
            data = {
                "model": "deepseek/deepseek-r1:free",
                "messages": [
                    {"role": "system", "content": "Ты умный помощник."},
                    {"role": "user", "content": user_message}  # Используем реальный запрос пользователя
                ]
            }

            # Отправляем запрос с обработкой исключений
            response = requests.post(API_URL, headers=headers, json=data)  # Автоматическая сериализация JSON
            response.raise_for_status()  # Проверка HTTP ошибок

            # Извлекаем ответ
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]

            # Удаляем сообщение "Думаю..." и отправляем ответ
            await mgs.delete()
            with open("save_text.txt","a", encoding="utf-8") as file:
                file.write("\n" + ai_response)
            await message.reply(ai_response)

        except Exception as e:
            # Обработка ошибок
            await message.reply(f"⚠️ Ошибка: {str(e)}")
            await mgs.delete()  # Удаляем уведомление при ошибке

if __name__ == '__main__':
    bot.run()

