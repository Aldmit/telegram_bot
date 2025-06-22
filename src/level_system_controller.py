r"""The LevelSystemController class has the following methods:

    - streak(self,count) - Меняет значение стрика в пользовательских настройках на +-1
    - progress(self,count) - Меняет значение прогресса в пользовательских настройках на +-1
    - sub_level(self,count) - Меняет значение саб-левела в пользовательских настройках на +-1, а также устанавливает уровень словаря пользователя по достижению контрольных значений

"""
#'
from .user import *

class LevelSystemController:
    def __init__(self, id: str) -> None:
        self._id = id
        self._user = User(id)
        self._user_data = self._user._data.get_data(self._user._language+'_settings')
    
    
    def set_level(self, level, sub_level, progress, streak) -> bool:
        user_data = self._user._data.get_data(self._user._language+'_settings')
        user_data['level'] = level
        user_data['sub-level'] = sub_level
        user_data['progress'] = progress
        user_data['streak'] = streak
        user_data = json.dumps(user_data)
        self._user._data.update_data(self._user._language+'_settings',user_data)
        return True
    

    def streak(self,count):
        user_data = self._user._data.get_data(self._user._language+'_settings')
        diff = user_data['streak'] + count

        if diff >= 7:
            diff = 0
            user_data['streak'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return self.progress(1)

        elif diff <= -7:
            diff = 0
            user_data['streak'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return self.progress(-1)
        
        else:
            user_data['streak'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return count


    def progress(self,count):
        user_data = self._user._data.get_data(self._user._language+'_settings')
        diff = user_data['progress'] + count

        if diff >= 5:
            diff = 0
            user_data['progress'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return self.sub_level(1)

        elif diff <= -5:
            diff = 0
            user_data['progress'] = diff
            if user_data['progress'] <= 10:
                user_data['progress'] = diff
                user_data = json.dumps(user_data)
                self._user._data.update_data(self._user._language+'_settings',user_data)
                return self.sub_level(0)
            else:        
                user_data['progress'] = diff
                user_data = json.dumps(user_data)
                self._user._data.update_data(self._user._language+'_settings',user_data)
                return self.sub_level(-1)

        else:
            user_data['progress'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return count
        

    def sub_level(self,count):
        user_data = self._user._data.get_data(self._user._language+'_settings')
        diff = user_data['sub-level'] + count
        
        if diff == 5000:
            level = 7
            user_data['level'] = level
            user_data['sub-level'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return 'HSK 6 завершен. Поздравляю, мне больше нечему вас учить.'
        
        elif diff == 2500:
            level = 6
            user_data['level'] = level
            user_data['sub-level'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return 'Открыт HSK 6. Вы на пути к вершине мастерства.'
        
        elif diff == 1200:
            level = 5
            user_data['level'] = level
            user_data['sub-level'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return 'Открыт HSK 5. Ваш путь к верщине начинается здесь.'

        elif diff == 599:
            level = 4
            user_data['level'] = level
            user_data['sub-level'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return 'Вы переходите на HSK 4. Ваше упорство поражает.'

        elif diff == 300:
            level = 3
            user_data['level'] = level
            user_data['sub-level'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return 'HSK 2 взят, добро пожаловать в HSK 3. Поздравляю!'

        elif diff == 150:
            level = 2
            user_data['level'] = level
            user_data['sub-level'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data)
            return 'HSK 1 позади, поздравляю!'
        
        elif count == 1:
            user_data['sub-level'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data) # Зачем тут обновлять данные?
            return 'Вы открыли новое слово!'
        
        elif count == -1:
            user_data['sub-level'] = diff
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data) # -/-/-/-/-/-
            return 'Одно из новых слов стало недоступно.'
        
        elif count == 0:
            user_data = json.dumps(user_data)
            self._user._data.update_data(self._user._language+'_settings',user_data) # -/-/-/-/-/-
            return "Я не могу опустить уровень ещё ниже 😅, пожалуйста пробуй с тем что есть)"


    


