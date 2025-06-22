r"""The JsonConverter class has the following methods:

    - j2o(self, json_data: str = "")- Возвращает массив, принимая на вход json-cловарь
    - o2j(self, object_array: list) - Возвращает упакованный json, принимая на вход массив

"""
#'
import json
import os

# t2j() - переводит размеченный файл формата txt в json-словарь, пригодный для изучения иностранного языка
# Также переводит json-словарь в массив объектов для работы приложения

class Character:
    def __init__(self, level: str, id: str, zh: str, py: str, translate) -> None:
        self.level = level
        self.id = id
        self.zh = zh
        self.py = py
        self.translate = {'en': translate[0], 'ru': translate[1]}


class Word:
    def __init__(self, level: str, id: str, zh: str, pinyin: str, ru: str, tcribe: str,  defi_zh: str, defi_ru: str) -> None:
        self.level = level
        self.id = id
        self.zh = zh
        self.pinyin = pinyin
        self.ru = ru
        self.tcribe = tcribe
        self.defi_zh = defi_zh
        self.defi_ru = defi_ru
        

class JsonConverter:
    def __init__(self, file_name: str = 'none') -> None:
        self._file = file_name

    def f2j(self):
    # Создаёт из подготовленного файла со словами новый словарь
        '''
            Обязательная структура файла - кадое слово должно быть записано так//

            * 1 - 24 - 桌子 - zhuo4zi - стол - stol - Мебель для письма или еды - 用于书写或进餐的家具 \n

            1. Уровень слова в системе словаря (это может быть уровень HSK или CEFR, главное чтобы он был определён в нужную группу слова)
            2. Порядковый номер слова (1++) нужен чтобы по нему можно было отследить нужное слово
            3. Слово на изучаемом языке
            4. Транскрипция изучаемого слова (как оно пишется, читается, звучит)
            5. Перевод слова на нужный язык (сейчас реализую ru-zh, в будущем над расширением языкового модуля будем думать отдельно)
            6. Транскрипция слова-перевода (как оно пишется, читается, звучит)
            7. Определение на русском
            8. Определение на китайском

            Требования к тексту, знакам и пунктуации//

            В китайских словах необходимо использовать китайские знаки припенания без пробелов: 我们，你的猫
            В русских словах если и используются знаки припенания, то с пробелами: мы, твой кот
            Все слова должны быть написаны с маленькой буквы

        '''
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Получение текущего пути к файлу

        raw_file = open(f"{path}/data/{self._file}", mode="r", encoding="utf-8") # Открытие сырого словаря для формирования json
        raw_data = raw_file.read()
        raw_file.close()
        
        upload_words = raw_data.replace('\n','').split('* ')
        upload_words.pop(0)
        
        for i in range(len(upload_words)):
            upload_words[i] = upload_words[i].split(' > ')

        for i in range(len(upload_words)):
                upload_words[i] = {"level":upload_words[i][0],"id":upload_words[i][1],"zh":upload_words[i][2],"pinyin":upload_words[i][3],"ru":upload_words[i][4],"tcribe":upload_words[i][5],"defi_zh":upload_words[i][6],"defi_ru":upload_words[i][7]}

        json_pack = json.dumps(upload_words) # Упаковать в json
        with open(f"{path}/data/fresh_dictionary.json", mode="w", encoding="utf-8") as file:
            file.write(json_pack)
            file.close()

        return f"Словарь сформирован."


    def j2o(self, json_data: str = ""):
    # Переводит json в массив объектов
        if self._file == 'none':

            json_data = json.loads(json_data)

            for i in range(len(json_data)):
                json_data[i] = Character(json_data[i]['level'],json_data[i]['id'],json_data[i]['zh'],json_data[i]['py'],[json_data[i]['translate']['en'],json_data[i]['translate']['ru']])

            if bool(json_data[0]) == 0:
                return 'void'
            else:
                return json_data # Массив объектов Character[i].attr
        
        elif self._file == 'data/zh_dictionary.json':
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Получение текущего пути к файлу

            raw_file = open(f"{path}/{self._file}", mode="r", encoding="utf-8") # Открытие словаря для получения слов
            raw_data = raw_file.read()
            raw_file.close()
            
            json_data = json.loads(raw_data)

            for i in range(len(json_data)):
                json_data[i] = Word(json_data[i]['level'],json_data[i]['id'],json_data[i]['zh'],json_data[i]['pinyin'],json_data[i]['ru'],json_data[i]['tcribe'],json_data[i]['defi_zh'],json_data[i]['defi_ru'])

            if bool(json_data[0]) == 0:
                return 'void'
            else:
                return json_data # Массив объектов Character[i].attr

        else:
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Получение текущего пути к файлу

            raw_file = open(f"{path}/{self._file}", mode="r", encoding="utf-8") # Открытие словаря для получения слов
            raw_data = raw_file.read()
            raw_file.close()
            
            json_data = json.loads(raw_data)

            for i in range(len(json_data)):
                json_data[i] = Character(json_data[i]['level'],json_data[i]['id'],json_data[i]['zh'],json_data[i]['py'],[json_data[i]['translate']['en'],json_data[i]['translate']['ru']])

            if bool(json_data[0]) == 0:
                return 'void'
            else:
                return json_data # Массив объектов Character[i].attr


    def o2j(self, object_array: list):
    # Переводит массив объектов в json
        
        for i in range(len(object_array)):
            object_array[i] = [object_array[i].level,object_array[i].id,object_array[i].zh,object_array[i].py,[object_array[i].translate['en'],object_array[i].translate['ru']]]

        json_data = json.dumps(object_array)
        
        return json_data # Упакованный json объект
    

# JsonConverter("text.txt").f2j()