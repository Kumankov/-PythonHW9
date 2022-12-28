# import logging
import playing
# from datetime import datetime

def Calculator(list, type):
            if list[1] =='*':
                result = type(list[0]) * type(list[2])
            elif list[1] =='/':
                result = type(list[0]) / type(list[2])
            elif list[1] =='+':
                result = type(list[0]) + type(list[2])
            else:
                result = type(list[0]) - type(list[2])
            return(result)

def Calc_2(message,bot):  
    playing.logging(message,'')
    input_list = message.text.split()
    if len(input_list) == 3 and input_list [1] in ['*','/','+','-']: 
        try:
            result = Calculator(input_list,float)
            msg = bot.reply_to(message, f'{result}\nВведите другое выражение для подсчета или exit для выхода')
            bot.register_next_step_handler(msg, Calc_2,bot)
            playing.logging(message,result)
        except Exception as e:
            msg = bot.reply_to(message, 'Ошибка.\nВведите другое выражение для подсчета или exit для выхода')
            bot.register_next_step_handler(msg, Calc_2,bot)          
    elif message.text == 'exit':
        bot.send_message(message.chat.id,'Выход')
    else:
        msg = bot.reply_to(message, 'Ошибка в выражении.\nВведите другое выражение для подсчета или exit для выхода')
        bot.register_next_step_handler(msg, Calc_2,bot)     

def Second_calc_2(message,bot,calc_list,check_complex):  
    playing.logging(message,'')  
    calc_list.append(message.text)
    if message.text == 'exit':
        bot.send_message(message.chat.id,'Выход')
        calc_list = []
        return   
    if 'j' in message.text:
        check_complex = True
    if len(calc_list) == 1:
        msg = bot.send_message(message.chat.id,'Введите действие или exit для выхода')
        bot.register_next_step_handler(msg, Second_calc_2,bot,calc_list,check_complex)
        return
    elif len(calc_list) == 2:
        msg = bot.send_message(message.chat.id,'Введите второе число или exit для выхода')
        bot.register_next_step_handler(msg, Second_calc_2,bot,calc_list,check_complex)
        return
    else:
        if calc_list[1] in ['*','/','+','-']:
            try:
                if check_complex:
                    result = Calculator(calc_list,complex)
                else:
                    result = Calculator(calc_list,float)
                playing.logging(message,result)
                msg = bot.send_message(message.chat.id,f'{result}\nВведите введите новое первое число или exit для выхода')
                calc_list = []
                bot.register_next_step_handler(msg, Second_calc_2,bot,calc_list,check_complex)
                return
            except Exception as e:
                msg = bot.reply_to(message, 'Ошибка.\nВведите введите новое первое число или exit для выхода')
                calc_list = []
                bot.register_next_step_handler(msg, Second_calc_2,bot,calc_list,check_complex)       
                return
        else: 
            msg = bot.reply_to(message, 'Ошибка.\nВведите введите новое первое число или exit для выхода')
            calc_list = []
            bot.register_next_step_handler(msg, Second_calc_2,bot,calc_list,check_complex)       
            return    
