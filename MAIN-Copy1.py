
# coding: utf-8

# In[ ]:

import os
import random
import numpy as np
import re
import requests
import vk_api
import urllib.request
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType, VkLongpollMode
from vk_api.upload import VkUpload as vkImport
import time
import json
#from vk_api.docs import getMessagesUploadServer


# In[ ]:

token_=''
url_begin='https://psv4.userapi.com/'


# In[ ]:

LOGIN=89142930493
PASSWORD='ayal11'
LANG='ru'


# **Варианты приветствий**

# In[ ]:

#TODO: оставить только нижний регистр
welcome=['привет', 'приветик','приветики','хэй', 'Привет','здарова', 'прив','дарова','Здарова', 'Халло', 'халло','Хелло', 'хэллоу','Хеллоу',
         'хелоу','хело','привет!']
how_are_you=['Как дела?','как дела?', 'как жизнь?', 'дела','дела?','как поживаешь?']
agromsg=['Тупой','тупой','Ты дурак', 'тупой?','Дурак', 'дурак', 'Дебил', 'дебил', 'дурачок', 'конченный', 'Конченный', 
         'глупый', 'Ты глупый', 'ты глупый','Баран', 'баран', 'тупой бот', 'Тупой бот', 
         'бяка', 'Бяка', 'Гадина', 'гадина', 'даун', 'Даун', 'Дэбил', 'дэбил', 'обормот', 
         'Обормот', 'Капец ты тупой','капец ты тупой', 'Лох', 
         'лох', 'ефим', 'критин', 'Критин', 'Мудак', 'мудак','хуй', 'пидор','чмо']
agrootv=['Кто обзывается, тот тем и называется!', 'Если ты так будешь общаться, то я тебя побью',
         'Фу, ужасное воспитание!','Было два стула, на какой сам сядешь, на какой бота посадишь', 
         'Я все маме расскажу!', 'За тобой уже выехали', 'Если ты меня еще раз оскорбишь,то тебе крышка',
         'За школой в 5']
randomanser=['Здорово', 'С тобой интересно общаться', 'Мне кажется, что неплохо', 'Ого', 'И вправду круто', 
             'Очень даже', 'Мне нравится', 'Пипееец', 'Оу маиин', 'Что? Серьезно? Четка!','В принципе неплохо!', 
             'Понятно, что-то еще?', 'Это действительно интересно!','Ого, расскажешь еще что-нибудь?',
             'Не, давай общаться нормально!']
whatDoUDo=['Что делаешь', 'делаешь']
drugs=['наркотики', 'алкоголь', 'пиво', 'водка', 'кит', 
       'смерть', 'умри','сигареты', 'умрешь', 'сдохни', 'убью']
ploho=['Это очень плохо', 'Не пиши такое!', 'Нельзя говорить подобные вещи!', 
       'Если ты еще раз подобное скажешь,то к тебе приедут определенные службы', 
       'Так,не стоит говорить такое, иначе позвоню твоей маме!', 
       'Слушай я все понимаю, но не нужно об этом говорить и даже думать!', 
       'Тебе подсказать телефон доверия?']
helper='На данный момент я умею отвечать на твои сообщения разного характера (будь то хорошие или плохие).\n В будущем я научусь редактировать аудиозаписи и накладывать туда разные голоса:)'


# ## Обработка `longpoll` запросов
# **Два вспомогательных класса-хендлера для обработки входящих запросов**

# In[ ]:

#@DaniloZZZ 
class Longpoll():
    def __init__(self, upd_checker,
                 params_modifier=lambda x,u: x):
        self.func= upd_checker
        self.param_next= params_modifier

    def event_emmitter(self,addr,params={}):
        while True:
            r = requests.get(addr,params)
            js = r.json()
            if r.status_code==200:
                if (self.func(js)):
                    yield js
                    print('upd',params)
                    self.param_next(params,True)
                else:
                    print('no updates, listening more...')
                    self.param_next(params,False)
                    return
            else:
                raise Exception('longpoller error',
                                r.status_code,js,
                                'params:',params
                                )

class VKBot:
    ep = 'https://api.vk.com/method'
    version = '5.80'

    def __init__(self,token,group):
        self.token = token
        self.group = group
        self.get_longpoll_server(group)
        self.poller = Longpoll(
            lambda x: len(x.get('updates',[]))>0,
            params_modifier=
            lambda x,u: x.update({'ts':x.get('ts',0)+1})\
            if u else x
        )

    def start_polling(self,**args):
        addr = self.longpoll_server
        params = {
            'act':'a_check',
            'key':self.longpoll_key,
            'ts':self.ts
        }
        for event in self.poller.event_emmitter(addr,params):
            try:
                #print('$$$$',event['updates'][0]['object']['attachments'],'$$$$')
                t = random.randint(0,100) 
                #print(event['updates'][0]['peer_id'])
                url_=event['updates'][0]['object']['attachments'][0]['doc']['preview']['audio_msg']['link_ogg']
                name_ = str(t)+'.ogg'
                #print(type(url_), url_)
                #print(type(name_),name_)
                #print('!!!!!!!!!!',url_,'!!!!!!!!!!!!!!')
                audio = urllib.request.urlretrieve(filename=name_, 
                                                   url=url_)            
                return audio
            except KeyError:
                print('KeyError event occured')
                pass
    def set_message_handler(self,clb):
        self.message_handler =  clb
    def set_callback_handler(self,clb):
        self.callback_handler = clb

    def get_longpoll_server(self,group):
        print("getting longpoll server addr")
        s = self.make_request('groups.getLongPollServer',
                          {
                            'group_id':group
                          }
                         )
        server,key = s.get('server'),s.get('key')
        # Assign the props to self
        if (server and key):
            self.longpoll_server, self.longpoll_key = server,key
            self.ts = s.get('ts')
        else:
            raise Exception("Vk returned no Longpoll servers")

    def make_request(self,method_name,method_params):
        ep = 'https://api.vk.com/method/'
        ep += method_name
        params = {
            'access_token':self.token,
            'v':self.version
        }
        params.update(method_params)
        r = requests.get(ep,params=params)
        js = r.json()
        print(r)
        print(r.text)
        return js.get('response')


# Инициализация токена

# In[ ]:

group_id = '168509549'
bot = VKBot(token_,group_id)


# # Функции-обработчики сообщений (текстовых и аттачей)

# **Эта функция получает на вход сообщение от пользователя, обрабатывает его и посылает пользователю ответ. На вход подается очередное слово на обработку, а также количество слов в сообщении.**

# In[ ]:

def handle_text_msg(text_from_usr_,length,vk,name):
    flag=0
    tmp=0
    for i in range(len(text_from_usr_)):
        text_from_usr=text_from_usr_[i]
        
        if text_from_usr in welcome:
            print('==welocome==')
            flag += 1
            return 'привет, '+name
        
                    
        if text_from_usr in whatDoUDo:
            print('==WhatDoUDo==')
            flag += 1
            return 'с тобой говорю, а ты?'
        
        if text_from_usr in ['help', 'Help','умеешь','можешь']: 
            print('==Help==') 
            flag += 1 
            return helper
        
        if text_from_usr in ['надя']:
            print('==надя==')
            flag += 1
            return 'Очень крутой,классный,балдежный,невероятный человек. Если кто то ее обидит,то ее команда порвет это существо!'

        if text_from_usr in ['чмо']:
            print('==чмо==')
            flag += 1
            return 'ЧеловекМодноОдетый'
        
        if text_from_usr in drugs:
            print('==Drugs==')
            flag += 1
            return str(random.choice(ploho))

        if text_from_usr in agromsg:
            r='сам ты '+text_from_usr
            agrootv.append(r)
            lol1=random.choice(agrootv)
            agrootv.remove(r)
            print('==Evil==')
            flag += 1
            return lol1


        if text_from_usr in how_are_you:
            print('==HowAreYou==')
            flag += 1
            return 'неплохо, спасибо! А как твои дела?'
        
    if (length==1) and flag==0:
        flag += 1
        print('==AnyText==')
        return random.choice(randomanser)
    else:
            return random.choice(randomanser)
                    


# In[ ]:

def handle_attach (event, vk):
    global event_temp
    event_temp = event # for debug
    
    try:
        print('@',event.attachments,'@')
        if (event.attachments['attach1_type']=='doc'):
            print('doc file recieved')
            try:
                if (event.attachments['attach1_kind']=='audiomsg'):
                    print ('audiomsg recieved')
                    vk.messages.send(user_id=event.user_id, 
                    message='Твое голосовое сообщение конвертируется в спектрограмму и находится в обработке...')
                    audio_url = event.message_data['attachments'][0]['doc']['url']
                    audio = urllib.request.urlretrieve(filename="voice_{}.ogg".format(event.message_id), url=audio_url)
                    return audio_url
            except KeyError:
                print('@KeyError@')
                vk.messages.send(
                    user_id=event.user_id,
                    sticker_id=1             
                    )
                return 1
    except KeyError:
        print('@KeyError@')
        vk.messages.send(
            user_id=event.user_id,
            sticker_id=1             
            )
                
                
    try:     
        if (event.attachments['attach1_type']=='photo'):
            t = random.randint(1,20)
            vk.messages.send(
                user_id=event.user_id,
                sticker_id=t              
                )
            return 1
        if (event.attachments['attach1_type']=='video'):
            vk.messages.send(
                user_id=event.user_id,
                message='Крутой видос, а голосовое сообщение пришлешь?'             
                )
            return 1
        if not(event.attachments['attach1_type']=='audiomsg'):
            print('@No_Audio&Photo@')
            vk.messages.send(
                user_id=event.user_id,
                message='Пришли-ка лучше мне голосовое сообщение, дружок-пирожок'
                )
            return 1
    except KeyError:
        print('@KeyError@')
        vk.messages.send(
            user_id=event.user_id,
            sticker_id=1             
            )
        return 1

   


# ## Функция для отправки аудиофайла

# ## Основная функция работы программы

# In[ ]:

def main():
    global audio_url, files, filename, vk_doc, vk
    
    #Запускаеaudiссию и авторизируем бота через токен
    session = requests.Session()
    vk_session = vk_api.VkApi(token=token_)
    print('Initialized vk_session')
    vk = vk_session.get_api()
    #будем использовать longpoll api для онлайн-ответов от бота
    longpoll = VkLongPoll(vk_session,preload_messages=True)
    #ожидаем (listen) очередное событие event от пользователя
    i = 0
    
    '''
        Это основной цикл, где бот ожидает очередного 
        сообщения от пользователя и обрабатывает его 
    '''
    
    for event in longpoll.listen():
        i += 1
        #если сообщение -- новое и прислано нашему боту, то обрабатываем его:
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            s=agrootv
            
            '''
                Посмотрим, от кого пришло НОВОЕ сообщение и 
                найдем информацию о пользователе.
                Разбираем сначала текстовое сообщение, затем -- прикрепленный аттач.
            
            '''
            usr_info = vk_session.method('users.get', {'user_ids': event.user_id, 'fields': 'city, verified'})
            name = usr_info[0]['first_name']
            print(i,' Сообщение от ''{}: "{}"'.format(usr_info[0]['last_name'], event.text), end=' ')
            if (name == 'Ефим'):
                vk.messages.send(user_id=event.user_id,
                                 message='Извини, Ефим, но с тобой я общаться не буду'
                                )
                continue
            text_usr=event.text
            text_usr = re.sub('[!?@#$]', '', text_usr)
                
            text_from_usr_=text_usr.lower().split()
            
            for i in range(len(text_from_usr_)):
                text_from_usr=text_from_usr_[i]
                

            if event.text:
                msg = handle_text_msg(text_from_usr_=text_from_usr_,
                                    length=len(text_from_usr_),
                                    vk = vk_session.get_api(),
                                    name=name
                                   )
                vk.messages.send(
                                user_id=event.user_id,
                                message=msg
                            )
                
                
            else:
                if len(event.text)==0:
                    print('recieved attach')
                    audio = handle_attach(event,vk = vk)
                    #print(audio,peer_id)
                    if not(audio == 1):
                        print('recieved audio')
                        upload = vk_api.VkUpload(vk_session)
                        audio_url = vk_session.method('docs.getMessagesUploadServer',
                                                        {'type': 'audio_message',
                                                        'peer_id':event.user_id,
                                                        'group_id':group_id})
                        filename = "voice_{}.ogg".format(event.message_id)
                        files = [('file', ('file0.ogg', open(filename, 'rb')))]
                        audio_msg = requests.post(audio_url['upload_url'], files=files).json()
                        vk_file = audio_msg['file']
                        vk_doc = vk_session.method('docs.save', {'file': vk_file})
                        print(vk_doc[0])
                        vk.messages.send(
                                user_id=event.user_id,
                                attachment='doc{}_{}'.format(vk_doc[0]['owner_id'], vk_doc[0]['id'])
                            )
            print('====================================','Querry',i,'completed','====================================')


# In[ ]:

if __name__ == '__main__':
    main()


# In[ ]:



