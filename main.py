import telebot
from random import randint
import playing
import calc
import phonebook

bot = telebot.TeleBot('Token')

phone_list = []

@bot.message_handler(commands=['help', 'start'])
def Start(message):
    playing.logging(message,'')
    bot.send_message(message.chat.id, 
                        '/calc - текстовый простейший калькулятор'
                        '\n/sec_calc - текстовый простейший калькулятор с поэлементным вводом'
                        '\n/candys - игра в "Конфеты"'
                        '\n/tictactoe - игра в "Крестики-нолики"'
                        '\n/text - типа анекдоты'
                        '\n/phonebook - телефонная книга')

@bot.message_handler(commands=['calc'])
def Calc(message):
    playing.logging(message,'')
    msg = bot.send_message(message.chat.id,'Введите арифметическое выражение')
    bot.register_next_step_handler(msg, calc.Calc_2,bot)
    
@bot.message_handler(commands=['sec_calc'])
def Second_calc(message):
    playing.logging(message,'')
    calc_list = []
    check_complex = False
    msg = bot.send_message(message.chat.id,'Введите первое число')
    bot.register_next_step_handler(msg, calc.Second_calc_2,bot,calc_list,check_complex)
    
@bot.message_handler(commands=['candys'])
def Candy(message):
    playing.logging(message,'')
    msg = bot.send_message(message.chat.id,'Введите количество конфет от 1 до 28')
    candys = 2021
    bot.register_next_step_handler(msg, playing.Candy_2,bot,candys)

@bot.message_handler(commands=['tictactoe'])
def Ttt(message):
    playing.logging(message,'')
    move = [0]*100  
    moves = []
    line = [['  ',' ',' '],['   ',' ',' '],['   ',' ',' ']]   
    msg = bot.send_message(message.chat.id,'Введите координаты вида 1 2 через пробел')
    bot.register_next_step_handler(msg, playing.Ttt_2, move,moves,line,bot)

@bot.message_handler(commands=['phonebook'])
def Phonebook(message):
    playing.logging(message,'')
    bot.send_message(message.chat.id,'Введите команду для работы с телефонной книгой'
                        '\n/view - для просмотра всех записей'
                        '\n/add - для добавления новой записи'
                        '\n/search - для вывода записей по критерию')

@bot.message_handler(commands=['view'])
def View_phonebook(message):
    playing.logging(message,'')
    bot.send_message(message.chat.id,phonebook.Print_phonebook(phonebook.Csv_read('phones.csv')))
    

@bot.message_handler(commands=['add'])
def Add_phonebook(message):
    playing.logging(message,'')   
    msg = bot.send_message(message.chat.id,'Введите фамилию, имя, отчество, телефон и его описание для нового контакта')
    bot.register_next_step_handler(msg, phonebook.Add_phonebook_2,bot)

@bot.message_handler(commands=['search'])
def Search_phonebook(message):
    playing.logging(message,'')
    msg = bot.send_message(message.chat.id,'Введите, что нужно найти')
    bot.register_next_step_handler(msg, phonebook.Search_phonebook_2,bot)
    

@bot.message_handler(commands=['text'])
def Calc(message):
    playing.logging(message,'')
    with open("text.txt", encoding="utf-8") as inputFile:
        input_list = [row.strip() for row in inputFile]
    bot.send_message(message.chat.id,input_list[randint(0,len(input_list)-1)])
    
bot.polling(none_stop=True, interval=0)
