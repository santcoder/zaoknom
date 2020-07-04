import os
import telebot
import logging
from flask import Flask, request

TOKEN = os.environ.get("APIKEY")
WEBHOOK_URL = os.environ.get("MYURL")

bot =telebot.TeleBot(TOKEN)
server = Flask(__name__)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)


@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message.chat.id, "Привет! Пришли мне фото!")


@server.route("/", methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200


@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url=WEBHOOK_URL)
	return "!", 200


