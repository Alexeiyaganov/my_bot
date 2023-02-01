from buttons_constructor import ButtonConstructor
import json

class Org:
    def __init__(self, bot):
        self.LINKS=[]
        self.bot = bot
        self.bc = ButtonConstructor()


    def question1(self, message, db, date):
        self.LINKS.append(message.text)
        m1 = self.bot.send_message(message.chat.id, 'Введите название старта')
        self.bot.register_next_step_handler(m1, self.question2, db, date)

    def question2(self, message, db, date):
        self.LINKS.append(message.text)
        markup = self.bc.without_info()
        m2 = self.bot.send_message(message.chat.id, text="Загрузите  информацию о мероприятии(документ(pdf, zip) или картика", reply_markup=markup)
        self.bot.register_next_step_handler(m2, self.question3, db, date)


    def question3(self, message, db, date):
        if message.text == "Не выкладывать информацию":
            self.LINKS.append("")
        if message.document == None and message.photo == None:
            m3 = self.bot.send_message(message.chat.id, text="Загрузка документа не получилась, попробуйте снова!")
            self.bot.register_next_step_handler(m3, self.question3, db, date)
        else:
            if message.document == None:
                photo_id = message.photo[-1].file_id
                photo = json.dumps({"photo": photo_id})
                self.LINKS.append(photo)
            else:
                document_id = message.document.file_id
                document_name = message.document.file_name
                document_type = document_name.split('.')[-1]
                document = json.dumps({document_type: document_id})
                self.LINKS.append(document)
        markup = self.bc.ask_check()
        m4 = self.bot.send_message(message.chat.id, text="Разместить заявку тут или прикрепить ссылку на внешний источник?", reply_markup=markup)
        self.bot.register_next_step_handler(m4, self.question4, db, date)

    def question4(self, message, db, date):
        if message.text == "Открыть заявку тут":
            self.LINKS.append("")
            self.LINKS.append(1)
            items = db.get_groups_by_phone(self.LINKS[0])[0]
            reply_markup = self.bc.make_group_list(self.LINKS[0], items, [])
            self.bot.send_message(message.chat.id, text="Ваши группы:", reply_markup=reply_markup)


        elif message.text == "Ссылка на внешнюю заявку":
            self.LINKS.append(message.text)
            self.LINKS.append(0)
        else:
            self.LINKS.append("")
            self.LINKS.append(0)
        self.final_push(message,db, date)







    def final_push(self, message, db, date):
        check_here = self.LINKS.pop()
        checkurl = self.LINKS.pop()
        info = self.LINKS.pop()
        event_name = self.LINKS.pop()
        phone = self.LINKS.pop()
        db.add_event(org_phone=phone, event_name=event_name, event_date=date, info=info, checkurl=checkurl, check_here=check_here, location="", split="")
        db.create_groups_event_table()
        db.add_groups_to_event(event_id, items)
        markup = self.bc.make_user_buttons()
        self.bot.send_message(message.chat.id, text="Поздравляем! Информация о мероприятии добавлена", reply_markup=markup)


