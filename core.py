import telebot, os, conf, flask, multiprocessing
from flask import request
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'), parse_mode=None)
app = flask.Flask(__name__)


def getMark():
	mark = telebot.types.InlineKeyboardMarkup()
	for el in conf.repos:
		mark.add(telebot.types.InlineKeyboardButton(el, callback_data=el))
	return mark


@app.route('/%s' % os.getenv('WEBHOOK_TOKEN'), methods=['POST'])
def webhook():
	print(request.json['repository']['full_name'])
	bot.send_message(conf.admin, 'Оновлено репозиторій %s\nБажаєте оновити якісь репозиторії?' % request.json['repository']['full_name'], reply_markup=getMark())
	return ('OK', 200)

def start():
	app.run(os.getenv('HOST'), os.getenv('PORT') or 7767)

if __name__ == '__main__':
	try:
		p = multiprocessing.Process(target=os.system, args=('py tg_bot.py', ))
		p1 = multiprocessing.Process(target=start)
		p.start()
		p1.start()
		p.join()
		p1.join()
	except KeyboardInterrupt:
		pass
	print('Stop all')