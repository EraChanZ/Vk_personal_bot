import requests
import vk_api
from vk_api import VkUpload
import random
from time import sleep
greetings = '''
В кои-то веки!,
Вот так встреча!,
Всегда рады Вам,
Глубокое (глубочайшее) почтение,
Горячий привет!,
Горячо приветствую,
Доброго здоровья (здоровьица...)!,
Доброе утро!,
Добро пожаловать!,
Добрый вечер!,
Добрый день!,
Дозвольте приветствовать (Вас),
Душевно рад (Вас видеть),
Душою рад Вас видеть,
Желаю здравствовать!,
Здравия желаю,
Здравствуйте!,
Какая встреча!,
Какие гости!,
Моё почтение! .,
Нижайшее почтение!,
Позвольте Вас приветствовать,
Почитаю приятным долгом засвидетельствовать Вам моё почтение (уважение...), 
Почтение моё Н.,
Привет!,
Приветствую Вас,
Приветствую Вас от имени...,
(Адресант) приветствует (адресата),
Приятный вечер!,
Приятный день!,
Рад Вам,
Рад Вас видеть,
Рад Вас видеть в добром здравии,
Рад Вас приветствовать,
Рад Вас слышать,
Рад пожать Вашу руку,
Разрешите Вас приветствовать,
Разрешите засвидетельствовать Вам моё почтение (уважение),
Свидетельствую (Вам, Н.) своё (моё) почтение (уважение),
С возвращением!,
С выздоровлением!, 
С добрым утром!,
Сердечно приветствую Вас!,
Сердечно рад Вам,
Сердечный поклон Вам,
Сердечный привет Вам,
Сколько лет, сколько зим!,
Тысячу лет Вас не видел (не виделись)!,
'''
greetings = greetings.split(',')
session = requests.Session()
login, password = '+79261572269', 'S6C89Q4G'
vk_session = vk_api.VkApi(login, password)
upload = VkUpload(vk_session)
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
vk = vk_session.get_api()
count = 120
ch = []
for offset in range(0,50000,1000):
    ch.extend(vk.groups.getMembers(group_id='45745333',offset=offset)['items'])
for i in range(100):
    try:
        print('yeah')
        vk.messages.send(
            user_id=random.choice(ch),
            message=random.choice(greetings),
            random_id=str(count)
        )
        count += 1
    except:
        print('blin')
        pass
    sleep(3)