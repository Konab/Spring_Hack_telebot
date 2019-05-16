# Импортируем библиотеки
from telebot import TeleBot
from config import Config
from telebot import types
import requests
import json
from dataclasses import dataclass
from random import choice


def get_number():
	a = [i for i in range(10)]
	b = [choice(a) for _ in range(6)]
	return '{0}{1}{2}-{3}{4}{5}'.format(*b)



@dataclass
class Query:
	client_type: str = ''
	service: str = ''
	curr_geo: str = ''

	def remove(self):
		self.client_type = ''
		self.service = ''
		self.curr_geo = {}

	def update(self, client_type=None, service=None, curr_geo=None):
		if client_type != None:
			self.client_type = client_type
		if service != None:
			self.service = service
		if curr_geo != None:
			self.curr_geo = curr_geo

	def to_dict(self):
		return {'client_type': self.client_type, 'service': self.service, 'lat': self.curr_geo['lat'], 'lon': self.curr_geo['lon']}


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

Change = {
	'individual': '🧑 Назад',
	'entity': '👨‍💻 Назад'
}


# def start_dialog(api, chat_id, text):
# 	req = requests.get('{}{}'.format(api, 'detected_text'), params=query.to_dict())


def set_client_type_keyboard(query, markup):
	if query.client_type == 'individual':
		markup.row(types.KeyboardButton(Change[query.client_type]))
	elif query.client_type == 'entity':
		markup.row(types.KeyboardButton(Change[query.client_type]))
	else:
		markup.row(
				types.KeyboardButton(ClientTypeKeyboards['set_individual']),
				types.KeyboardButton(ClientTypeKeyboards['set_entity'])
			)
	return markup


def set_service_type_keyboard(query, markup):
	if query.service == 'enroll':
		markup.row(types.KeyboardButton(ServiceTypeKeyboards['get_enroll'], request_location=True))
		markup.row(types.KeyboardButton(ServiceTypeKeyboards['get_dialog']))
	elif query.service == 'dialog':
		pass
	else:
		markup.row(types.KeyboardButton(ServiceTypeKeyboards['get_enroll'], request_location=True))
		markup.row(types.KeyboardButton(ServiceTypeKeyboards['get_dialog']))
	return markup


def set_base_keyboard(markup):
	markup.row(
			types.KeyboardButton(BaseKeyboards['get_help']),
			types.KeyboardButton(BaseKeyboards['get_phone'])
		)
	return markup


def set_keyboard(query):
	# Объект макета меню (клавиатуры)
	if not query.client_type:
		markup = types.ReplyKeyboardMarkup()
		# Добавляем кнопки выбора типа клиента
		markup = set_client_type_keyboard(query, markup)
		# Добавляем кнопки вызова меню
		markup = set_service_type_keyboard(query, markup)
		# Добавляем базовые кнопки меню
		markup = set_base_keyboard(markup)
	else:
		markup = types.ReplyKeyboardMarkup()
		# Добавляем кнопки вызова меню
		markup = set_service_type_keyboard(query, markup)
		# Добавляем базовые кнопки меню
		markup = set_base_keyboard(markup)
		# Добавляем кнопки выбора типа клиента
		markup = set_client_type_keyboard(query, markup)
	return markup


def api_request(api, method):
	'--> Отправил запрос на сервер'
	return requests.get('{}{}'.format(api, method)).json()


def get_near(chat_id, api, query):
	print('•'*10)
	print('The Fin')
	print(query)
	req = requests.get('{}{}'.format(api, 'get_near'), params=query.to_dict())
	if req.status_code == 200:
		company_dict = req.json()
		text = '*Ближайшее отделение находится по адресу:* {address}\n*Информация:* {info}\n*Время работы:* {work}\n*Время в пути:* {time}мин'.\
			format(
				address=company_dict['address'].replace('\n', '')[5:], 
				time=company_dict['time'],
				info=company_dict['info-page'].replace('\n', '')[5:],
				work=company_dict['working-time'].replace('\n', '')[5:]
			)
		reply = json.dumps({'inline_keyboard': [
			[{'text': '✅ Записаться', 'callback_data': 'call_accepted'}],
		]})
		bot.send_message(chat_id, text, parse_mode='markdown', disable_web_page_preview=True)
		bot.send_location(chat_id, company_dict['lon'], company_dict['lat'], reply_markup=reply)


def get_help():
	return '*Добро пожаловать!*\nЯ - бот команды 51с для банка *«Уралсиб»*.\nЯ помогу вам найти отделение банка и встать в очередь прямо сейчас.'


def get_phone(query):
	individual_phone = '*Частным лицам:* 8 (495) 723-77-77'
	entity_phone = '*Бизнесу:* 8 (800) 700-77-16'
	if query.client_type == 'individual':
		return individual_phone
	elif query.client_type == 'entity':
		return entity_phone
	else:
		return individual_phone + '\n' + entity_phone


if __name__ == '__main__':
	#Берем объект бота
	bot = TeleBot(Config.TOKEN)
	API = 'http://127.0.0.1:8000/'
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
		print(messege.from_user)
		bot.send_message(241612123, f'start by user: {messege.from_user.first_name}|@{messege.from_user.nick}, id: {messege.chat.id}')
		query.remove()
		bot.send_message(messege.chat.id, 'Здравствуйте, *{}*'.format(messege.from_user.first_name), parse_mode='markdown')
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
			bot.send_message(messege.chat.id, get_phone(query), parse_mode='markdown')
			# print(api_request(API, 'get_phone'))
		elif messege.text == ClientTypeKeyboards['set_individual']:
			print('>> set_individual')
			query.client_type = 'individual'
			send_menu_col(messege.chat.id, text='Вы выбрали тип: Частное лицо')
			if query.curr_geo:
				get_near(messege.chat.id, API, query)
			# print(api_request(API, 'set_individual'))
		elif messege.text == ClientTypeKeyboards['set_entity']:
			print('>> set_entity')
			query.client_type = 'entity'
			send_menu_col(messege.chat.id, text='Вы выбрали тип: Юр. лицо')
			if query.curr_geo:
				get_near(messege.chat.id, API, query)
			# print(api_request(API, 'set_entity'))
		elif messege.text == ServiceTypeKeyboards['get_enroll']:
			print('>> get_enroll')
			query.service = 'enroll'
			#######
			# print(api_request(API, 'get_enroll'))
		elif messege.text == ServiceTypeKeyboards['get_dialog']:
			print('>> get_dialog')
			bot.send_message(messege.chat.id, 'Вы хотите решить Ваш вопрос с оператором?')
			# markup = types.ReplyKeyboardRemove(selective=False)
			# bot.send_message(chat_id, 'Чем я могу помочь?', reply_markup=markup)
			# print(api_request(API, 'get_dialog'))
		elif messege.text == Change['individual']:
			query.update(client_type='')
			send_menu_col(messege.chat.id)
		elif messege.text == Change['entity']:
			query.update(client_type='')
			send_menu_col(messege.chat.id)
		else:
			bot.send_message(messege.chat.id, 'Вы хотите решить Ваш вопрос с оператором?')
		# 	start_dialog(API, message.chat.id, messege.text)


	@bot.message_handler(content_types=["location"])
	def location(message):
		print('>> location')
		query.service = 'enroll'
		if message.location is not None:
			location = message.location
			print(location)
			query.curr_geo = {'lat': location.latitude, 'lon': location.longitude}

			if not query.client_type:
				send_menu_col(message.chat.id, text='Вы частное или юридическое лицо?')
				# get_near(API, query)
			else:
				get_near(message.chat.id, API, query)


	@bot.callback_query_handler(func=lambda call: True)
	def callback(call):

		msg = call.data.split('_')

		if msg[1] == 'accepted':
			bot.send_message(call.message.chat.id, '*Ваш номер:* {}'.format(get_number()), parse_mode='markdown')

	# Запускаем бота
	print('--> Запускаю бота')
	bot.polling(True)
