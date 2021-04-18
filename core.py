import telebot, os, conf, flask
from dotenv import load_dotenv
from telebot.apihelper import send_message
load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'), parse_mode=None)
app = flask.Flask(__name__)


@app.route('/%s' % os.getenv('WEBHOOK_TOKEN'))
def webhook(req):
	print(req.json)


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
	mark = telebot.types.InlineKeyboardMarkup()
	for el in conf.repos:
		mark.add(telebot.types.InlineKeyboardButton(el, callback_data=el))
	bot.send_message(conf.admin, 'До системи підключені наступні репозиторії', reply_markup=mark)


print('Start tg')
bot.polling()
app.run(os.getenv('HOST'), os.getenv('PORT') or 7767)
print('Stop all')