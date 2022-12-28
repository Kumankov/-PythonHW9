import telebot
from telebot import types
import logging
from datetime import datetime

bot = telebot.TeleBot('Token')

def logging(message,comment):
    file = open('log.csv','a')
    time = datetime.utcfromtimestamp(int(message.date)+10800).strftime('%Y-%m-%d %H:%M:%S')
    file.write(f'{time};{message.from_user.id};{message.from_user.first_name};{message.from_user.username};{message.from_user.last_name};{message.text};{comment}\n')
    file.close

display = ''
old_display = ''

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(   telebot.types.InlineKeyboardButton('j', callback_data='j'),
                telebot.types.InlineKeyboardButton('C', callback_data='C'),
                telebot.types.InlineKeyboardButton('⌫', callback_data='⌫'),
                telebot.types.InlineKeyboardButton('/', callback_data='/') )

keyboard.row(   telebot.types.InlineKeyboardButton('7', callback_data='7'),
                telebot.types.InlineKeyboardButton('8', callback_data='8'),
                telebot.types.InlineKeyboardButton('9', callback_data='9'),
                telebot.types.InlineKeyboardButton('*', callback_data='*') )

keyboard.row(   telebot.types.InlineKeyboardButton('4', callback_data='4'),
                telebot.types.InlineKeyboardButton('5', callback_data='5'),
                telebot.types.InlineKeyboardButton('6', callback_data='6'),
                telebot.types.InlineKeyboardButton('-', callback_data='-') )

keyboard.row(   telebot.types.InlineKeyboardButton('1', callback_data='1'),
                telebot.types.InlineKeyboardButton('2', callback_data='2'),
                telebot.types.InlineKeyboardButton('3', callback_data='3'),
                telebot.types.InlineKeyboardButton('+', callback_data='+') )

keyboard.row(   telebot.types.InlineKeyboardButton('0', callback_data='0'),
                telebot.types.InlineKeyboardButton(',', callback_data='.'),
                telebot.types.InlineKeyboardButton('=', callback_data='=') )

@bot.message_handler(commands = ['calc'] )
def getmessage(message):
    global display
    logging(message,'')
    if display == '':
        bot.send_message(message.from_user.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, display, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):    
    global old_display, display    
    data = query.data
    print(data)
    if data == 'C':         
        display = ''
    elif data == '⌫':
        display = display[:len(display)-1]             
    elif data == '=':        
        try:
            logging(query.message,str(display+'='+str(eval(display))))
            display = str(eval(display))            
        except:            
            logging(query.message,str(display+'= Ошибка'))
            display = 'Ошибка!'            
    else:        
        display += data
    
    if (display != old_display and display != '') or (display != old_display and display == ''):
        if display == "":
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0', reply_markup=keyboard)
            old_display = '0'
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=display, reply_markup=keyboard)
            old_display = display

    old_display = display
    if display == 'Ошибка!': display = ''

bot.polling(none_stop=False, interval=0)