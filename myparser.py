import prettytable as pt
from telegram.constants import ParseMode
from telegram_bot_pagination import InlineKeyboardPaginator


class MyParser:

    def __init__(self, bot):
        self.bot = bot

    def make_table_list(self, data, message):

        paginator = InlineKeyboardPaginator(
            10,
            current_page=1,
            data_pattern='page#{page}'
        )

        table = pt.PrettyTable(['№', 'Фамилия', 'Имя'])
        data = data
        print(data)
        counter = 1
        for ln, fn in data:
            table.add_row([counter, ln, fn])
            counter += 1
        self.bot.send_message(message.chat.id, f'```{table}```', parse_mode=ParseMode.MARKDOWN_V2, reply_markup=paginator.markup)