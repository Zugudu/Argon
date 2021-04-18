import telebot, os, conf, flask, multiprocessing
from flask import request
from dotenv import load_dotenv
from telebot.apihelper import send_message
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


@bot.callback_query_handler(func=lambda m: True)
def purpose(msg):
	if conf.repos.get(msg.data):
		cmd = 'cd %s && git pull origin master' % conf.repos[msg.data]
		if os.getenv('DEBUG'):
			print(cmd)
		else:
			os.system(cmd)
		mes = 'Репозиторій %s оновлено' % msg.data
	else:
		mes = 'Такий репозиторій відсутній в системі'
	bot.send_message(conf.admin, mes)

@bot.message_handler(commands=['show'])
def show(msg):
	bot.send_message(conf.admin, 'До системи підключені наступні репозиторії', reply_markup=getMark())


def start_webhook():
	app.run(os.getenv('HOST'), os.getenv('PORT') or 7767)

def start_tg():
	bot.polling()


if __name__ == '__main__':
	p1 = multiprocessing.Process(target=start_webhook)
	p1.start()

	print('Start tg')
	p2 = multiprocessing.Process(target=start_tg)
	p2.start()
	try:
		p1.join()
		p2.join()
	except KeyboardInterrupt:
		pass
	print('Stop all')