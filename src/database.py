r"""The Database class has the following methods:

    - get_data(self, data: str) - Получает все данные из таблицы по ключу пользователя и названию таблицы
    - update_data(self, data: str, json_data: str) -> bool - Обновляет таблицу table данными из массива arr
    - insert_user(self) -> None - Добавляет пользователя в базу, создавая запись о нём в таблицы
    - create_tables(self) -> None - Создаёт таблицы users, wordlist, user_dictionary

"""
#'
import sqlite3 as sq
import os
import json

class Database:
    
    def __init__(self, chat_id: str):
        self._user = chat_id
        path = os.path.dirname(os.path.abspath(__file__)) # Получение текущего пути к файлу
        self.__bd_name = path+"/data/database.sql"

    def get_data(self, data: str):
        # Получение данных поля пользователя (user_id(str) language(str) ru_settings(dict) zh_srttings(dict) ru_wordlist(dict) zh_wordlist(dict) user_dictionary(dict) word(dict))
        conn = sq.connect(self.__bd_name)
        cur = conn.cursor()
        request = f"SELECT {data} FROM users WHERE user_id={self._user}"
        cur.execute(request)
        user_data = cur.fetchall()
        cur.close()
        conn.close()

        try:
            user_data = list(user_data[0])

            match data:
                case "user_id":
                    return user_data[0]
                case "language":
                    return user_data[0]
                case "*":
                    user_id = user_data[0]
                    language = user_data[1]
                    ru_settings = json.loads(user_data[2])
                    zh_settings = json.loads(user_data[3])
                    ru_wordlist = json.loads(user_data[4])
                    zh_wordlist = json.loads(user_data[5])
                    user_dictionary = json.loads(user_data[6])
                    word = json.loads(user_data[7])
                
                    return [user_id, language, ru_settings, zh_settings, ru_wordlist, zh_wordlist, user_dictionary, word]
                
                case _:
                    return json.loads(user_data[0])
                    
        except:
            return user_data
    
    
    def update_data(self, data: str, json_data: str) -> bool:
        match data:
            case 'language':  
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                cur.execute("UPDATE users SET language = '%s' WHERE user_id='%s'" %(json_data, self._user))
                conn.commit()
                cur.close()
                conn.close()
                return True
              
            case 'ru_settings':  
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                cur.execute("UPDATE users SET ru_settings = '%s' WHERE user_id='%s'" %(json_data, self._user))
                conn.commit()
                cur.close()
                conn.close()
                return True
             
            case 'zh_settings':  
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                cur.execute("UPDATE users SET zh_settings = '%s' WHERE user_id='%s'" %(json_data, self._user))
                conn.commit()
                cur.close()
                conn.close()
                return True
        
            case 'ru_wordlist':  
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                cur.execute("UPDATE users SET ru_wordlist = '%s' WHERE user_id='%s'" %(json_data, self._user))
                conn.commit()
                cur.close()
                conn.close()
                return True
            
            case 'zh_wordlist':  
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                cur.execute("UPDATE users SET zh_wordlist = '%s' WHERE user_id='%s'" %(json_data, self._user))
                conn.commit()
                cur.close()
                conn.close()
                return True
            
            case 'user_dictionary':  
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                cur.execute("UPDATE users SET user_dictionary='%s' WHERE user_id='%s'" %(json_data, self._user))
                conn.commit()
                cur.close()
                conn.close()
                return True
            
            case 'word':  
                conn = sq.connect(self.__bd_name)
                cur = conn.cursor()
                cur.execute("UPDATE users SET word='%s' WHERE user_id='%s'" %(json_data, self._user))
                conn.commit()
                cur.close()
                conn.close()
                return True
            case _:
                return False
    
    
    def insert_user(self) -> None:
        user_id = self._user
        language = ""
        ru_settings = json.dumps({"level":1, "sub-level":10, "progress":0, "streak":0, "language":""})
        zh_settings = json.dumps({"level":1, "sub-level":10, "progress":0, "streak":0, "language":""})
        ru_wordlist = json.dumps({0:"Твой список кандзи"})
        zh_wordlist = json.dumps({0:"你的单词列表"})
        user_dictionary = json.dumps({0:""})
        word = json.dumps({"word":"","transcription":"","translate":"","description":""})

        
        conn = sq.connect(self.__bd_name) # Работа с подключением к БД через встроенный import sq
        cur = conn.cursor()
        cur.execute("INSERT INTO users(user_id,language,ru_settings,zh_settings,ru_wordlist,zh_wordlist,user_dictionary,word) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(user_id,language,ru_settings,zh_settings,ru_wordlist,zh_wordlist,user_dictionary,word))
        conn.commit()
        cur.close()
        conn.close()

    
    def create_tables(self) -> None:

        conn = sq.connect(self.__bd_name) # USERS
        cur = conn.cursor()
        cur.execute(f'''CREATE TABLE IF NOT EXISTS users (
                    user_id varchar(100) primary key, 
                    language varchar(30),
                    ru_settings varchar(100),
                    zh_settings varchar(100),
                    ru_wordlist varchar(50000),
                    zh_wordlist varchar(50000),
                    user_dictionary varchar(10000),
                    word varchar(300)
                    )''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tab users have created\n\n")
        