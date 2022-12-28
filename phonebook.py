import playing
import csv

def Csv_read(file):
    list=[]
    with open(file, 'r', newline='') as csvfile:    
        for row in csv.reader(csvfile, delimiter=';'):
            list.append(row)
    return(list)        

def Csv_write(list, file):
    with open(file, 'w', newline='') as csvfile:
        csv.writer(csvfile, delimiter=';').writerows(list)    

def Print_phonebook(list):
    str = ''
    for i in range(len(list)):
        if len(list[i]) == 1:
            str += list[i] + ' '
        else:    
            for j in range(len(list[i])):
                str += list[i][j] + ' '
            str +='\n' 
    return(str)

def Add_phonebook_2(message,bot):
    playing.logging(message,'')
    new_phone = message.text.split()
    phone_list = Csv_read('phones.csv')
    phone_list.append(new_phone)
    new_contact_str = ' '.join(map(str, new_phone))
    msg = bot.send_message(message.chat.id,f'Новый контакт - {new_contact_str}\nХотите записать справочник?\nВведите Да - для записи')
    bot.register_next_step_handler(msg, Add_phonebook_3,phone_list,bot)

def Add_phonebook_3(message,phone_list,bot):
    playing.logging(message,'')
    if message.text.lower() == 'да':
        Csv_write(phone_list, 'phones2.csv')
        bot.send_message(message.chat.id,'Телефонная книга сохранена')
    else:
        bot.send_message(message.chat.id,'Изменения не сохранены')
        return   

def Search_phonebook_2(message,bot):
    playing.logging(message,'')
    search_phonebook = []
    phone_list = Csv_read('phones.csv')
    for row in phone_list:
        for i in range(len(row)):
            if message.text.lower() in row[i].lower():
                search_phonebook.append(row)
    if len(search_phonebook) == 0:
        bot.send_message(message.chat.id,'Ничего не найдено')
    else:
        bot.send_message(message.chat.id,Print_phonebook(search_phonebook))
 