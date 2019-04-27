from telebot import TeleBot
from config import Config


@bot.message_handler(commands=['start'])
def start_handler(messege):
	print('::> Start by user: {}, id: {}'.format(messege.from_user.first_name, messege.chat.id))
	bot.send_message(messege.chat.id, 'Hello, *{}*'.format(messege.from_user.first_name), parse_mode='markdown')


if __name__ == '__main__':
	bot = TeleBot(Config.TOKEN)
