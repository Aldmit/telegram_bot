
import json
import sqlite3 as sq
from random import shuffle
from math import sqrt,ceil

hanzi = ["爱", "ai", "любовь"] 

async def db_create(): # Создание базы
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50), level int(1), sub_level int(4), progress int(5), streak int(8), hanzi varchar(50), pinyin varchar(50))")
    conn.commit()
    cur.close()
    conn.close()

    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS wordlist(id int auto_increment primary key, name varchar(50), pass varchar(50), hanzi varchar(100))")
    conn.commit()
    cur.close()
    conn.close()
    
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS textlist(id int auto_increment primary key, name varchar(50), pass varchar(50), text varchar(100), text_gen varchar(100))")
    conn.commit()
    cur.close()
    conn.close()

    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS user_dictionary(id int auto_increment primary key, id_user varchar(50), user_pass varchar(50), upload_words varchar(50000))")
    conn.commit()
    cur.close()
    conn.close()


# = = = = = = = INSERTS = = = = = = = = = =
    

async def db_insert_user(name, password): # Заведение нового пользователя
    name = name
    password = password
    level = 1
    sub_level = 10
    progress = 0 
    streak = 0
    hanzi = '-'
    pinyin = '-'

    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name,pass,level,sub_level,progress,streak,hanzi,pinyin) VALUES ('%s', '%s', '%i', '%i', '%i', '%i', '%s', '%s')" %(name,password,level,sub_level,progress,streak,hanzi,pinyin))
    conn.commit()
    cur.close()
    conn.close()

async def db_insert_wordlist(name, password): # Заведение новой таблицы слов
    name = name
    password = password
    hanzi = {0:'Твой список кандзи'}
    hanzi_json = json.dumps(hanzi)
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("INSERT INTO wordlist(name,pass,hanzi) VALUES ('%s', '%s', '%s')" %(name,password,hanzi_json))
    conn.commit()
    cur.close()
    conn.close()

async def db_insert_textlist(name, password): # Заведение новой таблицы слов
    name = name
    password = password
    text = ""
    text_gen = ""
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("INSERT INTO textlist(name,pass,text,text_gen) VALUES ('%s', '%s', '%s', '%s')" %(name,password,text,text_gen))
    conn.commit()
    cur.close()
    conn.close()

async def db_insert_user_dictionary(name, password): # Заведение новой таблицы слов
    name = name
    password = password
    upload_words = ""
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("INSERT INTO user_dictionary(id_user, user_pass, upload_words) VALUES ('%s', '%s', '%s')" %(name,password,upload_words))
    conn.commit()
    cur.close()
    conn.close()



# = = = = = = = GETS = = = = = = = = = =
    

async def db_get_data(name, password):
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("SELECT name,pass,level,sub_level,progress,streak,hanzi,pinyin FROM users WHERE name='%s' AND pass='%s'" %(name,password))
    users = cur.fetchall()
    cur.close()
    conn.close()
    # print('Get data ==-')
    return users[0]


async def db_get_textgen(name, password):
    
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("SELECT text_gen FROM textlist WHERE name='%s' AND pass='%s'" %(name,password))
    text_gen = cur.fetchall()
    cur.close()
    conn.close()

    return text_gen[0][0]


async def db_get_user_dictionary(name, password):
    
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("SELECT upload_words FROM user_dictionary WHERE id_user='%s' AND user_pass='%s'" %(name,password))
    upload_words = cur.fetchall()
    cur.close()
    conn.close()

    print('\n\n\nget1_json - - - ', upload_words)

    print('\n\n\nget2_json - - - ', upload_words[0][0])

    upload_words = json.loads(upload_words[0][0]) # Распаковать из json

    print('\n\n\nget_normal - - - ', upload_words)

    return upload_words
    

# = = = = = = = UPDATES = = = = = = = = = =
    

async def db_update_data(name,password,level,sub_level,progress,streak):
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("UPDATE users SET level = '%s',sub_level = '%s',progress = '%s',streak = '%s' WHERE name='%s' AND pass='%s'" %(level,sub_level,progress,streak,name,password))
    conn.commit()
    cur.close()
    conn.close()
    # print('Update data ==-')


def db_update_hanzi(hanzi,pinyin,name,password): # 
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("UPDATE users SET hanzi = '%s',pinyin = '%s' WHERE name='%s' AND pass='%s'" %(hanzi,pinyin,name,password))
    conn.commit()
    cur.close()
    conn.close()
    # print('Update hanzi ==-')


async def db_update_wordlist(name,password,hanzi,func_mode):
    # Отдаёт готовый список значений
    if func_mode == 0:
        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("SELECT hanzi FROM wordlist WHERE name='%s' AND pass='%s'" %(name,password))
        user_wordlist_json = cur.fetchall()
        cur.close()
        conn.close()

        hanzi_list = json.loads(user_wordlist_json[0][0])
        return hanzi_list
    
    # Добавляет новое слово в вордлист
    elif func_mode == 1:
        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("SELECT hanzi FROM wordlist WHERE name='%s' AND pass='%s'" %(name,password))
        user_wordlist_json = cur.fetchall()
        cur.close()
        conn.close()

        hanzi_list = json.loads(user_wordlist_json[0][0]) # Распаковать из json
        hanzi_list[len(hanzi_list)] = hanzi
        json_hanzi = json.dumps(hanzi_list) # Упаковать в json

        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("UPDATE wordlist SET hanzi = '%s' WHERE name='%s' AND pass='%s'" %(json_hanzi,name,password))
        conn.commit()
        cur.close()
        conn.close()

        await db_update_textlist(name,password)

        return f"Слово {hanzi} добавлено в словарь."
    
    # Удаляет слово из wordlist
    elif func_mode == -1:
        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("SELECT hanzi FROM wordlist WHERE name='%s' AND pass='%s'" %(name,password))
        user_wordlist_json = cur.fetchall()
        cur.close()
        conn.close()

        # print(f"JSON -- {user_wordlist_json[0][0]}")
        hanzi_list = json.loads(user_wordlist_json[0][0]) # Распаковать из json

        new_list = dict()
        for i in hanzi_list:
            if i == 0 and hanzi_list[i] != hanzi: 
                print(i,' >> ',hanzi_list[i],' >> ',hanzi)
                new_list[len(new_list)] = hanzi_list[i]

            if hanzi_list[i] != hanzi:
                print(i,' => ',hanzi_list[i],' => ',hanzi)
                new_list[len(new_list)] = hanzi_list[i]

        # print(f"NO JSON -- {new_list}")
        
        json_hanzi = json.dumps(new_list) # Упаковать в json

        conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("UPDATE wordlist SET hanzi = '%s' WHERE name='%s' AND pass='%s'" %(json_hanzi,name,password))
        conn.commit()
        cur.close()
        conn.close()

        await db_update_textlist(name,password)

        return f"Слово {hanzi} удалено из словаря."



async def db_update_textlist(name,password):

    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("SELECT hanzi FROM wordlist WHERE name='%s' AND pass='%s'" %(name,password))
    text_json = cur.fetchall()
    cur.close()
    conn.close()

    hanzi_list = json.loads(text_json[0][0]) # Распаковать из json
    hanzi_text = ','.join(hanzi_list.values()).split(',') # cоздаём массив для перемешки
    shuffle(hanzi_text)

    # print(f"\n === 1 === \n{hanzi_text}\n\n")
    # print(f"\n === 2 === \n{len(hanzi_text)}\n\n")
    # print(f"\n === 3 === \n{sqrt(len(hanzi_text))}\n\n")
    # print(f"\n === 4 === \n{int(ceil(sqrt(len(hanzi_text))))}\n\n")
    # print(f"\n === 5 === \n{hanzi_text[:int(ceil(sqrt(len(hanzi_text))))]}\n\n")

    # hanzi_text = ','.join(hanzi_text[:int(ceil(sqrt(len(hanzi_text))))]) # готовый перемешанный текст

    hanzi_text = ','.join(hanzi_text[:5]) # готовый перемешанный текст

    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("UPDATE textlist SET text='%s',text_gen='%s' WHERE name='%s' AND pass='%s'" %(text_json[0][0],hanzi_text,name,password))
    conn.commit()
    cur.close()
    conn.close()

    return hanzi_text


async def db_update_user_dictionary(name,password,upload_words):
    
    # Получаем сырой текст, парсим и заворачиваем в json

    upload_words = upload_words.replace('\n','').split('* ')
    upload_words.pop(0)
    
    for i in range(len(upload_words)):
        upload_words[i] = upload_words[i].split(' - ')

    
    print('upload_words - - - ', upload_words)

    
    json_pack = json.dumps(upload_words) # Упаковать в json
    
    conn = sq.connect("database.sql") # Работа с подключением к БД через встроенный import sq
    cur = conn.cursor()
    cur.execute("UPDATE user_dictionary SET upload_words='%s' WHERE id_user='%s' AND user_pass='%s'" %(json_pack,name,password))
    conn.commit()
    cur.close()
    conn.close()

    print('update - - - ', json_pack)

    return f"Пользовательский список слов обновлён."
    