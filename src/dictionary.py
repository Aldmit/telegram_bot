r"""The WordGenerator class has the following methods:

    - get_word_by_index(self, index='1') - Получает слово по его индексу в словаре
    - get_word_info(self, word) - получает информацию о слове из словаря
    - get_random_word(self,mode='0') - Генерирует случайное слово из заданных диапазонов
        mode = wordlist - Генерирует слово для повторения из вордлиста
        mode = user_dictionary -Генерирует слово для повторения из пользовательского словаря
        mode = 0 - Генерирует слово для повторения из основного словаря, исключая слова в вордлисте
    

"""

import random
from .user import *
from .handlers import JsonConverter
import os

class Comment:
    def get_comments_ftom_file(self):
        file = os.path.dirname(os.path.abspath(__file__))+"/data/comments.json"# Получение текущего пути к файлу
        raw_file = open(f"{file}", mode="r", encoding="utf-8") # Открытие сырого словаря для формирования json
        json_file = raw_file.read()
        raw_file.close()
        x = json.loads(json_file)
        return x[0]
    
    def get_comment(self, lang:str, number_of_comment:str):
        y = self.get_comments_ftom_file()
        lang = str(lang)
        number = str(number_of_comment)
        x = y[number][lang]
        return x
        

class WordGenerator:
    def __init__(self, id: str) -> None:
        self._id = id
        self._user = User(id) 
        self._dictionary = ''

        match self._user._language:
            case 'ru':
                self._dictionary = JsonConverter("data/hsk_dictionary.json").j2o()  # Массив объектов Character[i].attr
            case 'zh':
                self._dictionary = JsonConverter("data/zh_dictionary.json").j2o()  # Массив объектов Character[i].attr

    def get_word_by_index(self, index='1'):
        return self._dictionary[index]
    

    def get_word_info(self, word):
        i=0
        if self._user._language == 'ru':
            '''ru'''
            while i < len(self._dictionary):
                if word == self._dictionary[i].zh:
                    return self._dictionary[i]
                else:
                    i+=1
            return ("Не найдено.","","")
        
        elif self._user._language == 'zh':
            '''zh'''
            while i < len(self._dictionary):
                if word == self._dictionary[i].ru:
                    return self._dictionary[i]
                else:
                    i+=1
            return ("Не найдено.","","")


    def get_random_word(self,mode='0'):
        match mode:
            case 'wordlist':
            # Генерация случайного иероглифа из вордлиста для повторения
                try:
                    wordlist = self._user.update_wordlist(0,'-',self._user._language)

                    data_name = self._user._language+"_settings"
                    user_data = self._user._data.get_data(data_name)
                    word_index = 0
                    selected_word = list() 
                    
                    if self._user._language == 'ru':
                        while (word_index <= user_data['sub-level']):
                            if self._dictionary[word_index].zh in wordlist.values():
                                selected_word.append(self._dictionary[word_index])
                            word_index+=1
                    
                    elif self._user._language == 'zh':
                        while (word_index <= user_data['sub-level']):
                            if self._dictionary[word_index].ru in wordlist.values():
                                selected_word.append(self._dictionary[word_index])
                            word_index+=1

                    r = random.randint(0, len(selected_word)-1)

                    if self._user._language == 'ru':
                        self._user.update_word(selected_word[r].zh,selected_word[r].py,selected_word[r].translate['ru'],'')
                        return [selected_word[r].zh,selected_word[r].py,selected_word[r].translate['ru']]
                    
                    if self._user._language == 'zh':
                        self._user.update_word(selected_word[r].ru,'',selected_word[r].zh,'')
                        return [selected_word[r].zh,selected_word[r].ru]
                
                except:
                    if self._user._language == 'ru':
                        return "Повторять нечего, сперва добавь несколько слов в режиме изучения"
                    
                    elif self._user._language == 'zh':
                        return "Повторять нечего, сперва добавь несколько слов в режиме изучения"
                


            case 'user_dictionary':
            # Генерация случайного иероглифа из пользовательского словаря

                try:
                    if self._user._language == 'ru':
                        wordlist = self._user.get_user_dictionary()

                        if wordlist[0] is not '':
                            r = random.randint(0, len(wordlist)-1)

                            word = list()
                            word = [i for i in wordlist[r]]

                            index = len(word)
                            if index == 2:
                                self._user.update_word(word(0),'',word(1),'')
                                return [word[0],word[1]]
                            if index == 3:
                                self._user.update_word(word[0],word[1],word[2],'')
                                return [word[0],word[1],word[2]]
                            
                    elif self._user._language == 'zh':
                        wordlist = self._user.get_user_dictionary()

                        if wordlist[0] is not '':
                            r = random.randint(0, len(wordlist)-1)

                            word = list()
                            word = [i for i in wordlist[r]]

                            self._user.update_word(word[0],'',word[1],'')
                            return [word[0],word[1]]
                        
                except:
                    return ['not_dictionary',"Не задан пользовательский список слов."]

            
            case _:
            # Генерация случайного иероглифа из словаря по умолчанию
                word_index = 0
                selected_word = list()

                data_name = self._user._language + "_settings"
                user_data = self._user._data.get_data(data_name)
                wordlist = self._user.update_wordlist(0,'-',self._user._language)

                if self._user._language == 'ru':
                    while (word_index <= int(user_data['sub-level'])):
                        if self._dictionary[word_index].zh not in wordlist.values():
                            selected_word.append(self._dictionary[word_index])
                        word_index+=1
                
                elif self._user._language == 'zh':
                    while (word_index <= user_data['sub-level']):
                        if self._dictionary[word_index].ru not in wordlist.values():
                            selected_word.append(self._dictionary[word_index])
                        word_index+=1

                
                if len(selected_word) == 0:
                    word_index+=1
                    selected_word.append(self._dictionary[word_index])
                    
                r = random.randint(0, len(selected_word)-1)

                if self._user._language == 'ru':
                    self._user.update_word(selected_word[r].zh, selected_word[r].py, selected_word[r].translate['ru'], "")
                    return [selected_word[r].zh, selected_word[r].py, selected_word[r].translate['ru']]
                
                elif self._user._language == 'zh':
                    self._user.update_word(selected_word[r].ru, '', selected_word[r].zh, "")
                    return [selected_word[r].zh, selected_word[r].ru]
                