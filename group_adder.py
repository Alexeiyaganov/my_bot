from buttons_constructor import ButtonConstructor




class GroupAdder:
    def __init__(self, bot, db):
        self.bot = bot
        self.GROUP = []
        self.bc = ButtonConstructor()
        self.db = db
        self.checked = []

    def start(self, message):
        m5 = self.bot.send_message(message.chat.id, text="Введите название группы:")
        self.bot.register_next_step_handler(m5, self.ask_group)

    def ask_group(self, message):
        self.GROUP.append(message.text)
        markup = self.bc.make_continue_button()
        m = self.bot.send_message(message.chat.id, text="Введите минимальный год рождения:", reply_markup=markup)
        self.bot.register_next_step_handler(m, self.ask_age_since)


    def ask_age_since(self, message):
        if message.text == "Пропустить":
            markup = self.bc.make_continue_button()
            self.GROUP.append(0)
            self.GROUP.append(0)
            m = self.bot.send_message(message.chat.id, text="Введите стоимость:", reply_markup=markup)
            self.bot.register_next_step_handler(m, self.ask_price)
        else:
            try:
                since_age = int(message.text)
                self.GROUP.append(since_age)
                m = self.bot.send_message(message.chat.id, text="Введите максимальный год рождения:")
                self.bot.register_next_step_handler(m, self.ask_age_to)
            except:
                markup = self.bc.make_continue_button()
                m = self.bot.send_message(message.chat.id, text="Не получилось прочитать число, попробуйте еще раз:", reply_markup=markup)
                self.bot.register_next_step_handler(m, self.ask_age_since)


    def ask_age_to(self, message):
        try:
            since_age = int(message.text)
            self.GROUP.append(since_age)
            m = self.bot.send_message(message.chat.id, text="Введите цену:")
            self.bot.register_next_step_handler(m, self.ask_price)
        except:
            markup = self.bc.make_continue_button()
            m = self.bot.send_message(message.chat.id, text="Не получилось прочитать число, попробуйте еще раз:", reply_markup=markup)
            self.bot.register_next_step_handler(m, self.ask_age_since)

    def ask_price(self, message):
        if message.text == "Пропустить":
            self.GROUP.append(0)
        else:
            try:
                self.GROUP.append(int(message.text))
            except:
                markup = self.bc.make_continue_button()
                m = self.bot.send_message(message.chat.id, text="Не получилось прочитать целое число, попробуйте еще раз:",
                                          reply_markup=markup)
                self.bot.register_next_step_handler(m, self.ask_price)
        self.final_push(message)

    def final_push(self, message):
        price = self.GROUP.pop()
        age_to = self.GROUP.pop()
        age_from = self.GROUP.pop()
        group_name = self.GROUP.pop()
        phone = self.GROUP.pop()
        self.db.add_group(org_phone=phone, group_name=group_name, age_from=age_from, age_to=age_to, price=price)
        items = self.db.get_groups_by_phone(phone)[0]
        markup = self.bc.make_group_list(phone, items, self.checked)
        self.bot.send_message(message.chat.id, text="Группа добавлена!",
                              reply_markup=markup)

