# Импортируем библиотеки
from telebot import TeleBot
from config import Config
from telebot import types
import requests
import json


# Словарик с базовыми кнопками (на всех экранах меню)
BaseKeyboards = {
	'get_help': '💁‍♀️ Информация',
	'get_phone': '☎️ Телефон банка'
}
# Выбрать тип клиента
ClientTypeKeyboards = {
	'set_individual': '🧑 Частным лицам',
	'set_entity': '👨‍💻 Бизнесу'
}
# Выбор услуги от бота
ServiceTypeKeyboards = {
	'get_enroll': '✍️ Записаться на приём',
	'get_dialog': '💬 Получить консультацию'
}


def api_request(api, method):
	return json.load(requests.get('{}?{}'.format(api, method)))


if __name__ == '__main__':
	#Берем объект бота
	bot = TeleBot(Config.TOKEN)
	API = 'http://127.0.0.1:5000/'

	def send_menu_col(chat_id):
		# Объект макета меню (клавиатуры)
		markup = types.ReplyKeyboardMarkup()
		# Добавляем кнопки выбора типа клиента
		markup.row(
				types.KeyboardButton(ClientTypeKeyboards['set_individual']),
				types.KeyboardButton(ClientTypeKeyboards['set_entity']),
			)
		# Добавляем кнопки вызова меню
		for key in ServiceTypeKeyboards:
			markup.row(types.KeyboardButton(ServiceTypeKeyboards[key]))
		# Добавляем базовые кнопки меню
		markup.row(
				types.KeyboardButton(BaseKeyboards['get_help']),
				types.KeyboardButton(BaseKeyboards['get_phone'])
			)
		# Отправляем макет клавиатуры телеграму
		bot.send_message(chat_id, 'Choose one letter:', reply_markup=markup)


	@bot.message_handler(commands=['start'])
	def start_handler(messege):
		# Обаботчик команды '/start'
		print('::> Start by user: {}, id: {}'.format(messege.from_user.first_name, messege.chat.id))
		bot.send_message(messege.chat.id, 'Hello, *{}*'.format(messege.from_user.first_name), parse_mode='markdown')
		send_menu_col(messege.chat.id)


	@bot.message_handler(commands=['info'])
	def info_handler(messege):
		# Обработчик команды '/info'
		print('::> Info by user: {}, id: {}'.format(messege.from_user.first_name, messege.chat.id))


	@bot.message_handler(content_types=['text'])
	def menu_handler(messege):
		# Обработчик меню и текста
		if messege.text == BaseKeyboards['get_help']:
			print('>> get_help')
			print(api_request(API, messege.text))
		elif messege.text == BaseKeyboards['get_phone']:
			print('>> get_phone')
		elif messege.text == ClientTypeKeyboards['set_individual']:
			print('>> set_individual')
		elif messege.text == ClientTypeKeyboards['set_entity']:
			print('>> set_entity')
		elif messege.text == ServiceTypeKeyboards['get_enroll']:
			print('>> get_enroll')
		elif messege.text == ServiceTypeKeyboards['get_dialog']:
			print('>> get_dialog')

	# Запускаем бота
	print('--> Запускаю бота')
	bot.polling(True)
