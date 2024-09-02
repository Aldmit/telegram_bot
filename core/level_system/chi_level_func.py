
from ..data_layer import *

async def sub_level(name,password,count):
    user_data = await db_get_data(name,password)
    diff = user_data[3] + count
    
    if diff == 5000:
        level = 7
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'HSK 6 завершен. Поздравляю, мне больше нечему вас учить.'
    
    elif diff == 2500:
        level = 6
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'Открыт HSK 6. Вы на пути к вершине мастерства.'
    
    elif diff == 1200:
        level = 5
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'Открыт HSK 5. Ваш путь к верщине начинается здесь.'

    elif diff == 599:
        level = 4
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'Вы переходите на HSK 4. Ваше упорство поражает.'

    elif diff == 300:
        level = 3
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'HSK 2 взят, добро пожаловать в HSK 3. Поздравляю!'

    elif diff == 150:
        level = 2
        await db_update_data(name,password,level,diff,user_data[4],user_data[5])
        return 'HSK 1 позади, поздравляю!'
    
    elif count == 1:
        await db_update_data(name,password,user_data[2],diff,user_data[4],user_data[5])
        return 'Вы открыли новое слово!'
    
    elif count == -1:
        await db_update_data(name,password,user_data[2],diff,user_data[4],user_data[5])
        return 'Одно из новых слов стало недоступно.'
    
    elif count == 0:
        await db_update_data(name,password,user_data[2],diff,user_data[4],user_data[5])
        return "Я не могу опустить уровень ещё ниже 😅, пожалуйста пробуй с тем что есть)"



async def progress(name,password,count):
    user_data = await db_get_data(name,password)
    diff = user_data[4] + count

    if diff >= 5:
        diff = 0
        await db_update_data(name,password,user_data[2],user_data[3],diff,user_data[5])
        return await sub_level(name,password,1)

    elif diff <= -5:
        diff = 0
        if user_data[3] <= 10:
            await db_update_data(name,password,user_data[2],user_data[3],diff,user_data[5])
            return await sub_level(name,password,0)
        else:
            await db_update_data(name,password,user_data[2],user_data[3],diff,user_data[5])
            return await sub_level(name,password,-1)

    else:
        await db_update_data(name,password,user_data[2],user_data[3],diff,user_data[5])
        return count


async def streak(name,password,count):
    user_data = await db_get_data(name,password)
    # print(f'Получение данных в стрике: {user_data}')
    diff = user_data[5] + count

    if diff >= 7:
        diff = 0
        await db_update_data(name,password,user_data[2],user_data[3],user_data[4],diff)
        return await progress(name,password,1)

    elif diff <= -7:
        diff = 0
        await db_update_data(name,password,user_data[2],user_data[3],user_data[4],diff)
        return await progress(name,password,-1)
    
    else:
        await db_update_data(name,password,user_data[2],user_data[3],user_data[4],diff)
        return count



