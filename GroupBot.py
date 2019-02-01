
import requests
import vk_api
import traceback
import json
import apiai
from vk_api import VkUpload
import random
from time import sleep
import datetime
import random

HANGMANPICS = [
'''
    +---+
    |   |
        |
        |
        |
        |
 =========''',
    '''
    +---+
    |   |
        |
        |
        |
        |
 =========''', '''

    +---+
    |   |
     O  |
        |
        |
        |
 =========''', '''

    +---+
    |   |
    O   |
    |   |
        |
        |
 =========''', '''

    +---+
    |   |
    O   |
   /|   |
        |
        |
  =========''', '''

    +---+
    |   |
    O   |
   /|\  |
        |
        |
 =========''', '''

    +---+
    |   |
    O   |
   /|\  |
   /    |
        |
 =========''', '''

    +---+
    |   |
    O   |
   /|\  |
   / \  |
        |
 =========''']
from vk_api.longpoll import VkLongPoll, VkEventType
def is_number(smth):
    arr = list('0123456789')
    for s in smth:
        if s not in arr:
            return False
    return True
def return_pos(word,let):
    pos = 0
    positions = []
    if word[0] == let:
        positions.append(0)
    while pos != -1:
        pos = word.find(let,pos+1)
        if pos != -1:
            positions.append(pos)
    return positions
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
def make_w(right,pred,pos):
    final = ''
    count = 0
    counter = 0
    for i in pred:
        if count == pos[counter]:
            final += right[pos[counter]]
            if counter + 1 != len(pos):
                counter += 1
        else:
            final += pred[count]
        count += 1
    return final
sessionu = requests.Session()
login, password = 'login', 'password'
vk_sessionu = vk_api.VkApi(login, password)
uploadu = VkUpload(vk_sessionu)
try:
    vk_sessionu.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
vku = vk_sessionu.get_api()
token = 'YOUR TOKEN'
session = requests.Session()
commun = ['4ch','cheerfulcactus','the.facepallm','rus_strany','numos']
facts = ['fakt1','v5inf','vk.goodfakts','interst_facts','fact','scifacts']
vk_session = vk_api.VkApi(token=token)
upload = VkUpload(vk_session)
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
count = 1
words = [i for i in open(file = 'wordssss.txt',encoding="utf8",mode='r').read().lower().split(',') if len(i) > 3]
talk_array = []
save = ''
save_text = ''
used_words = {}
is_send = []
words_array = []
viselt_array = {}
for event in longpoll.listen():
    block_list = [i.replace('\n', '').split(':') for i in open('blocked_users.txt', 'r').readlines()]
    users = [i.replace('\n', '').split(':') for i in open('database.txt', 'r').readlines()]
    all_users = {}
    all_bans = {}
    for bl in block_list:
        all_bans[bl[0]] = bl[1]
    for user in users:
        all_users[user[0]] = {'balance':user[1],'status':user[2]}
    print(all_users)
    print(event.type)
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        print('kek')
        if event.from_user:
            count += 1
            save_text = event.text
            print('kek')
            if event.user_id in talk_array:
                if event.text.lower() == '/общение':
                    talk_array.remove(event.user_id)
                elif '/учить' in event.text.lower():
                    if ':' in event.text.lower():
                        file = open('learn.txt', 'a')
                        file.write(str(event.user_id) + ':' + event.text.lower().replace(' ','').replace(',','').replace('/учить','')+',\n')
                        file.close()
                        all_users[str(event.user_id)]['balance'] = str(int(all_users[str(event.user_id)]['balance']) + 10)
                        vk.messages.send(user_id=event.user_id,
                                         message='Спасибо учитель!',
                                         random_id=str(count)
                                         )
                    else:
                        vk.messages.send(user_id=event.user_id,
                                         message='В вашем предложении нету ":"',
                                         random_id=str(count)
                                         )
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
            elif event.user_id in list(viselt_array.keys()):
                if viselt_array[event.user_id]['tries'] == 0:
                    vk.messages.send(user_id=event.user_id,
                                     message='Вы проиграли и потеряли 5 дублей :(\n' +
                                             'Правильное слово: ' + viselt_array[event.user_id]['right'],
                                     random_id=str(count)
                                     )
                    all_users[str(event.user_id)]['balance'] = str(int(all_users[str(event.user_id)]['balance']) - 5)
                    del viselt_array[event.user_id]
                elif '_' not in viselt_array[event.user_id]['pred']:
                    vk.messages.send(user_id=event.user_id,
                                     message='Поздравляю, вы правильно угадали слово!',
                                     random_id=str(count)
                                     )
                    all_users[str(event.user_id)]['balance'] = str(int(all_users[str(event.user_id)]['balance']) + 20)
                    del viselt_array[event.user_id]
                elif '/виселица' in event.text.lower():
                    del viselt_array[event.user_id]
                else:
                    if '/угадал' in event.text.lower():
                        pred = event.text.lower().replace('/угадал','').replace(' ','')
                        if pred == viselt_array[event.user_id]['right']:
                            vk.messages.send(user_id=event.user_id,
                                             message='Поздравляю, вы правильно угадали слово!',
                                             random_id=str(count)
                                             )
                            all_users[str(event.user_id)]['balance'] = str(int(all_users[str(event.user_id)]['balance']) + 20)
                            del viselt_array[event.user_id]
                        else:
                            vk.messages.send(user_id=event.user_id,
                                             message='Вы неправильно предсказали слово :(',
                                             random_id=str(count)
                                             )
                            sleep(1)
                            count += 1
                            vk.messages.send(user_id=event.user_id,
                                             message=HANGMANPICS[len(HANGMANPICS)-viselt_array[event.user_id]['tries']],
                                             random_id=str(count)
                                             )
                            sleep(1)
                            count += 1
                            viselt_array[event.user_id]['tries'] -= 1
                            vk.messages.send(user_id=event.user_id,
                                             message='У вас осталось {} попыток'.format(viselt_array[event.user_id]['tries']),
                                             random_id=str(count)
                                             )
                    else:
                        if len(event.text.lower()) > 1:
                            vk.messages.send(user_id=event.user_id,
                                             message='Вы должны вписывать по одной букве,но если вы уже угадали слово, то впишите /угадал {угаданное слово}',
                                             random_id=str(count)
                                             )
                        elif event.text.lower() not in viselt_array[event.user_id]['used_l']:
                            coinc = return_pos(viselt_array[event.user_id]['right'],event.text.lower())
                            if coinc:
                                vk.messages.send(user_id=event.user_id,
                                                 message='Вы верно предсказали букву!',
                                                 random_id=str(count)
                                                 )
                                count += 1
                                sleep(1)
                                viselt_array[event.user_id]['pred'] = make_w(viselt_array[event.user_id]['right'],viselt_array[event.user_id]['pred'], coinc)
                                vk.messages.send(user_id=event.user_id,
                                                 message=viselt_array[event.user_id]['pred'],
                                                 random_id=str(count)
                                                 )
                                viselt_array[event.user_id]['used_l'].append(event.text.lower())
                            else:
                                vk.messages.send(user_id=event.user_id,
                                                 message='Вы неверно предсказали букву!',
                                                 random_id=str(count)
                                                 )
                                count += 1
                                sleep(1)
                                vk.messages.send(user_id=event.user_id,
                                                 message=HANGMANPICS[
                                                     len(HANGMANPICS) - viselt_array[event.user_id]['tries']],
                                                 random_id=str(count)
                                                 )
                                count += 1
                                sleep(1)
                                vk.messages.send(user_id=event.user_id,
                                                 message=viselt_array[event.user_id]['pred'],
                                                 random_id=str(count)
                                                 )
                                viselt_array[event.user_id]['tries'] -= 1
                                count += 1
                                sleep(1)
                                vk.messages.send(user_id=event.user_id,
                                                 message='У вас осталось {} попыток'.format(
                                                     viselt_array[event.user_id]['tries']),
                                                 random_id=str(count)
                                                 )
                                viselt_array[event.user_id]['used_l'].append(event.text.lower())
                        else:
                            vk.messages.send(user_id=event.user_id,
                                             message='Вы уже вводили эту букву!',
                                             random_id=str(count)
                                             )
            elif event.user_id in words_array:
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
            elif str(event.user_id) in list(all_bans.keys()):
                vk.messages.send(user_id=event.user_id,
                                 message='Вы были забанены по причине: {}\n'.format(all_bans[str(event.user_id)])+
                                         'чтобы подать апелляцию на свой бан - пишите сюда --> https://vk.com/sachkov2015',
                                 random_id=str(count)
                                 )
            else:
                if str(event.user_id) not in list(all_users.keys()):
                    fl = open('database.txt','a')
                    fl.write(str(event.user_id)+':'+'1000:'+'user\n')
                    fl.close()
                    all_users[str(event.user_id)] = {'balance':'1000','status':'user'}
                    is_send.append(event.user_id)
                    print('все норм')
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Здравствуйте, я Евгений - Искусственный Интеллект\n'+
                                'Могу вам предложить воспользоваться следующими командами:\n' +
                                '/факт (Кидает вам интересный факт)\n' +
                                '/мем (Кидает орный мем)\n' +
                                '/общение (включается режим общения бота (написать еще раз , чтобы выключить))\n' +
                                '/инфо (вывести сообщение еще раз)\n'+
                                '/игры (Высылает вам весь список мини-игр)\n'+
                                '/предложение {текст предложения} (У вас есть шанс предложить что-то новое (например новую команду), или сообщить о какой-либо ошибке)\n'+
                                '/лк (кидает информацию о вашем балансе и прочем...)\n'+
                                '/заработать (кидает вам все возможные способы заработать)'
                        ,
                        random_id=str(count),
                        v='5.92'
                    )
                elif '/игры' in event.text.lower():
                    vk.messages.send(user_id=event.user_id,
                                     message='/слова (начинает играть с вами в слова, написать /слова ещё раз,чтобы закончить)\n' +
                                            '/виселица (вы начинаете играть в игру виселица)',
                                     random_id=str(count)
                                     )
                elif '/виселица' in event.text.lower():
                    right_word = random.choice(words)
                    vk.messages.send(
                        user_id=event.user_id,
                        message='Вы получите 20 дублей, если отгадайте слово верно, у вас 8 попыток \n'+
                                'Чтобы выйти до окончания игры, вам нужно вписать /виселица еще раз, но вы потеряете 10 дублей.\n'+
                                'Если вы уверены,что вы уже угадали слово и не хотите вводить по букве, впишите /угадал {ваше слово}\n'
                        ,
                        random_id=str(count))
                    vk.messages.send(
                        user_id=event.user_id,
                        message=str('_' * len(right_word)),
                        random_id=str(count))
                    viselt_array[event.user_id] = {'right':right_word.lower(),'pred':str('_' * len(right_word)),'used_l':[],'tries':7}
                elif '/лк' in event.text.lower():
                    vk.messages.send(user_id=event.user_id,
                                     message="""
                                     Ваш баланс: {} дублей\n
                                     Ваш ID: {}\n
                                     Ваш статус: {}\n
                                     """.format(all_users[str(event.user_id)]['balance'],str(event.user_id),all_users[str(event.user_id)]['status']),
                                     random_id=str(count)
                                     )
                elif '/админ' in event.text.lower() and all_users[str(event.user_id)]['status'] == 'admin':
                    vk.messages.send(
                        user_id=event.user_id,
                        message='/ban {user_id} {причина бана}(банит юзера с этим id)\n'+
                                '/repl {user_id} {сумма дублей} (поплняет счёт юзера с данным id)\n'+
                                '/unban {user_id}',
                        random_id=str(count)
                                            )
                elif '/ban' in event.text.lower() and all_users[str(event.user_id)]['status'] == 'admin':
                    req = event.text.lower().replace('/ban ','')
                    req = req.split(' ')
                    if req[0] in list(all_users.keys()) and len(req)==2:
                        fli = open('blocked_users.txt','a')
                        fli.write(req[0]+':'+req[1]+'\n')
                        fli.close()
                        vk.messages.send(user_id=event.user_id,
                                         message='Успешно!',
                                         random_id=str(count)
                                         )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Пользователя с этим id нету в базе данных бота, или вы не написали причину бана',
                            random_id=str(count)
                        )
                elif 'unban' in event.text.lower() and all_users[str(event.user_id)]['status'] == 'admin':
                    req = event.text.lower().replace('/unban ', '')
                    if req in list(all_users.keys()):
                        sm = open('blocked_users.txt', 'r')
                        fli = [i.replace('\n', '').split(':') for i in sm.readlines()]
                        sm.close()
                        final = []
                        for li in fli:
                            if li[0] == req:
                                pass
                            else:
                                final.append(li)
                        fuiil = open('blocked_users.txt','w')
                        for sk in final:
                            fuiil.write(':'.join(sk)+'\n')
                        fuiil.close()
                        vk.messages.send(user_id=event.user_id,
                                         message='Успешно!',
                                         random_id=str(count)
                                         )
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            message='Пользователя с этим id нету в базе данных бота',
                            random_id=str(count)
                        )
                elif '/repl' in event.text.lower() and all_users[str(event.user_id)]['status'] == 'admin':
                    req = event.text.lower().replace('/repl ', '')
                    req = req.split(' ')
                    if req[0] in list(all_users.keys()) and len(req) == 2 and is_number(req[1]):
                        all_users[req[0]]['balance'] = str(int(all_users[req[0]]['balance']) + int(req[1]))
                        vk.messages.send(user_id=event.user_id,
                                         message='Успешно!',
                                         random_id=str(count)
                                         )
                    else:
                        vk.messages.send(user_id=event.user_id,
                                         message='Что-то вы сделали не по правилам, попробуйте еще!',
                                         random_id=str(count)
                                         )
                elif '/заработать' in event.text.lower():
                    vk.messages.send(user_id=event.user_id,
                                     message=
                                     'Способы заработать:\n'+
                                     '1. Во время режима общения c ботом, когда вы используете команду /учить , вы зарабатываете 10 дублей\n'+
                                     '2. Если вы используете команду /предложение, у вас есть возможность заработать до 500 дублей, если ваше предложение понравится создателю\n'+
                                     '3. Выиграть в игре виселица (Вы получаете 20 дублей)',
                                     random_id=str(count)
                                     )
                elif '/факт' in event.text.lower():
                    attachments = []
                    image_url = ''
                    while image_url == '':
                        try:
                            image_url = random.choice(random.choice(
                                vku.wall.get(domain=random.choice(facts), offset=random.randint(1, 1000))['items'])[
                                                          'attachments'])['photo']['sizes'][-1]['url']
                        except Exception as e:
                            print('Ошибка:\n', traceback.format_exc())
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
                    while image_url == '':
                        try:
                            image_url = random.choice(random.choice(vku.wall.get(domain=random.choice(commun), offset=random.randint(1, 1000))['items'])['attachments'])['photo']['sizes'][-1]['url']
                        except Exception as e:
                            print('Ошибка:\n', traceback.format_exc())
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
                                     message="""
                                     Здравствуйте!
                                     (Если вы считаете мою фразу неуместной ,или глупой , введите /учить {вопрос}:{Правильный ответ} (обязательно через двоеточие)
                                     С помощью этого наш бот будет становится всё умнее и умнее!)
                                     """,
                                     random_id=str(count))
                elif '/предложение' in event.text.lower():
                    vk.messages.send(user_id=event.user_id,
                                     message='Спасибо за предложение! Обязательно учтём!',
                                     random_id=str(count))
                    sleep(2)
                    vku.messages.send(user_id='281303430',
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
                        message='Здравствуйте, я Евгений - Искусственный Интеллект\n'+
                                'Могу вам предложить воспользоваться следующими командами:\n' +
                                '/факт (Кидает вам интересный факт)\n' +
                                '/мем (Кидает орный мем)\n' +
                                '/общение (включается режим общения бота (написать еще раз , чтобы выключить))\n' +
                                '/инфо (вывести сообщение еще раз)\n'+
                                '/игры (Высылает вам весь список мини-игр)\n' +
                                '/предложение {текст предложения} (У вас есть шанс предложить что-то новое (например новую команду), или сообщить о какой-либо ошибке)\n'+
                                '/лк (кидает информацию о вашем балансе и прочем...)\n' +
                                '/заработать (кидает вам все возможные способы заработать)'
                        ,
                        random_id=str(count),
                        v='5.92'
                    )
    fuil = open('database.txt','w')
    for ki in all_users:
        fuil.write(ki+':'+all_users[ki]['balance']+':'+all_users[ki]['status']+'\n')
    fuil.close()
    sleep(1)
