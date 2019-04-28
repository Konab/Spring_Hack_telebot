# Импортируем библиотеки
from telebot import TeleBot
from config import Config
from telebot import types
import requests
import json
from dataclasses import dataclass


@dataclass
class Query:
	client_type: str = ''
	service: str = ''
	geo: str = ''


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


def set_client_type_keyboard(query, markup):
	if query.client_type == 'individual':
		markup.row(types.KeyboardButton('Частное лицо: *Изменить*'))
	elif query.client_type == 'entity':
		markup.row(types.KeyboardButton('Юр. лицо: *Изменить*'))
	else:
		markup.row(
				types.KeyboardButton(ClientTypeKeyboards['set_individual']),
				types.KeyboardButton(ClientTypeKeyboards['set_entity'])
			)
	return markup


def set_service_type_keyboard(query, markup):
	if query.service == 'enroll':
		pass
	elif query.service == 'dialog':
		pass
	else:
		for key in ServiceTypeKeyboards:
					markup.row(types.KeyboardButton(ServiceTypeKeyboards[key]))
	return markup


def set_base_keyboard(markup):
	markup.row(
			types.KeyboardButton(BaseKeyboards['get_help']),
			types.KeyboardButton(BaseKeyboards['get_phone'])
		)
	return markup


def set_keyboard(query):
	# Объект макета меню (клавиатуры)
	markup = types.ReplyKeyboardMarkup()
	# Добавляем кнопки выбора типа клиента
	markup = set_client_type_keyboard(query, markup)
	# Добавляем кнопки вызова меню
	markup = set_service_type_keyboard(query, markup)
	# Добавляем базовые кнопки меню
	markup = set_base_keyboard(markup)
	return markup


def api_request(api, method):
	'--> Отправил запрос на сервер'
	return requests.get('{}{}'.format(api, method)).json()


def get_help():
	return '*Добро пожаловать!*\nЯ - бот команды 51с для банка *«Уралсиб»*.\nЯ помогу вам найти отделение банка и встать в очередь прямо сейчас.'


def get_phone(type=None):
	individual_phone = '*Частным лицам:* 8 (495) 723-77-77'
	entity_phone = '*Бизнесу:* 8 (800) 700-77-16'
	if type == 'individual':
		return individual_phone
	elif type == 'entity':
		return entity_phone
	else:
		return individual_phone + '\n' + entity_phone


if __name__ == '__main__':
	#Берем объект бота
	bot = TeleBot(Config.TOKEN)
	API = 'http://127.0.0.1:5000/'
	query = Query()

	def send_menu_col(chat_id, text=''):
		# Отправляем макет клавиатуры телеграму
		markup = set_keyboard(query)
		if text:
			bot.send_message(chat_id, text, reply_markup=markup)
		else:
			bot.send_message(chat_id, 'Как Вам помочь?', reply_markup=markup)


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
			bot.send_message(messege.chat.id, get_help(), parse_mode='markdown')
			# print(api_request(API, 'get_help'))
		elif messege.text == BaseKeyboards['get_phone']:
			print('>> get_phone')
			bot.send_message(messege.chat.id, get_phone(), parse_mode='markdown')
			# print(api_request(API, 'get_phone'))
		elif messege.text == ClientTypeKeyboards['set_individual']:
			print('>> set_individual')
			query.client_type = 'individual'
			send_menu_col(messege.chat.id, text='Вы выбрали тип: *Частное лицо*')
			# print(api_request(API, 'set_individual'))
		elif messege.text == ClientTypeKeyboards['set_entity']:
			print('>> set_entity')
			query.client_type = 'entity'
			send_menu_col(messege.chat.id, text='Вы выбрали тип: *Юр. лицо*')
			# print(api_request(API, 'set_entity'))
		elif messege.text == ServiceTypeKeyboards['get_enroll']:
			print('>> get_enroll')
			# print(api_request(API, 'get_enroll'))
		elif messege.text == ServiceTypeKeyboards['get_dialog']:
			print('>> get_dialog')
			# print(api_request(API, 'get_dialog'))

	# Запускаем бота
	print('--> Запускаю бота')
	bot.polling(True)
