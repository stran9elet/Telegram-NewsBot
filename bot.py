import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
from flask import Flask, request
from telegram import Update, Bot, ReplyKeyboardMarkup
from utils import get_reply
from gnewsclient import gnewsclient
from waitress import serve
import os


TOKEN = "TOKEN WHICH @BotFather GAVE YOU"

topics_keyboard = [
	["Top Stories", "World", "Nation"],
 	["Business", "Technology", "Entertainment"],
 	["Sports", "Science", "Health"]
]


# enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
	


# define handler functions
def start(update: Updater, context: CallbackContext):
	print(update)

	author = update.message.from_user

	reply = f"Hi! {author.first_name}"
	context.bot.send_message(chat_id=update.message.chat_id, text=reply)


def _help(update: Updater, context: CallbackContext):
	print(update)

	reply = "This is a help text!"
	context.bot.send_message(chat_id=update.message.chat_id, text=reply)


def news(update: Updater, context: CallbackContext):
	reply_keyboard_markup = ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True)
	context.bot.send_message(chat_id=update.message.chat_id, text="Choose a topic", reply_markup=reply_keyboard_markup)



def echo_text(update: Updater, context: CallbackContext):
	print(update)

	reply = update.message.text
	context.bot.send_message(chat_id=update.message.chat_id, text=reply)


def echo_sticker(update: Updater, context: CallbackContext):
	print(update)

	reply = update.message.sticker.file_id
	context.bot.send_sticker(chat_id=update.message.chat_id, sticker=reply)


def reply_text(update: Updater, context: CallbackContext):
	print(update)

	intent, reply = get_reply(update.message.text, update.message.chat_id)
	print(reply)
	if intent == "NewsIntent":
		client = gnewsclient.NewsClient()
		client.location = reply.get("geo-country")
		client.language = reply.get("language")
		client.topic = reply.get("newsentity")

		article_list = client.get_news()[:5]
		for article in article_list:
			context.bot.send_message(chat_id=update.message.chat_id, text=article["link"])
	else:
		context.bot.send_message(chat_id=update.message.chat_id, text=reply)



def get_port():
	return int(os.environ.get("PORT", 8080))


	
def main():
	print("--------------------------------------START--------------------------------------------")

	# creating the bot object and setting the webhook
	bot = Bot(TOKEN)
	bot.set_webhook("YOUR CALLBACK URL" + TOKEN)


	# creating the dispatcher
	dispatcher = Dispatcher(bot, None)


	# add handlers to dispatcher
	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("help", _help))
	dispatcher.add_handler(CommandHandler("news", news))
	dispatcher.add_handler(MessageHandler(Filters.text, reply_text))
	dispatcher.add_handler(MessageHandler(Filters.sticker, echo_sticker))


	app = Flask(__name__)

	# create the view to handle webhook
	@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
	def webhook():
		request_json = request.get_json()
		update = Update.de_json(request_json, bot)
		dispatcher.process_update(update)
		return "ok"


	return app

	print("--------------------------------------END--------------------------------------------")

		

if __name__ == "__main__":
	app = main()
	app.run(debug=True, port=get_port(), host='0.0.0.0')

