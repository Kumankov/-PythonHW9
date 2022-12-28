from random import randint
import logging
from datetime import datetime

def logging(message,comment):
    file = open('log.csv','a')
    time = datetime.utcfromtimestamp(int(message.date)+10800).strftime('%Y-%m-%d %H:%M:%S')
    file.write(f'{time};{message.from_user.id};{message.from_user.first_name};{message.from_user.username};{message.from_user.last_name};{message.text};{comment}\n')
    file.close

def lineWin(line, symbol):    
    return(line[0][0] == line[0][1] == line[0][2] == symbol 
        or line[1][0] == line[1][1] == line[1][2] == symbol 
        or line[2][0] == line[2][1] == line[2][2] == symbol 
        or line[0][0] == line[1][0] == line[2][0] == symbol 
        or line[0][1] == line[1][1] == line[2][1] == symbol 
        or line[0][2] == line[1][2] == line[2][2] == symbol 
        or line[0][0] == line[1][1] == line[2][2] == symbol 
        or line[0][2] == line[1][1] == line[2][0] == symbol) 

def Tttfinish(winX, win0, draw):
    if winX:
        return ('Вы выиграли!')
    elif win0:
        return ('Я выиграл!')
    elif draw:
        return ('Ничья! Игра окончена')   

def Print_field(line):
    return(f'{line[0][0]} | {line[0][1]} | {line[0][2]}'
            '\n_________'
            f'\n{line[1][0]} | {line[1][1]} | {line[1][2]}'
            '\n_________'
            f'\n{line[2][0]} | {line[2][1]} | {line[2][2]}')

def Check_end_game(bot,message,line,moves):
    if lineWin(line,'X') or lineWin(line,'0') or len(moves) == 9: 
        bot.send_message(message.chat.id, Tttfinish(lineWin(line,'X'),lineWin(line,'0'),len(moves) == 9))
        bot.send_message(message.chat.id, Print_field(line))
        moves = []
        line = [['  ',' ',' '],['   ',' ',' '],['   ',' ',' ']]                   
        exit()


def Candy_2(message,bot,candys):
    logging(message,'')
    move = 0
    while candys > 0:
        if message.text.isdigit():            
            move = int(message.text)
            if move > 28 or move < 1 or move > candys:                 
                msg = bot.send_message(message.chat.id,'Некорректный ход.\nВведите количество конфет от 1 до 28 \nНо не более, чем лежит на столе')                
                bot.register_next_step_handler(msg, Candy_2,bot,candys)
                return    
            else:
                candys -= move
                if candys == 0:
                    bot.send_message(message.chat.id,'Игра окончена. Вы выиграли')
                    candys = 2021
                    return      
                elif candys > 0: 
                    bot.send_message(message.chat.id,f'Остаток конфет на столе - {candys}')
                    if candys%29:               
                        move = candys%29
                    else:
                        move = randint(1,28)
                    candys -= move
                    bot.send_message(message.chat.id,f'Я беру {move} конфет.\nОстаток конфет на столе - {candys}')                    
                    if candys == 0:
                        bot.send_message(message.chat.id,'Я выиграл.')
                        candys = 2021
                        return
            msg = bot.send_message(message.chat.id,'Введите количество конфет от 1 до 28')      
            bot.register_next_step_handler(msg, Candy_2,bot,candys)
            return
        else:
            if message.text == 'exit':
                bot.send_message(message.chat.id,'Вы вышли из игры')
                return
            else:
                msg = bot.send_message(message.chat.id, 'Введите число')
                bot.register_next_step_handler(msg, Candy_2,bot,candys)
                return                                

def Ttt_2(message,move,moves,line,bot):
    logging(message,'')
    move0 = [0]*2
    
    for i in range(2):
        if not i%2:
            move[i] = message.text.split()
            if message.text == 'exit':
                bot.send_message(message.chat.id,'Вы вышли из игры')
                return
            elif len(move[i]) < 2 or int(move[i][0]) not in [1,2,3] or int(move[i][1]) not in [1,2,3] or not map(lambda x:x.isdigit(),move[i]):
                msg = bot.send_message(message.chat.id,'Некорректный ход.\nВведите координаты вида 1 2 через пробел')                
                bot.register_next_step_handler(msg, Ttt_2,move,moves,line,bot)
                return       
            elif move[i] in moves:
                msg = bot.send_message(message.chat.id,'Такой ход уже был.\nВведите координаты вида 1 2 через пробел')            
                bot.register_next_step_handler(msg, Ttt_2,move,moves,line,bot)
                return    
            else:
                moves.append(move[i])
                line[int(move[i][0])-1][int(move[i][1])-1] = 'X'
            if len(moves)>3:
                Check_end_game(bot,message,line,moves)                          
        elif i%2:
            move0[0] = str(randint(1,3))
            move0[1] = str(randint(1,3))
            while move0 in moves:
                move0[0] = str(randint(1,3))
                move0[1] = str(randint(1,3))
            move[i]=move0
            moves.append(move[i])
            line[int(move[i][0])-1][int(move[i][1])-1] = '0'    
            if len(moves)>3:
                Check_end_game(bot,message,line,moves)   
            msg = bot.send_message(message.chat.id,Print_field(line))                
            bot.register_next_step_handler(msg, Ttt_2,move,moves,line,bot)
            return   
            
