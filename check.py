from buttons_constructor import ButtonConstructor

class Check:
    def __init__(self, bot, db, event_id):
        self.SPORTSMAN=[]
        self.bot = bot
        self.event_id = event_id
        self.bc = ButtonConstructor()
        self.db = db
        self.checked =[]


    def start(self, message):
        m1 = self.bot.send_message(message.chat.id, 'Введите фамилию')
        self.bot.register_next_step_handler(m1, self.question1)


    def question1(self, message):
        self.SPORTSMAN.append(message.text)
        m2 = self.bot.send_message(message.chat.id, 'Введите Имя')
        self.bot.register_next_step_handler(m2, self.question2)

    def question2(self, message):
        self.SPORTSMAN.append(message.text)
        markup = self.bc.make_year_list()
        self.bot.send_message(message.chat.id, 'Введите Год Рождения:                  ', reply_markup=markup)

    def question3(self, message):
        m3 = self.bot.send_message(message.chat.id, 'Введите Название Команды:')
        self.bot.register_next_step_handler(m3, self.question4)

    def question4(self, message):
        self.SPORTSMAN.append(message.text)
        markup = self.bc.make_rank_list()
        self.bot.send_message(message.chat.id, 'Выберите разряд:', reply_markup=markup)
        # self.bot.register_next_step_handler(m3, self.question5)

    def question5(self, message):
        m3 = self.bot.send_message(message.chat.id, 'Введите Комментарий:')
        self.bot.register_next_step_handler(m3, self.final_push)




    def final_push(self, message):
        comment = message.text
        rank = self.SPORTSMAN.pop()
        team = self.SPORTSMAN.pop()
        year = self.SPORTSMAN.pop()
        first_name = self.SPORTSMAN.pop()
        last_name = self.SPORTSMAN.pop()
        phone = self.SPORTSMAN.pop()
        self.db.add_sportsman(org_phone=phone, last_name=last_name, first_name=first_name, year_born=year, team=team, rank=rank, comment = comment)
        sportsmen = self.db.get_sportsmens_by_phone(phone)
        markup = self.bc.make_sportsmen_list(self.event_id, phone, sportsmen, self.checked)
        self.bot.send_message(message.chat.id, text="Поздравляем! Спортсмен добавлен!", reply_markup=markup)
