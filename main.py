from telebot import TeleBot
from config import Config
from telebot import types


if __name__ == '__main__':
	bot = TeleBot(Config.TOKEN)

	def send_menu_col():
		# It defines how many button are fit on each row before continuing on next row
		markup = types.ReplyKeyboardMarkup(row_width=2)
		itembtn1 = types.KeyboardButton('a')
		itembtn2 = types.KeyboardButton('v')
		itembtn3 = types.KeyboardButton('d')
		markup.add(itembtn1, itembtn2, itembtn3)
		bot.send_message(241612123, 'Choose one letter:', reply_markup=markup)

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
		send_menu_col()


	@bot.messege_handler(commands=['info'])
	def info_handler(messege):
		print('::> Info by user: {}, id: {}'.format(messege.from_user.first_name, messege.chat.id))
		send_menu_row()


	print('--> Запускаю бота')
	bot.polling(True)
