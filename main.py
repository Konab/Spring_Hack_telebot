from telebot import TeleBot
from config import Config
from telebot import types


Keyboards = {'get_help': '💁‍♀️ Справочная информация',
			'get_phone': '☎️ Телефон оператора'
		}

if __name__ == '__main__':
	bot = TeleBot(Config.TOKEN)

	def send_menu_col(chat_id):
		# It defines how many button are fit on each row before continuing on next row
		markup = types.ReplyKeyboardMarkup(row_width=2)
		for key in Keyboards:
			markup.row(Keyboards[key])

		markup.add()
		bot.send_message(chat_id, 'Choose one letter:', reply_markup=markup)

	def send_menu_row():
		# or add KeyboardButton one row at a time:
		markup = types.ReplyKeyboardMarkup()
		itembtna = types.KeyboardButton('a')
		itembtnv = types.KeyboardButton('v')
		itembtnc = types.KeyboardButton('c')
		itembtnd = types.KeyboardButton('d')
		itembtne = types.KeyboardButton('e')
		markup.row(itembtna, itembtnv)
		markup.row(itembtnc, itembtnd, itembtne)
		bot.send_message(241612123, 'Choose one letter:', reply_markup=markup)


	@bot.message_handler(commands=['start'])
	def start_handler(messege):
		print('::> Start by user: {}, id: {}'.format(messege.from_user.first_name, messege.chat.id))
		bot.send_message(messege.chat.id, 'Hello, *{}*'.format(messege.from_user.first_name), parse_mode='markdown')
		send_menu_col(messege.chat.id)


	@bot.message_handler(commands=['info'])
	def info_handler(messege):
		print('::> Info by user: {}, id: {}'.format(messege.from_user.first_name, messege.chat.id))
		send_menu_row()


	print('--> Запускаю бота')
	bot.polling(True)
