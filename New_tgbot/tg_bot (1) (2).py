import telebot, json, random
from timeit import default_timer as timer
from telebot import types
import time

bot = telebot.TeleBot('6322715753:AAFCmRmUFNjZL4SEWXFedq0XNjrKU1gtb58')

#Список с заданиями

tip1=[
{"qestion": "1", "a": '150'},
{"qestion":"2","a": '12'},
{"qestion": "3", "a": '0,25'},
{"qestion": "4", "a": '9975'},
{"qestion":"5","a": '21'},
{"qestion": "6", "a": '1'},
{"qestion": "7", "a": '5'},
{"qestion":"8","a": '12'},
{"qestion": "9", "a": '21'},
{"qestion": "10", "a": '-7'},
{"qestion":"11","a": '-5'}
]
ids = {}



#Перевод float во время

def time_result(k):
    hour= k // 3600 #hour
    k -= hour * 3600
    minut = int(k // 60) #minutes
    k -= 60*minut
    # second = round(float(k),2) #seconds
    second = int(k) #second
    return f'{str(minut)} мин, {str(second)} сек'

#При комадне /start

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Погнали!")
    btn2 = types.KeyboardButton("Расскажи побольше о себе")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text=f"Привет, @{message.from_user.first_name}, меня зовут Гиро, и я постараюсь помочь тебе подготовится к экзамену по математике, погнали!?".format(
                         message.from_user), reply_markup=markup)
#########################################

@bot.message_handler(content_types=["text"])

#Выбор режима

def get_go(message):
    id = message.from_user.id
    if message.text=="Погнали!":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        btn4 = types.KeyboardButton("4")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id,
                         text=f"Выбери режим: \n 1.Тест \n 2.Задачи по номеру \n "
                              f"3.Отрешать первую часть ЕГЭ \n 4.Задачи на определенную тему"
                              f"".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, choose);
#########################################

def choose(message):

#Первый режим "Тест"

    if message.text == "1":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Старт")
        markup.add(btn1)
        bot.send_message(message.chat.id, text='В этом режиме тебе предстоит на вермя решить 11 задач из ЕГЭ по '
                                               'математике на время, постарайся сделать их правильно и как можно '
                                               'быстрее.\n\n '
                                               'Когда будешь готов, намжи кнопку старт',reply_markup=markup)
        bot.register_next_step_handler(message, ans_ntv)
#########################################

    elif message.text == "2":
        pass

    elif message.text == "3":
        pass

#Четврёртный режим "Задачи на определенную тему"

    elif message.text == "4":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Алгебра")
        btn2 = types.KeyboardButton("Геометрия")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text=f"Из какого раздела ты хочешь решать задачи".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, alg_topic);
#########################################


#Если в 4 режима выбрали Алгебру (самого режима пока нет)

def alg_topic(message):
    if message.text == 'Алгебра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         text=f"Выбери тему:\n\n 1.Начала теории вероятностей\n\n 2.Вероятности сложных событий\n\n "
                              f"3.Простейшие уравнения\n\n 4.Вычисления и преобразования\n\n "
                              f"5.Производная и первообразная\n\n 6.Задачи с прикладным содержанием\n\n "
                              f"7.Текстовые задачи\n\n 8.Графики функций\n\n 9.Наибольшее и наименьшее значение "
                              f"функций ".format(
                             message.from_user), reply_markup=markup)
#########################################

#Функция с заданиями для режима "Тест"

def ans_ntv(message):
    global start
    global i
    # i=0
    id = message.from_user.id
    if message.text == "Старт":
        numb_q = random.randint(0, 10)
        id = message.from_user.id
        ids.update({id:{'r':0,'numb':numb_q}})
        qestion_img = str(tip1[numb_q]['qestion'] + ".jpg")
        img = open(qestion_img, "rb")
        bot.send_photo(message.chat.id, img)
        i=1
        start = timer()
    elif tip1[ids[id]['numb']]['a']==message.text:
        bot.send_message(message.chat.id,"Молодец, правильно!")
        i += 1
        ids[id]['r']+=1
        ids[id]['numb']=random.randint(0, 10)
    else:
        bot.send_message(message.chat.id, "К сожелению ты ошибся(")
        i += 1
        ids[id]['numb'] = random.randint(0, 10)
    if i <= 11 and message.text != 'Старт':
        ids[id]['numb'] = random.randint(0, 10)
        qestion_img = str(tip1[ids[id]["numb"]]['qestion'] + ".jpg")
        # qestion_img = str(q[ids[id][numb_q]]['qestion'] + ".jpg")
        img = open(qestion_img, "rb")
        bot.send_photo(message.chat.id, img)
    elif i>11:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Погнали!")
        markup.add(btn1)
        r=ids[id]["r"]
        end = timer()
        all_time = round(float(end - start), 2)
        bot.send_message(message.chat.id,f"Ты закончил, у тебя {r} правильных ответов из 11.Ты затратил "
                                             f"{time_result(all_time)}\n\n"
                                             f"Хочешь ещё позаниматься?".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, get_go)
        return
    bot.register_next_step_handler(message, ans_ntv)
#########################################

bot.infinity_polling()
