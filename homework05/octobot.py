import json
import re
from datetime import datetime, timedelta

import gspread  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore
import telebot  # type: ignore
from dateutil import relativedelta  # type: ignore

bot = telebot.TeleBot("6033201656:AAFV4N5fKWUyTqg5gSSv8HsnZvmPerN_OPA")


# done
def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    if divider != date[2] or divider != date[5]:
        return False
    if divider != "/":
        date = date.replace(divider, "/")
    today = datetime.today()
    try:
        new_date = convert_date(date)
        delta = relativedelta.relativedelta(new_date, today)
        if new_date < today:
            if delta.years == delta.months == delta.days == 0:
                return True
            else:
                return False
        if delta.years >= 1:
            return False
        return True
    except ValueError:
        return False


# done
def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    url = url if ("https://" in url or "http://" in url) else ("https://" + url)
    try:
        requests.get(url)
        return True
    except Exception:
        return False


# done
def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    return datetime.strptime(date, "%d/%m/%y")


# done
def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    sheet_id = url[url.find("d/") + 2 : url.find("/edit")]
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")


# done
def access_current_sheet():
    """Обращаемся к Google-таблице"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)

    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    df = pd.DataFrame(worksheet.get_all_records())
    return worksheet, tables[max(tables)]["url"], df  # worksheet - лист 1, куда будет записываться вся информация


# done
def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    worksheet, table, dataframe = access_current_sheet()
    subjects = worksheet.col_values(1)
    if message.text == "Подключить Google-таблицу":
        info = bot.send_message(message.chat.id, "Отправьте ссылку на таблицу в следующем сообщении")
        bot.register_next_step_handler(info, connect_table)
    elif message.text == "Редактировать предметы":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить предмет")
        start_markup.row("Редактировать предмет")
        start_markup.row("Удалить предмет")
        start_markup.row("Удалить все предметы")
        info = bot.send_message(message.chat.id, "Чем я могу быть полезен?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)
    elif message.text == "Редактировать дедлайн":
        if len(subjects) < 1:
            bot.send_message(message.chat.id, "Таблица дедлайнов пока пуста!")
            start(message)
        else:
            bot.send_message(message.chat.id, "Далее мы будем работать с дедлайнами")
            start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for i in range(1, len(subjects)):
                start_markup.row(subjects[i])
            info = bot.send_message(
                message.chat.id,
                "Выберете предмет, у которого вы хотите изменить/добавить дедлайн",
                reply_markup=start_markup,
            )
            bot.register_next_step_handler(info, choose_subject)
    elif message.text == "Посмотреть дедлайны на ближайшие 7 дней":
        show_deadlines_this_week(message)
    else:
        bot.send_message(message.chat.id, "Меня не учили такой команде :'( Давайте попробуем заново")
        start(message)


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Добавить предмет":
        info = bot.send_message(message.chat.id, "Введите название нового предмета")
        bot.register_next_step_handler(info, add_new_subject)
    elif message.text == "Редактировать предмет":
        worksheet, table, dataframe = access_current_sheet()
        subjects = worksheet.col_values(1)
        if len(subjects) <= 1:
            bot.send_message(message.chat.id, "Таблица дедлайнов пока пуста!")
            start(message)
        else:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for i in range(1, len(subjects)):
                markup.row(subjects[i])
            info = bot.send_message(message.chat.id, "Выберете предмет", reply_markup=markup)
            global action
            action = -1
            bot.register_next_step_handler(info, update_subject)
    elif message.text == "Удалить предмет":
        worksheet, table, dataframe = access_current_sheet()
        subjects = worksheet.col_values(1)
        if len(subjects) < 1:
            bot.send_message(message.chat.id, "Таблица дедлайнов пока пуста!")
            start(message)
        else:
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for i in range(1, len(subjects)):
                markup.row(subjects[i])
            info = bot.send_message(message.chat.id, "Выберете предмет", reply_markup=markup)
            bot.register_next_step_handler(info, delete_subject)
    elif message.text == "Удалить все предметы":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Да")
        markup.row("Нет")
        info = bot.send_message(message.chat.id, "Вы уверены, что хотите очистить таблицу?", reply_markup=markup)
        bot.register_next_step_handler(info, choose_removal_option)
    else:
        bot.send_message(message.chat.id, "Меня не учили такой команде :'( Давайте попробуем заново")
        start(message)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    worksheet, table, dataframe = access_current_sheet()
    if not message.text.isdigit():
        info = bot.send_message(message.chat.id, "Введите номер работы")
        bot.register_next_step_handler(info, choose_deadline_action)
        return
    val = worksheet.cell(1, int(message.text) + 2).value  ############
    global CELL_col
    CELL_col = int(message.text) + 2
    if val != message.text:
        for i in range(2, int(message.text) + 2):
            worksheet.update_cell(1, i + 1, str(i - 1))
    info = bot.send_message(message.chat.id, "Введите дату дедлайна в формате дд/мм/гг")
    bot.register_next_step_handler(info, update_subject_deadline)


def show_deadlines_this_week(message):
    today = datetime.today()
    week = today + timedelta(days=7)
    worksheet, table, dataframe = access_current_sheet()
    msg = ""
    for i in range(2, len(worksheet.col_values(1)) + 1):
        for deadline in worksheet.row_values(i)[2:]:
            if week >= convert_date(deadline) >= today:
                msg += f"{worksheet.cell(i, 1).value}: {deadline}\n"
    if msg == "":
        msg += "Дедлайнов в ближайшую неделю нет, можете расслабиться!"
    bot.send_message(message.chat.id, msg)
    start(message)


# done
def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    if message.text == "Да":
        clear_subject_list(message)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Отмена удаления")
        start(message)
    else:
        bot.send_message(message.chat.id, "Меня не учили такой команде :'( Давайте попробуем заново")
        start(message)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    worksheet, table, dataframe = access_current_sheet()
    if worksheet.find(message.text) is None:
        bot.send_message(message.chat.id, "Что-то пошло не так, давайте начнем сначала")
        start(message)
        return
    cell = worksheet.find(message.text)
    global CELL_row
    CELL_row = cell.row
    info = bot.send_message(message.chat.id, "Выберете номер работы, у которой нужно изменить дедлайн")
    bot.register_next_step_handler(info, choose_deadline_action)


def update_subject_deadline(message):
    """Обновляем дедлайн"""
    date = message.text
    divider = date[2]
    if not is_valid_date(date, divider):
        info = bot.send_message(
            message.chat.id, "Дата введена неверно, введите дату снова (напоминаю, формат даты дд/мм/гг)"
        )
        bot.register_next_step_handler(info, update_subject_deadline)
    else:
        worksheet, table, dataframe = access_current_sheet()
        if divider != "/":
            date = date.replace(divider, "/")
        worksheet.update_cell(CELL_row, CELL_col, date)
        bot.send_message(
            message.chat.id,
            f"Дедлайн работы №{CELL_col - 2} успешно обновлен! Совет - не откладывайте задание на последний день)",
        )
        start(message)


def add_new_subject(message):  # из choose_subject_action
    """Вносим новое название предмета в Google-таблицу"""
    worksheet, table, dataframe = access_current_sheet()
    new_subject = message.text
    if worksheet.find(new_subject) is not None:
        info = bot.send_message(message.chat.id, "Этот предмет уже есть в таблице")
        bot.register_next_step_handler(info, add_new_subject)
        return
    worksheet.append_row([new_subject])
    info = bot.send_message(message.chat.id, "Теперь добавьте нужную URL-ссылку для этого предмета")
    bot.register_next_step_handler(info, add_new_subject_url)


def add_new_subject_url(message):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    url = message.text
    if not is_valid_url(url):
        info = bot.send_message(message.chat.id, "Некорректная ссылка, попробуйте снова")
        bot.register_next_step_handler(info, add_new_subject_url)
        return
    worksheet, table, dataframe = access_current_sheet()
    values_list = worksheet.col_values(1)
    worksheet.update_cell(len(values_list), 2, url)  ##########
    bot.send_message(message.chat.id, "Предмет успешно добавлен в таблицу!")
    start(message)


def update_subject(message):
    """Обновляем информацию о предмете в Google-таблице"""
    worksheet, table, dataframe = access_current_sheet()
    global action
    global UPD_row
    if action == -1:
        if worksheet.find(message.text) is None:
            bot.send_message(message.chat.id, "Что-то пошло не так, давайте начнем сначала")
            start(message)
            return
        subject = message.text
        cell = worksheet.find(subject)
        UPD_row = cell.row
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Название")
        markup.row("URL")
        markup.row("Все вместе")
        info = bot.send_message(message.chat.id, "Какие изменения вы хотите внести?", reply_markup=markup)
        action += 1
        bot.register_next_step_handler(info, update_subject)
    elif action == 0:
        if message.text == "Название":
            action = 1
            info = bot.send_message(message.chat.id, "Ведите новое название предмета")
            bot.register_next_step_handler(info, update_subject)
        elif message.text == "URL":
            action = 2
            info = bot.send_message(message.chat.id, "Ведите новую ссылку для предмета")
            bot.register_next_step_handler(info, update_subject)
        elif message.text == "Все вместе":
            action = 3
            info = bot.send_message(message.chat.id, "Ведите новое название предмета")
            bot.register_next_step_handler(info, update_subject)
        else:
            bot.send_message(message.chat.id, "Что-то пошло не так, давайте начнем сначала")
            action = -1
            start(message)
    elif action == 1:
        if worksheet.find(message.text) is not None:
            info = bot.send_message(
                message.chat.id, "Предмет с таким названием уже есть в таблице, предлагаю дать другое название"
            )
            bot.register_next_step_handler(info, update_subject)
            return

        worksheet.update_cell(UPD_row, 1, message.text)
        bot.send_message(message.chat.id, "Название предмета успешно изменено")
        start(message)
    elif action == 2:
        url = message.text
        if not is_valid_url(url):
            info = bot.send_message(message.chat.id, "Ссылка некорректна, попробуйте снова")
            bot.register_next_step_handler(info, update_subject)
            return
        else:
            worksheet.update_cell(UPD_row, 2, url)
            bot.send_message(message.chat.id, "Ссылка на предмет успешно изменена")
            start(message)
    elif action == 3:
        if worksheet.find(message.text) is not None:
            info = bot.send_message(
                message.chat.id, "Предмет с таким названием уже есть в таблице, предлагаю дать другое название"
            )
            bot.register_next_step_handler(info, update_subject)
            return
        worksheet.update_cell(UPD_row, 1, message.text)
        action += 1
        info = bot.send_message(message.chat.id, "Название предмета успешно изменено, осталось добавить ссылку")
        bot.register_next_step_handler(info, update_subject)
    elif action == 4:
        url = message.text
        if not is_valid_url(url):
            info = bot.send_message(message.chat.id, "Ссылка некорректна, попробуйте снова")
            bot.register_next_step_handler(info, update_subject)
            return
        else:
            worksheet.update_cell(UPD_row, 2, url)
            bot.send_message(message.chat.id, "Ссылка на предмет успешно изменена, мы отредактировали все что нужно!")
            start(message)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    worksheet, table, dataframe = access_current_sheet()
    if worksheet.find(message.text) is None:
        bot.send_message(message.chat.id, "Команда некорректна, возврат в меню")
        start(message)
        return
    cell = worksheet.find(message.text)
    worksheet.delete_rows(cell.row)
    bot.send_message(message.chat.id, "Предмет успешно удален!")
    start(message)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    worksheet, table, dataframe = access_current_sheet()
    worksheet.clear()
    worksheet.append_row(["Subject", "URL"])
    bot.send_message(message.chat.id, "Начинаем жизнь с чистого листа!")
    start(message)


@bot.message_handler(commands=["start"])
# done
def start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    try:
        json_file = open("tables.json")
    except FileNotFoundError:
        start_markup.row("Подключить Google-таблицу") #
    else:
        start_markup.row("Посмотреть дедлайны на ближайшие 7 дней")
        start_markup.row("Редактировать дедлайн")
        start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


if __name__ == "__main__":
    bot.infinity_polling()
