from telebot import types
import json
from datetime import datetime



class ButtonConstructor:
    def __init__(self):
        pass


    def make_main_buttons(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.InlineKeyboardButton("🏃 Спортсмен")
        btn2 = types.InlineKeyboardButton("🧘 Организатор")
        markup.add(btn1, btn2)
        return markup

    def ask_phone(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        contact = types.KeyboardButton('Поделиться номером телефона', request_contact=True)
        markup.add(contact)
        return markup




    def ask_check(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.InlineKeyboardButton('Открыть заявку тут')
        btn2 = types.InlineKeyboardButton('Ссылка на внешнюю заявку')
        btn3 = types.InlineKeyboardButton('Без заявки')
        markup.add(btn1, btn2, btn3)
        return markup



    def make_user_buttons(self):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.InlineKeyboardButton("Будущие старты")
        btn2 = types.InlineKeyboardButton("Прошедшие старты")
        back = types.InlineKeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        return markup

    def make_events_list(self, items):
        markup = types.InlineKeyboardMarkup()

        for value in items:
            call_data = json.dumps(value[0])
            markup.add(types.InlineKeyboardButton(text=" ".join(value[1:]),
                                              callback_data=call_data))

        return markup

    def make_item_list(self, item, id):
        markup = types.InlineKeyboardMarkup()

        strings = ["Информация", "Заявка", "Заявиться", "location", "splits", "map"]

        for index, value in enumerate(item):
            if value != None and value != '' and value != 0:
                call_data = json.dumps({strings[index]: id}, ensure_ascii=False)
                url = None
                if strings[index] == "Заявка":
                    url = value
                    call_data=None
                markup.add(types.InlineKeyboardButton(text=strings[index], callback_data=call_data, url=url))
        return markup

    def make_rank_list(self):
        ranks=["б.р.", "3ю", "2ю", "1ю", "3р", "2р", "1р", "кмс", "мс", "мсмк", "змс"]

        markup = types.InlineKeyboardMarkup()

        for item in range(len(ranks)//3):
            call_data = json.dumps({"rank": ranks[item * 3]}, ensure_ascii=False)
            btn1 = types.InlineKeyboardButton(text=ranks[item * 3], callback_data=call_data)
            call_data = json.dumps({"rank": ranks[item * 3 + 1]}, ensure_ascii=False)
            btn2 = types.InlineKeyboardButton(text=ranks[item * 3 + 1], callback_data=call_data)
            call_data = json.dumps({"rank": ranks[item * 3 + 1]}, ensure_ascii=False)
            btn3 = types.InlineKeyboardButton(text=ranks[item * 3 + 2], callback_data=call_data)
            markup.row(btn1, btn2, btn3)
        call_data = json.dumps({"rank": "мсмк"}, ensure_ascii=False)
        btn1 = types.InlineKeyboardButton(text="мсмк", callback_data=call_data)
        call_data = json.dumps({"rank": "змс"}, ensure_ascii=False)
        btn2 = types.InlineKeyboardButton(text="змс", callback_data=call_data)
        markup.row(btn1, btn2)
        return markup

    def make_year_list(self):
        markup = types.InlineKeyboardMarkup()

        tmp = 1930

        while int(datetime.now().year) > tmp:
            call_data = json.dumps({"year": tmp}, ensure_ascii=False)
            tmp += 1
            btn1 = types.InlineKeyboardButton(text=tmp, callback_data=call_data)
            call_data = json.dumps({"year": tmp}, ensure_ascii=False)
            tmp += 1
            btn2 = types.InlineKeyboardButton(text=tmp, callback_data=call_data)
            call_data = json.dumps({"year": tmp}, ensure_ascii=False)
            tmp += 1
            btn3 = types.InlineKeyboardButton(text=tmp, callback_data=call_data)
            call_data = json.dumps({"year": tmp}, ensure_ascii=False)
            tmp += 1
            btn4 = types.InlineKeyboardButton(text=tmp, callback_data=call_data)
            call_data = json.dumps({"year": tmp}, ensure_ascii=False)
            tmp += 1
            btn5 = types.InlineKeyboardButton(text=tmp, callback_data=call_data)
            markup.row(btn1, btn2, btn3, btn4, btn5)

        return markup

    def make_sportsmen_list(self, event_id: int, phone: str, items, checked: list):
        markup = types.InlineKeyboardMarkup()
        print("got_list")
        print(items)
        print(checked)
        for value in items:
            if value is not []:
                flag = 0
                id = value[0]
                year = value[4]
                string = ""
                for i in value[2:]:
                    string += str(i) + " "
                for item in checked:
                    if id == item[0]:
                        call_data1 = json.dumps({"sportsman_edit": [phone, checked, id, 0]}, ensure_ascii=False)
                        call_data2 = json.dumps({"sportsman": [phone, checked, id, 0, year]}, ensure_ascii=False)
                        print("1111111")
                        btn1 = types.InlineKeyboardButton(text=string, callback_data=call_data1)
                        btn2 = types.InlineKeyboardButton(text="✅", callback_data=call_data2)
                        markup.row(btn1, btn2)
                        flag = 1
                        break
                    else:
                        continue
                if flag == 0:
                    call_data1 =json.dumps({"sportsman_edit": [phone, checked, id, 0]}, ensure_ascii=False)
                    call_data2 = json.dumps({"sportsman": [phone, checked, id, 1, year]}, ensure_ascii=False)
                    print("222222")
                    btn1 = types.InlineKeyboardButton(text=string, callback_data=call_data1)
                    btn2 = types.InlineKeyboardButton(text="✔", callback_data=call_data2)
                    markup.row(btn1, btn2)
        call_data = json.dumps({"add_sportsman": [phone, checked]}, ensure_ascii=False)
        markup.add(types.InlineKeyboardButton(text="Добавить спортсмена", callback_data=call_data))
        if len(checked) > 0:
            call_data = json.dumps({"check": [event_id, checked]}, ensure_ascii=False)
            markup.add(types.InlineKeyboardButton(text="Заявить", callback_data=call_data))
        print("ok")
        return markup

    def make_buttons_after_checking(self, event_id):
        markup = types.InlineKeyboardMarkup()
        call_data1 = json.dumps({"check_list": event_id}, ensure_ascii=False)
        call_data2 = json.dumps({"main_menu": None}, ensure_ascii=False)
        btn1 = types.InlineKeyboardButton(text="Список заявившихся", callback_data=call_data1)
        btn2 = types.InlineKeyboardButton(text="В главное меню", callback_data=call_data2)
        markup.row(btn1, btn2)
        return markup

    def without_info(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.InlineKeyboardButton("Не выкладывать информацию")
        markup.add(btn1)
        return markup

    def make_continue_button(self):
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.InlineKeyboardButton("Пропустить")
        markup.add(btn1)
        return markup

    def make_group_list(self, phone, items, checked):
        markup = types.InlineKeyboardMarkup()
        if items != []:
            for value in items:
                if value is not []:
                    id = value[0]
                    string = str(value[2]) + " c " + str(value[3]) + " до " + str(value[4])
                    if id in checked:
                        call_data1 = json.dumps({"group_edit": [phone, checked, id]}, ensure_ascii=False)
                        call_data2 = json.dumps({"group": [phone, checked, id, 0]}, ensure_ascii=False)
                        btn1 = types.InlineKeyboardButton(text=string, callback_data=call_data1)
                        btn2 = types.InlineKeyboardButton(text="✅", callback_data=call_data2)
                        markup.row(btn1, btn2)
                    else:
                        call_data1 = json.dumps({"group_edit": [phone, checked, id]}, ensure_ascii=False)
                        call_data2 = json.dumps({"group": [phone, checked, id, 1]}, ensure_ascii=False)
                        btn1 = types.InlineKeyboardButton(text=string, callback_data=call_data1)
                        btn2 = types.InlineKeyboardButton(text="✔", callback_data=call_data2)
                        markup.row(btn1, btn2)

        call_data = json.dumps({"add_group": [phone]}, ensure_ascii=False)
        markup.add(types.InlineKeyboardButton(text="Добавить группу", callback_data=call_data))
        if len(checked) > 0:
            call_data = json.dumps({"save_groups": [phone, checked]}, ensure_ascii=False)
            markup.add(types.InlineKeyboardButton(text="Сохранить", callback_data=call_data))
        return markup

    def make_check_group_list(self, checked, id, year, groups):
        markup = types.InlineKeyboardMarkup()
        buttons=[]
        print(checked)
        for item in groups:
            if (item[1] <= year <= item[2]) or (item[1] == 0 and item[2] == 0):
                call_data = json.dumps({"choose_group": [item[0], checked, id]}, ensure_ascii=False)
                print(call_data)
                btn = types.InlineKeyboardButton(text=item[0], callback_data=call_data)
                buttons.append(btn)
        markup.row(*buttons)
        return markup

