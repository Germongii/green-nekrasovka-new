import telebot
import sqlite3
from telebot import types
from telebot.types import InputMediaPhoto
import emoji


blocked_address = ['1 вольская дом 6', 'льва яшина 3']
blocked_commands = ['Фото с последней высадки' + emoji.emojize(':framed_picture:'),'Дата и место ближайшей высадки' + emoji.emojize(':spiral_calendar:'), 'О проекте' + emoji.emojize(':white_exclamation_mark:'),'Предложить адресс высадки']
bot = telebot.TeleBot('****')
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item4 = types.KeyboardButton('Фото с последней высадки' + emoji.emojize(':framed_picture:'))
    item2 = types.KeyboardButton('Дата и место ближайшей высадки' + emoji.emojize(':spiral_calendar:'))
    item3 = types.KeyboardButton('О проекте' + emoji.emojize(':white_exclamation_mark:'))
    item1 = types.KeyboardButton('Предложить адресс высадки')
    markup.add(item4,item2,item3,item1)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)

#def bot_message(message):
#    if message.chat.type == 'private':
#        if message.text == 'Предложить адресс высадки':
@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == 'Предложить адресс высадки':
        msg = bot.send_message(message.chat.id, 'Введите адресс высадки или геолокацию')
        bot.register_next_step_handler(msg, fio_step)
    if message.text == 'Дата и место ближайшей высадки' + emoji.emojize(':spiral_calendar:'):
        msg = bot.send_message(message.chat.id, 'Высадки продолжатся весной, а пока вы можете предложить адрес высадки')
    if message.text == 'Фото с последней высадки' + emoji.emojize(':framed_picture:'):
        with open('20-09_1.jpg','rb') as photo1, open('20-09_2.jpg','rb') as photo2, open('20-09_3.jpg','rb') as photo3, open('20-09_4.jpg','rb') as photo4,open('20-09_5.jpg','rb') as photo5:
            bot.send_media_group(message.chat.id, [InputMediaPhoto(photo1), InputMediaPhoto(photo2), InputMediaPhoto(photo3),InputMediaPhoto(photo4), InputMediaPhoto(photo5)])
    if message.text == 'О проекте' + emoji.emojize(':white_exclamation_mark:'):
        msg = bot.send_message(message.chat.id,'Test message')

def fio_step(message):
    db = sqlite3.connect('user_address')
    sql = db.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS  users (
        user_id TEXT,
        adress TEXT
    )""")
    db.commit()
    input_adress = message.text
    input_id = message.from_user.id
    print(input_adress)
    fl = 0
    for l in blocked_commands:
        if input_adress == l:
            fl = 2
            main(message)
            break
    for i in blocked_address:
        if input_adress == i:
            fl = 1
            msg = bot.send_message(message.chat.id, 'Ксожелению высадка на данном адресе невозможна по техническим причинам')
            break
    if fl == 0:
        sql.execute(f"INSERT INTO users VALUES (?,?)", (input_id,input_adress))
        db.commit()
        msg = bot.send_message(message.chat.id, 'Спасибо, ваше предложение записано' + emoji.emojize(':check_mark_button:'))














            # connect = sqlite3.connect('users.db')
            # cursor = connect.cursor()
            # cursor.execute("""CREATE TABLE IF NOT EXISTS adress_users(
            #     id INTEGER
            # )""")
            # connect.commit()
            # users_list = [message.chat.id]
            # cursor.execute("INSERT INTO adress_users VALUES(?);",users_list)
            # connect.commit()



bot.polling(none_stop=True)
