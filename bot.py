import vk_api
import requests
import traceback
import json
import apiai
from vk_api import VkUpload
import random
from time import sleep
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
def is_anybody_has_birthday(names,current):
    final = []
    for name in names:
        nam = name.split(',')[-1]
        if [i.strip() for i in nam.split('.')[:2]] == current.split('.'):
            final.append(name)
    return final
session = requests.Session()
commun = ['4ch','cheerfulcactus','the.facepallm','rus_strany']
facts = ['fakt1','v5inf','vk.goodfakts','interst_facts']
login, password = '+79261572269', 'S6C89Q4G'
vk_session = vk_api.VkApi(login, password)
upload = VkUpload(vk_session)
block_list = ['165790907']
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
all_names = open('birthdays.txt','r').readlines()
count = 1200
reason = input('Владимир, почему вы уходите ? :')
when = input('Владимир, на сколько вы уходите ? :')
talk_array = []
greetings = ['привет','здарова','приветики','Чё-как','Здоровеньки-булы']
save = ''
save_text = ''
is_send = []
for event in longpoll.listen():
    save = event
    print(event.type)
    current_time = str(datetime.datetime.now())[5:]
    current_time = '.'.join(current_time[:current_time.find(' ')].split('-')[::-1])
    result = is_anybody_has_birthday(all_names,current_time)
    print(result)
    if result:
        infa = result[0].split('.')
        vk.messages.send(
            user_id=infa[0],
            message='C днём рождения '+infa[1]+' '+infa[2]+' !',
            random_id=str(count)
        )
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        print('kek')
        if event.from_user:
            if save_text == event.text:
                print('ПОВТОР')
                continue
            count += 1
            save_text = event.text
            print('kek')
            if event.user_id in talk_array:
                if event.text.lower() == '/общение':
                    talk_array.remove(event.user_id)
                else:
                    CLIENT_ACCESS_TOKEN = '289a95d5bc84431bb1f6b6a10100e805'
                    AI = apiai.ApiAI(client_access_token=CLIENT_ACCESS_TOKEN)
                    request = AI.text_request()
                    request.lang = 'russian'
                    request.session_id = '<SESSION ID, UNIQUE FOR EACH USER>'
                    request.query = event.text
                    response = request.getresponse()
                    obj = json.loads(response.read())
                    reply = obj['result']['fulfillment']['speech']
                    vk.messages.send(user_id=event.user_id,
                                     message=reply,
                                     random_id=str(count)
                                     )
            elif event.user_id not in block_list:
                if '/когда' in event.text.lower():
                    vk.messages.send(user_id=event.user_id,
                                     message='Он вернется через '+ str(when),
                                     random_id = str(count)
                                     )
                elif '/факт' in event.text.lower():
                    attachments = []
                    image_url = ''
                    try:
                        image_url = random.choice(random.choice(
                            vk.wall.get(domain=random.choice(facts), offset=random.randint(1, 100))['items'])[
                                                      'attachments'])['photo']['sizes'][-1]['url']
                    except:
                        pass
                    if image_url:
                        image = session.get(image_url, stream=True)
                        photo = upload.photo_messages(photos=image.raw)[0]
                        attachments.append(
                            'photo{}_{}'.format(photo['owner_id'], photo['id'])
                        )
                        vk.messages.send(user_id=event.user_id,
                                         message=str(count),
                                         attachment=','.join(attachments),
                                         random_id=str(count)
                                         )
                    else:
                        vk.messages.send(user_id=event.user_id,
                                         message='Напиши /факт ещё разок)',
                                         random_id=str(count)
                                         )
                elif '/мем' in event.text.lower():
                    attachments = []
                    image_url = ''
                    try:
                        image_url = random.choice(random.choice(vk.wall.get(domain=random.choice(commun), offset=random.randint(1, 100))['items'])['attachments'])['photo']['sizes'][-1]['url']
                    except:
                        pass
                    if image_url:
                        image = session.get(image_url, stream=True)
                        photo = upload.photo_messages(photos=image.raw)[0]
                        attachments.append(
                            'photo{}_{}'.format(photo['owner_id'], photo['id'])
                        )
                        vk.messages.send(user_id=event.user_id,
                                         message=str(count),
                                         attachment=','.join(attachments),
                                         random_id=str(count)
                                         )
                    else:
                        vk.messages.send(user_id=event.user_id,
                                         message='Впиши /мем ещё разок)',
                                         random_id=str(count)
                                         )
                elif '/общение' in event.text.lower():
                    talk_array.append(event.user_id)
                    vk.messages.send(user_id=event.user_id,
                                     message='Привет)',
                                     random_id=str(count))
                elif '/инфо' in event.text.lower():
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Привет, я личный бот Сачкова , Евгений\n' + 'Вовы сейчас нет у компьютера по причине : {}'.format(
                            reason) + '\n' +
                                'Пока Владимира нет, могу вам предложить воспользоваться следующими функциями:\n' +
                                '/когда (С помощью этой функции вы узнаете через сколько времени владимир вернётся домой)\n' +
                                '/факт (Кидает вам интересный факт)\n' +
                                '/мем (Кидает орный мем)\n' +
                                '/общение (включается режим общения бота (написать еще раз , чтобы выключить))\n' +
                                '/инфо (вывести сообщение еще раз)\n',
                        random_id=str(count),
                        v='5.92'
                    )
                elif event.user_id not in is_send:
                    is_send.append(event.user_id)
                    print('все норм')
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Привет, я личный бот Сачкова , Евгений\n'+'Вовы сейчас нет у компьютера по причине : {}'.format(reason)+'\n'+
                                'Пока Владимира нет, могу вам предложить воспользоваться следующими функциями:\n'+
                                '/когда (С помощью этой функции вы узнаете через сколько времени владимир вернётся домой)\n'+
                                '/факт (Кидает вам интересный факт)\n'+
                                '/мем (Кидает орный мем)\n' +
                                '/общение (включается режим общения бота (написать еще раз , чтобы выключить))\n'+
                                '/инфо (вывести сообщение еще раз)\n',
                        random_id=str(count),
                        v='5.92'
                    )
