

import random
import json
import os

from ..data_layer import *

path = os.path.dirname(os.path.abspath(__file__)) # Получение текущего пути к файлу
file = open(f"{path}/hsk.json", "rb") # Открытие словаря для получения слов
hsk = json.load(file)  # Разбираем полученные JSON данные в читабельный формат
hanzi = ["爱", "ai", "любовь"] 

path = os.path.dirname(os.path.abspath(__file__)) # Получение текущего пути к файлу
file = open(f"{path}/hsk.json", "rb") # Открытие словаря для получения слов
hsk = json.load(file)  # Разбираем полученные JSON данные в читабельный формат

async def irg_generate(name,password,mode='off'):
    sub_level = await db_get_data(name,password)
    if mode=='off':

        wordlist = ""

        word_index = 0
        selected_word = list()

        while (word_index <= sub_level[3]):
            selected_word.append(hsk[word_index])
            word_index+=1

        r = random.randint(0, len(selected_word)-1)
        a = selected_word[r]["hanzi"]
        b = selected_word[r]["pinyin"]
        c = selected_word[r]["translations"]["rus"][0]
        db_update_hanzi(a,b,name,password)
        return [a, b, c]


    if mode=='user_dictionary':

        wordlist = await db_get_user_dictionary(name, password)
        if wordlist[0] is not '':
            r = random.randint(0, len(wordlist)-1)
            a = wordlist[r][0]
            b = wordlist[r][1]
            c = wordlist[r][2]
            db_update_hanzi(a,b,name,password)
            return [a, b, c]
        else:
            return ['not_dictionary',"Не задан пользовательский список слов."]


    else:
        wordlist = await db_update_wordlist(name, password,'-',0)

        word_index = 0
        selected_word = list()
        word_index = 0
        selected_word = list()

        while (word_index <= sub_level[3]):
            if hsk[word_index]["hanzi"] not in wordlist.values():
                selected_word.append(hsk[word_index])
            word_index+=1
        while (word_index <= sub_level[3]):
            if hsk[word_index]["hanzi"] not in wordlist.values():
                selected_word.append(hsk[word_index])
            word_index+=1

        r = random.randint(0, len(selected_word)-1)
        a = selected_word[r]["hanzi"]
        b = selected_word[r]["pinyin"]
        c = selected_word[r]["translations"]["rus"][0]
        db_update_hanzi(a,b,name,password)
        return [a, b, c]
        r = random.randint(0, len(selected_word)-1)
        a = selected_word[r]["hanzi"]
        b = selected_word[r]["pinyin"]
        c = selected_word[r]["translations"]["rus"][0]
        db_update_hanzi(a,b,name,password)
        return [a, b, c]


async def kanzi_text_shuffle(hanzi_list, size):
    hanzi_text = list()
    for i in hanzi_list:
        hanzi_text.append(hanzi_list[i])
    random.shuffle(hanzi_text)

    return ''.join(hanzi_text)


async def get_hanzi_info(hanzi):
    i=0
    while i<len(hsk):
        if hanzi == hsk[i]['hanzi']:
            return (hsk[i]['hanzi'],hsk[i]['pinyin'],hsk[i]["translations"]["rus"][0])
        else:
            i+=1
    return ("Не найдено.","","")

