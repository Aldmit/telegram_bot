

import random
import json
import os

from ..db_functions import *

path = os.path.dirname(os.path.abspath(__file__)) # Получение текущего пути к файлу
file = open(f"{path}/hsk.json", "rb") # Открытие словаря для получения слов
hsk = json.load(file)  # Разбираем полученные JSON данные в читабельный формат
hanzi = ["爱", "ai", "любовь"] 

path = os.path.dirname(os.path.abspath(__file__)) # Получение текущего пути к файлу
file = open(f"{path}/hsk.json", "rb") # Открытие словаря для получения слов
hsk = json.load(file)  # Разбираем полученные JSON данные в читабельный формат

async def irg_generate(name,password):
    sub_level = await db_get_data(name,password)
    wordlist = await db_update_wordlist(name, password,'-',0)

    word_index = 0
    selected_word = list()

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

    # r = random.randint(0, sub_level[3])
    # if hsk[r]["hanzi"] not in wordlist.values():  # проверка на словарь
    #     a = hsk[r]["hanzi"]
    #     b = hsk[r]["pinyin"]
    #     c = hsk[r]["translations"]["rus"][0]
    #     db_update_hanzi(a,b,name,password)
    #     # print('Работает else')
    #     return [a, b, c]
    # else:
    #     return await irg_generate(name,password)
    
    # print(f'Проверка числа в генераторе {sub_level[3]},{sub_level[4]} += Проверка данныз из wordlist: {wordlist}')
    # if sub_level[3] > 15:
    #     r = random.randint(sub_level[3]-15, sub_level[3])
    #     if hsk[r]["hanzi"] not in wordlist.values():
    #         a = hsk[r]["hanzi"]
    #         b = hsk[r]["pinyin"]
    #         c = hsk[r]["translations"]["rus"][0]
    #         db_update_hanzi(a,b,name,password)
    #         print('Работает sub_level')
    #         return [a, b, c]
    #     else:
    #         return await irg_generate(name,password)
    # else:




async def kanzi_text_shuffle(hanzi_list, size):
    hanzi_text = list()
    for i in hanzi_list:
        hanzi_text.append(hanzi_list[i])
    random.shuffle(hanzi_text)

    return ''.join(hanzi_text)

