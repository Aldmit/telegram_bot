r"""The User class has the following methods:

    - checking_existing_user(self) -> bool - Проверяет пользователя в базе, если его нет - делает INSERT

    - set_language(self, language: str) - Устанавливает язык работы в приложении
    - get_language(self) -> str - Возвращает установленный язык пользователя
    - get_user_info(self) - Отдаёт массив данных пользователя
    - get_user_dictionary(self) -> str - Отдаёт массив данных пользовательского словаря

    - update_user_dictionary(self, upload_words) -> str - Обновляет пользовательский словарь
    - update_word(self, word:str = "", transcription:str = "", translate:str = "", description:str = "") - Обновляет текущее слово пользователя
    - update_wordlist(self, func_mode: int, word: str, lang: str = '') - По параметру lang определяет, какой обработчик словаря запустить следующим

    - update_wordlist_ru(self, func_mode: int, word: str) - Работает с русским пользовательским словарем (в словаре китайские слова)
    - update_wordlist_zh(self, func_mode: int, word: str) - Работает с китайским пользовательским словарем (в словаре русские слова)

"""
#'
import json
from .database import *

class User:
    def __init__(self, id: str):
        self._id = id
        self._data = Database(self._id)
        self._language = self.get_language()


    def checking_existing_user(self) -> bool:
        try:
            if Database(self._id).get_data('user_id') == str(self._id):
                print("User already exist.")
                return True
            else:
                Database(self._id).insert_user()
                print("User has created.")
                return False
        except:
            Database(self._id).insert_user()
            print("User has created.")
            return False
    

    def set_language(self, language: str):
        return self._data.update_data('language',language)
    
    def get_language(self) -> str:
        return self._data.get_data('language')


    def get_user_info(self):
        return self._data.get_data('*')
    

    def get_user_dictionary(self) -> str:
        upload_words = self._data.get_data('user_dictionary')
        return upload_words


    def update_user_dictionary(self, upload_words) -> str:
        # Получаем сырой текст, парсим и заворачиваем в json

        upload_words = upload_words.replace('\n','').split('* ')
        upload_words.pop(0)
        
        for i in range(len(upload_words)):
            upload_words[i] = upload_words[i].split(' - ')

        json_pack = json.dumps(upload_words) # Упаковать в json

        self._data.update_data('user_dictionary', json_pack)
        return f"Пользовательский список слов обновлён."


    def update_word(self, word:str = "", transcription:str = "", translate:str = "", description:str = ""):
        json_data = self._data.get_data('word')
        # json_data = json.loads(json_data)

        json_data['word'] = word
        json_data['transcription'] = transcription
        json_data['translate'] = translate
        json_data['description'] = description

        json_pack = json.dumps(json_data) # Упаковать в json
        self._data.update_data('word', json_pack)



    def update_wordlist(self, func_mode: int, word: str, lang: str = ''):
        match lang:
            case 'ru':
                return self.update_wordlist_ru(func_mode, word)
            case 'zh':
                return self.update_wordlist_zh(func_mode, word)
            

    def update_wordlist_ru(self, func_mode: int, word: str):
        match func_mode:
            case 0: # Отдаёт готовый список значений
                word_list = self._data.get_data('ru_wordlist')
                return word_list
            

            case 1: # Добавляет новое слово в вордлист, гарантирует что у пользователя не останется ноль слов в изучении
                word_list = self._data.get_data('ru_wordlist')
                user_info = self._data.get_data("ru_settings")

                if word in word_list.values():                
                    return f"Слово {word} уже добавлено в словарь."
                
                if user_info['sub-level'] <= len(word_list):
                    return f"В изучении должно быть хотя бы одно слово! Сперва открой новое слово."

                word_list[len(word_list)] = word
                json_word = json.dumps(word_list) # Упаковать в json

                self._data.update_data('ru_wordlist', json_word)
                return f"Слово {word} добавлено в словарь и скрыто :3"
                
            
            case -1: # Удаляет слово из wordlist
                word_list = self._data.get_data('ru_wordlist')
                new_word_list = []
                word_list = list(word_list.values()) # Потому что иначе индексы элементов будут удаляться и не выстраиваться по порядку. Со списком работать проще, а словарь очень топорный в этом плане.
                try: 
                    word_list.remove(word)
                    
                    i = 0
                    for i in range(len(word_list)):
                        new_word_list.append([i, word_list[i]]) 
                        i+=1

                    word_list = dict(new_word_list)
                    json_word = json.dumps(word_list) # Упаковать в json
                    self._data.update_data('ru_wordlist',json_word)
                    return f"Слово {word} удалено из словаря."
                
                except:
                    return f"Кадзи не найдено"




    def update_wordlist_zh(self, func_mode: int, word: str):
        match func_mode:
            case 0: # Отдаёт готовый список значений
                word_list = self._data.get_data('zh_wordlist')
                return word_list
            
            case 1: # Добавляет новое слово в вордлист
                word_list = self._data.get_data('ru_wordlist')
                user_info = self._data.get_data("ru_settings")
        
                word_list[len(word_list)] = word
                json_word = json.dumps(word_list) # Упаковать в json

                if word in word_list.values():                
                    return f"单词 {word} 已在词典中。"
                
                if user_info['sub-level'] <= len(word_list):
                    return f"书房里至少要有一个字！首先，发现一个新词。"

                word_list[len(word_list)] = word
                json_word = json.dumps(word_list) # Упаковать в json

                self._data.update_data('zh_wordlist', json_word)
                return f"{word} 一词已被添加到字典中."
                
            
            case -1: # Удаляет слово из wordlist
                word_list = self._data.get_data('zh_wordlist')

                new_list = dict()
                for i in word_list:
                    if i == 0 and word_list[i] != word: 
                        new_list[len(new_list)] = word_list[i]

                    if word_list[i] != word:
                        new_list[len(new_list)] = word_list[i]

                json_word = json.dumps(new_list) # Упаковать в json

                self._data.update_data('zh_wordlist',json_word)
                return f"{word} 这个词已从字典中删除."

