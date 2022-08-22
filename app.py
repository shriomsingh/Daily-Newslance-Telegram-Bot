import logging
from telegram import Update, Bot,ReplyKeyboardMarkup
from flask import Flask, request
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ContextTypes, CallbackContext, Dispatcher)
from utils import get_reply, fetch_news, topics_keyboard

#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


Token = '5555837723:AAHSc2hC6ZEPINBHvpY7MM884urExivwYAk'

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello!"


@app.route(f'/{Token}', methods = ['GET','POST'])
def webhook(): 
	update = Update.de_json(request.get_json(),bot)

	dp.process_update(update)
	return "ok"


def start(update: Update, context: CallbackContext):
	print(update)
	author = update.message.from_user.first_name
	reply = "Hi! {}".format(author)
	context.bot.send_message(chat_id=update.message.chat_id, text= reply)
	

def _help(update: Update, context: CallbackContext):
	help_txt = 'What news would you like to hear!!'
	context.bot.send_message(chat_id=update.message.chat_id, text= help_txt)

def news(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.message.chat_id, text="Choose a Category",
		reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard,one_time_keyboard=True))

def reply_text(update: Update, context: CallbackContext):
	intent, reply = get_reply(update.message.text,update.message.chat_id)

	if intent == 'get_news':
		articles = fetch_news(reply)
		for article in articles:
			context.bot.send_message(chat_id = update.message.chat_id, text=article['link'])
	else:
		context.bot.send_message(chat_id =update.message.chat_id, text= reply)

def echo_sticker(update: Update, context: CallbackContext):
	context.bot.send_sticker(chat_id = update.message.chat_id, sticker = update.message.sticker.file_id)

def error(update: Update, context: CallbackContext):
	logger.error("Update '%s' caused error '%s'", update, update.error)


# def main():

bot = Bot(Token)
try:
	bot.set_webhook("https://salty-brook-58301.herokuapp.com/" + Token)
except Exception as e:
	print(e)

	
dp = Dispatcher(bot, None)
dp.add_handler(CommandHandler('start',start))
dp.add_handler(CommandHandler('help',_help))
dp.add_handler(CommandHandler('news',news))
dp.add_handler(MessageHandler(Filters.text,reply_text))
dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
dp.add_error_handler(error)




if __name__ == '__main__':
	# main()
	app.run(port=8443)

