import os, io
import telebot
import logging
from PIL import Image, ImageDraw
from flask import Flask, request
import random

from resizer import cropped_thumbnail

TOKEN = os.environ.get("APIKEY")
WEBHOOK_URL = os.environ.get("MYURL")

bot =telebot.TeleBot(TOKEN)
server = Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


def get_filer_by_id(file_id):
	file = bot.get_file(file_id)
	downloaded_file = bot.download_file(file.file_path)
	user_photo = io.BytesIO()
	user_photo.write(downloaded_file)
	user_photo.seek(0)
	return user_photo


def add_foreground(name):
	with Image.open(f"./windows/{random.choice(os.listdir('./windows'))}").convert("RGBA") as foreground:
		background = Image.open(name).convert("RGBA")
		background = cropped_thumbnail(background, foreground.size)
		background.paste(foreground, (0, 0), foreground)
		return background


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, "Привет! Пришли мне фото!")


@bot.message_handler(content_types=["photo"])
def photo(message):
	chat_id = message.chat.id
	file_id = message.photo[-1].file_id
	photo = get_filer_by_id(file_id)
	result = add_foreground(photo)
	result_io = io.BytesIO()
	result.save(result_io, "PNG")
	result_io = "result.png"
	result_io.seek(0)
	bot.send_photo(chat_id, result_io)

@bot.message_handler(content_types=["text"])
def text(message):
	bot.send_message(message.chat.id, "Нет, пришли фото!")


@server.route("/", methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200


@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=WEBHOOK_URL)
	return "!", 200


