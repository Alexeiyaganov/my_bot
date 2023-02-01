import os
import sys
import json
from telebot import TeleBot
import time
import pathlib


from telegram_bot_calendar import DetailedTelegramCalendar as dtc, LSTEP as lp
from buttons_constructor import ButtonConstructor
from myparser import MyParser
from group_adder import GroupAdder
from db import DBHelper
from organizer import Org
from check import Check
import configparser


config_path = os.path.join(sys.path[0], 'settings.ini')
config = configparser.ConfigParser()
config.read(config_path)
BOT_TOKEN = config.get('Telegram', 'BOT_TOKEN')
DATE=None
EVENT_ID = None
db = DBHelper()

bot = TeleBot(BOT_TOKEN)
db = DBHelper()
org = Org(bot)
bc = ButtonConstructor()
FLAG=None
ch = Check(bot, db, EVENT_ID)
PHONE=None
ps = MyParser(bot)
ga = GroupAdder(bot, db)




@bot.message_handler(commands=['start'])
def start(message):
    markup = bc.make_main_buttons()
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я твой бот менеджмента стартов по спортивному ориентированию".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text in ["🧘 Организатор", "о"]):
        global FLAG
        FLAG="ORG"
        markup = bc.ask_phone()
        bot.send_message(message.chat.id,
                         text="Для размещение информации о мероприятии Вам необходимо поделиться своим номером телефона:",
                         reply_markup=markup)

    elif (message.text in ["🏃 Спортсмен", "c"]):
        markup = bc.make_user_buttons()
        bot.send_message(message.chat.id, text="Выбери интересующий вариант:", reply_markup=markup)

    elif (message.text in ["Будущие старты", "б"]):
        items = db.get_new_items()
        keyboard = bc.make_events_list(items)
        bot.send_message(message.chat.id, text="Выбери интересующий вариант:", reply_markup=keyboard)

    elif message.text in ["Прошедшие старты", "п"]:
        items = db.get_last_items()
        keyboard = bc.make_events_list(items)
        bot.send_message(message.chat.id, text="Выбери интересующий вариант:", reply_markup=keyboard)
    elif (message.text in ["Вернуться в главное меню", "в"]):
        markup = bc.make_main_buttons()
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммировал..")




@bot.message_handler(content_types=['contact'])
def contact(message):
    global FLAG
    if FLAG == "ORG":
        org.LINKS.append(message.contact.phone_number)
        show_calendar(message)
    else:
        global PHONE
        global EVENT_ID
        PHONE = message.contact.phone_number
        sportsmens = db.get_sportsmens_by_phone(PHONE)
        db.create_event_table(EVENT_ID)
        ch.event_id = EVENT_ID
        res = db.get_event_sportsmen_by_phone(EVENT_ID, PHONE)
        checked = []
        print(res)
        if len(res) > 0:
            for item in res[0]:
                checked.append(item)
        # print(checked)
        keyboard = bc.make_sportsmen_list(EVENT_ID, PHONE, sportsmens, checked)
        bot.send_message(message.chat.id, text="Мои спортсмены:", reply_markup=keyboard)




@bot.callback_query_handler(func=dtc.func())
def call(c):
    result, key, step = dtc().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Выбери {lp[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Вы выбрали {result}",
                              c.message.chat.id,
                              c.message.message_id)
        global DATE
        DATE = result
        org.question1(c.message, db, DATE)





def show_calendar(message):
        calendar, step = dtc().build()
        bot.send_message(message.chat.id,
                         f"Выбери {lp[step]}",
                         reply_markup=calendar)



@bot.callback_query_handler(func=lambda call: True)
def call(call):
    called_data = json.loads(call.data)
    if type(called_data) == int:
        items = db.get_item_by_id(called_data)[0]
        keyboard = bc.make_item_list(items[2:-1], called_data)
        bot.send_message(call.message.chat.id,text="" + items[1])
        bot.send_message(call.message.chat.id, text="Актуальные опции:", reply_markup=keyboard)
        bot.send_message(call.message.chat.id, text="Дата проведения: " + items[-1])
    elif type(called_data) == dict:
        if list(called_data.keys())[0] == "Информация":
            file_str = db.get_item_by_id(called_data["Информация"])[0][2]
            file_json = json.loads(file_str)
            file_type = list(file_json.keys())[0]
            file_info = bot.get_file(file_json[file_type])
            info = bot.download_file(file_info.file_path)

            file_name = ""

            if file_type == "photo":
                file_name = "Информация.jpg"
            else:
                file_name = "Информация." + file_type

            with open(file_name, 'wb+') as new_file:
                new_file.write(info)
                new_file.seek(0,0)
                bot.send_document(call.message.chat.id, new_file)

        elif list(called_data.keys())[0] == "Заявиться":
            global FLAG
            FLAG = "USR"
            global EVENT_ID
            EVENT_ID = called_data["Заявиться"]
            markup = bc.ask_phone()
            bot.send_message(call.message.chat.id,
                             text="Для Заявки Вам необходимо поделиться своим номером телефона:",
                             reply_markup=markup)
        elif list(called_data.keys())[0] == "add_sportsman":
            ch.SPORTSMAN.append(called_data["add_sportsman"][0])
            ch.checked = called_data["add_sportsman"][1]
            ch.start(call.message)

        elif list(called_data.keys())[0] == "sportsman":
            phone = called_data["sportsman"][0]
            checked = called_data["sportsman"][1]
            id = called_data["sportsman"][2]
            flag = called_data["sportsman"][3]
            if flag == 0:
                checked.remove(id)
            else:
                checked.append(id)
            sportsmen = db.get_sportsmens_by_phone(phone)
            reply_markup = bc.make_sportsmen_list(EVENT_ID, phone, sportsmen, checked)

            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

        elif list(called_data.keys())[0] == "rank":
            ch.SPORTSMAN.append(called_data["rank"])
            ch.question5(call.message)

        elif list(called_data.keys())[0] == "year":
            ch.SPORTSMAN.append(called_data["year"])
            ch.question3(call.message)

        elif list(called_data.keys())[0] == "check":
            event_id = called_data["check"][0]
            checked = called_data["check"][1]
            items = []
            for item in checked:
                row = db.get_sportsman_by_id(item)
                if len(row) != 0:
                    items.append(row)
            db.add_sportsmen_to_event(event_id, items)
            reply_markup = bc.make_buttons_after_checking(event_id)
            bot.send_message(call.message.chat.id,
                             text="Поздравляем! Вы успешно зарегестрировались!",
                             reply_markup=reply_markup)

        elif list(called_data.keys())[0] == "check_list":
            event_id = called_data["check_list"]
            data = db.get_event_list(event_id)
            ps.make_table_list(data, call.message)
            bc.make_user_buttons()

        elif list(called_data.keys())[0] == "main_menu":
            bc.make_user_buttons()

        elif list(called_data.keys())[0] == "group":
            phone = called_data["group"][0]
            checked = called_data["group"][1]
            id = called_data["group"][2]
            flag = called_data["group"][3]
            if flag == 0:
                checked.remove(id)
            else:
                checked.append(id)
            items = db.get_groups_by_phone(phone)
            reply_markup = bc.make_group_list(items, checked)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=reply_markup)

        elif list(called_data.keys())[0] == "add_group":
            ga.GROUP = []
            ga.GROUP.append(called_data["add_group"][0])
            ga.start(call.message)


        elif list(called_data.keys())[0] == "save_groups":
            phone = called_data["save_groups"][0]
            checked = called_data["save_groups"][1]
            items = []
            for item in checked:
                row = db.get_group_by_id(item)
                if len(row) != 0:
                    items.append(row)
            db.add_groups_to_event(event_id, items)
            org.final_push(call.message, db, DATE)

bot.polling()

# while True:
#     try:
#         bot.polling(none_stop=True, interval=0, timeout=0)
#     except:
#         time.sleep(2)