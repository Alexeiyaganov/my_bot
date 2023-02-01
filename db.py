import sqlite3
from datetime import datetime


class DBHelper:
    def __init__(self, dbname="bd/bot_bd.db"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS main_tb (id INTEGER PRIMARY KEY, organizer TEXT NOT NULL, event_name TEXT, info TEXT, checkurl TEXT, checking TEXT, location TEXT, split TEXT, map TEXT, event_date TEXT NOT NULL, comment text)"
        stmt1 = "CREATE TABLE IF NOT EXISTS sportsman_tb (id INTEGER PRIMARY KEY, org_phone TEXT NOT NULL, last_name TEXT NOT NULL, first_name TEXT, year_born INTEGER, team TEXT, rank TEXT, comment text)"
        self.conn.execute(stmt, stmt1)
        self.conn.commit()

    def create_event_table(self, name):
        name_tb = 'check_tb_'+str(name)
        stmt = "CREATE TABLE IF NOT EXISTS " + name_tb +"(id integer PRIMARY KEY, org_phone text NOT NULL, last_name text NOT NULL, first_name text, year_born integer, team text, rank text, comment text)"
        name_tb = (name_tb,)
        self.conn.execute(stmt)
        self.conn.commit()

    def add_event(self, org_phone: str, event_name: str, event_date: str, info: str, checkurl: str, check_here: str, location: str, split: str):
        stmt = "INSERT INTO main_tb (org_phone, event_name, event_date, info, checkurl, check_here, location, split) VALUES (?, ?, ?, ?, ?, ?, ?, ?) RETURNING id"
        args = (org_phone, event_name, event_date, info, checkurl, check_here, location, split)
        id = self.conn.execute(stmt, args)
        self.conn.commit()
        return id

    # def delete_item(self, item_text):
    #     stmt = "DELETE FROM items WHERE description = (?)"
    #     args = (item_text, )
    #     self.conn.execute(stmt, args)
    #     self.conn.commit()

    def get_new_items(self):
        stmt = "SELECT id, event_date, event_name  FROM main_tb WHERE date('now') <= event_date "
        return [x[:] for x in self.conn.execute(stmt)]

    def get_last_items(self):
        stmt = "SELECT id, event_date, event_name  FROM main_tb WHERE date('now') >= event_date "
        return [x[:] for x in self.conn.execute(stmt)]

    def get_item_by_id(self, item_id):
        stmt = "SELECT * FROM main_tb WHERE id = ?"
        id_val=(item_id,)
        self.conn.execute(stmt, id_val)
        return [x[1:] for x in self.conn.execute(stmt, id_val)]


    def add_sportsman(self, org_phone: str, last_name: str, first_name: str, year_born: int, team: str, rank: str, comment: str):
        stmt = "INSERT INTO sportsmen_tb (org_phone, last_name, first_name, year_born, team, rank, comment) VALUES (?, ?, ?, ?, ?, ?, ?)"
        args = (org_phone, last_name, first_name, year_born, team, rank, comment)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_sportsmens_by_phone(self, phone):
        stmt = "SELECT * FROM sportsmen_tb WHERE org_phone = ?"
        phone_val = (phone,)
        # self.conn.execute(stmt, phone_val)
        return [x[:] for x in self.conn.execute(stmt, phone_val)]

    def get_event_sportsmen_by_phone(self, event, phone):
        table = "check_tb_" + str(event)
        stmt = "SELECT id FROM " + table + " WHERE org_phone = ?"
        phone_val = (phone,)
        return [x[:] for x in self.conn.execute(stmt, phone_val)]

    def get_sportsman_by_id(self, sportsman_id):
        stmt = "SELECT * FROM sportsmen_tb WHERE id = ?"
        id_val=(sportsman_id,)
        return [x[1:] for x in self.conn.execute(stmt, id_val)]


    def add_sportsmen_to_event(self, event_id, items):
        for item in items:
            stmt = "INSERT INTO " + "check_tb_" + str(event_id) + " (org_phone, last_name, first_name, year_born, team, rank, comment) VALUES (?, ?, ?, ?, ?, ?, ?)"
            args = (item[0][0], item[0][1], item[0][2], int(item[0][3]), item[0][4], item[0][5], item[0][6])
            self.conn.execute(stmt, args)
        self.conn.commit()

    def get_event_list(self, event_id):
        table = "check_tb_" + str(event_id)
        stmt = "SELECT * FROM " + table
        res = []
        for x in self.conn.execute(stmt):
            x = x[2:-4]
            x = (x[0][:10], x[0][:10])
            res.append(x)
        return res

    def get_groups_by_phone(self, phone):
        stmt = "SELECT * FROM groups_tb WHERE org_phone = ?"
        phone_val = (phone,)
        return [x[:] for x in self.conn.execute(stmt, phone_val)]


    def add_group(self, org_phone: str, group_name: str, age_from: int, age_to: int, price: int):
        stmt = "INSERT INTO main_tb (org_phone, group_name, min_age, max_age, price) VALUES (?, ?, ?, ?, ?)"
        args = (org_phone, group_name, age_from, age_to, price)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_group_by_id(self, id):
        stmt = "SELECT * FROM group_tb WHERE id = ?"
        id_val = (id,)
        return [x[1:] for x in self.conn.execute(stmt, id_val)]

    def add_groups_to_event(self):
        pass

    def create_groups_event_table(self, name):
        name_tb = 'group_tb_'+str(name)
        stmt = "CREATE TABLE IF NOT EXISTS " + name_tb +"(id integer PRIMARY KEY, org_phone text NOT NULL, group_name text NOT NULL, min_age integer, max_age integer, price integer)"
        self.conn.execute(stmt)
        self.conn.commit()

