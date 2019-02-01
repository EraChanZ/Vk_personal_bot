import requests
import vk_api
import traceback
import json
import apiai
from vk_api import VkUpload
import random
from time import sleep
import datetime
from vk_api.longpoll import VkLongPoll, VkEventType
def find_word(letter, used):
    for word in words:
        if word[0] == letter and word not in used:
            return word
def is_anybody_has_birthday(names,current):
    final = []
    for name in names:
        nam = name.split(',')[-1]
        if [i.strip() for i in nam.split('.')[:2]] == current.split('.'):
            final.append(name)
    return final
def namag(word):
    if word[-1] == 'ь' or word[-1] == 'ъ':
        return word[-2]
    else:
        return word[-1]
session = requests.Session()
commun = ['4ch','cheerfulcactus','the.facepallm','rus_strany']
facts = ['fakt1','v5inf','vk.goodfakts','interst_facts']
login, password = '+79261572269', 'S6C89Q4G'
vk_session = vk_api.VkApi(login, password)
upload = VkUpload(vk_session)
block_list = ['165790907','281303430']
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
all_names = open('birthdays.txt','r').readlines()
count = 4070
words = [i for i in open(file = 'wordssss.txt',encoding="utf8",mode='r').read().lower().split(',') if len(i) > 3]
reason = input('Владимир, почему вы уходите ? :')
when = input('Владимир, на сколько вы уходите ? :')
talk_array = []
greetings = ['привет','здарова','приветики','Чё-как','Здоровеньки-булы']
save = ''
save_text = ''
used_words = {}
is_send = []
words_array = []
for event in longpoll.listen():
    save = event
    print(event.type)
    '''
    current_time = str(datetime.datetime.now())[5:]
    current_time = '.'.join(current_time[:current_time.find(' ')].split('-')[::-1])
    result = is_anybody_has_birthday(all_names,current_time)
    print(result)
    if result:
        infa = result[0].split(',')
        vk.messages.send(
            user_id=infa[0],
            message='C днём рождения '+infa[1]+' '+infa[2]+' !',
            random_id=str(count)
        )
    '''
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        print('kek')
        if event.from_user:
            count += 1
            save_text = event.text
            print('kek')
            if event.user_id in talk_array and str(event.user_id) not in block_list:
                if event.text.lower() == '/общение':
                    talk_array.remove(event.user_id)
                else:
                    CLIENT_ACCESS_TOKEN = '2bf2871e252c4a7a99e6c7c70721bd72'
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
            elif event.user_id in words_array and str(event.user_id) not in block_list:
                if '/слова' in event.text.lower():
                    words_array.remove(event.user_id)
                    used_words[event.user_id]['bot'] = []
                    used_words[event.user_id]['client'] = []
                else:
                    if event.text:
                        if event.text.lower() in used_words[event.user_id]['client']:
                            vk.messages.send(user_id=event.user_id,
                                             message='Вы уже использовали это слово, придумайте что-то новое',
                                             random_id=str(count)
                                             )
                        else:
                            checking = namag(used_words[event.user_id]['bot'][-1])
                            if event.text.lower()[0] != checking:
                                vk.messages.send(user_id=event.user_id,
                                                 message='Буквы не совпадают, попробуйте другое слово',
                                                 random_id=str(count)
                                                 )
                            else:
                                if event.text.lower()[-1] == 'ь' or event.text.lower()[-1] == 'ъ':
                                    answer = find_word(event.text.lower()[-2], used_words[event.user_id]['bot'])
                                else:
                                    answer = find_word(event.text.lower()[-1], used_words[event.user_id]['bot'])
                                if answer:
                                    vk.messages.send(user_id=event.user_id,
                                                     message=answer,
                                                     random_id=str(count)
                                                     )
                                    used_words[event.user_id]['bot'].append(answer)
                                    used_words[event.user_id]['client'].append(event.text.lower())
                                else:
                                    vk.messages.send(user_id=event.user_id,
                                                     message='Не могу найти подходящего слова, вы выиграли!',
                                                     random_id=str(count)
                                                     )
                                    words_array.remove(event.user_id)
            elif str(event.user_id) not in block_list:
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
                elif '/предложение' in event.text.lower():
                    vk.messages.send(user_id=event.user_id,
                                     message='Спасибо за предложение! Обязательно учтём!',
                                     random_id=str(count))
                    sleep(1)
                    vk.messages.send(user_id='281303430',
                                     message="""
                                     Предложение от юзера с id : {}\n
                                     Сообщение: {}\n
                                     """.format(event.user_id,event.text.lower().replace('/предложение','')),
                                     random_id=str(count))
                elif '/слова' in event.text.lower():
                    words_array.append(event.user_id)
                    random_word = random.choice(words)
                    used_words[event.user_id] = {'client':[],'bot':[random_word]}
                    vk.messages.send(user_id=event.user_id,
                                     message=random_word,
                                     random_id=str(count))
                elif '/инфо' in event.text.lower():
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Привет, я личный бот Сачкова , Евгений\n' + 'Вовы сейчас нет у компьютера по причине : {}'.format(reason) + '\n' +
                                'Пока Владимира нет, могу вам предложить воспользоваться следующими функциями:\n' +
                                '/когда (С помощью этой функции вы узнаете через сколько времени владимир вернётся домой)\n' +
                                '/факт (Кидает вам интересный факт)\n' +
                                '/мем (Кидает орный мем)\n' +
                                '/общение (включается режим общения бота (написать еще раз , чтобы выключить))\n' +
                                '/инфо (вывести сообщение еще раз)\n'+
                                '/слова (начинает играть с вами в слова)\n'+
                                '/предложение {текст предложения} (У вас есть шанс предложить что-то новое (например новую команду), или сообщить о какой-либо ошибке)',
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
                                '/инфо (вывести сообщение еще раз)\n'
                                '/слова (начинает играть с вами в слова)\n'+
                                '/предложение {текст предложения} (У вас есть шанс предложить что-то новое (например новую команду), или сообщить о какой-либо ошибке)'
                        ,
                        random_id=str(count),
                        v='5.92'
                    )
