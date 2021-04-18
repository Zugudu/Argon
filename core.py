from logging import DEBUG
import telebot, os, conf
from dotenv import load_dotenv
from telebot.apihelper import send_message
load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN'), parse_mode=None)


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


print('Start')
bot.polling()
print('Stop')