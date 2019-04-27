from telebot import TeleBot
from config import Config
from telebot import types


if __name__ == '__main__':
	bot = TeleBot(Config.TOKEN)

	def send_menu():
		markup = types.ReplyKeyboardMarkup(row_width=2)
		itembtn1 = types.KeyboardButton('a')
		itembtn2 = types.KeyboardButton('v')
		itembtn3 = types.KeyboardButton('d')
		markup.add(itembtn1, itembtn2, itembtn3)
		bot.send_message(241612123, 'Choose one letter:', reply_markup=markup)


	@bot.message_handler(commands=['start'])
	def start_handler(messege):
		print('::> Start by user: {}, id: {}'.format(messege.from_user.first_name, messege.chat.id))
		bot.send_message(messege.chat.id, 'Hello, *{}*'.format(messege.from_user.first_name), parse_mode='markdown')
		send_menu()


	print('--> Запускаю бота')
	bot.polling(True)
