import datetime
import sqlite3
import matplotlib as plt
import pyodbc
import tkinter.messagebox as mb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def grafic_return():
    a = []
    b = []

def get_timestamp(y, m, d):
    return datetime.datetime.timestamp(datetime.datetime(y, m, d)) # хранение типа данных date, (тип отсутвует в бд)

def get_date(tmstmp):
    return datetime.datetime.fromtimestamp(tmstmp).date() # вывод типа данных дата

def get_timestamp_sting(s):
    t = s.split('-')
    return get_timestamp(int(t[2]), int(t[1]), int(t[0]))

def get_statistic_data():
    all_data1 = []
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        querty = """SELECT * from payments"""
        cursor.execute(querty)
        all_data1 = cursor
    return all_data1

def get_most_expens_item(): #самая затратная сфера
    data = get_statistic_data()
    return max(list(data), key=lambda x:x['amount'])['name']

def alina(): #сумма расходов по этой сфере
    data = get_statistic_data()
    allina = get_most_expens_item()
    p = 2
    count = 0
    for payments in data:
        if payments['expenses_id'] == allina:
            count += payments["amount"]
    return count

def srednaya_summa(): #средняя сумма расходов за период
    data1 = get_statistic_data()
    count = 0
    for payments in data1:
        if payments['amount']:
            count += payments["amount"]
    return count

def get_most_common_item():
    data = get_statistic_data()
    quantily = {}
    for payments in data:
        if payments['expense_id'] in quantily:
            quantily[payments['expense_id']]['qty'] += 1
        else:
            quantily[payments['expense_id']] = {'qty': 1, "name": payments['expense_id']}
    return max(quantily.values(), key=lambda x: ['qty'])['name']

qw = 0
def get_most_expens_day():
    global qw
    data = get_statistic_data()
    week_days = ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье")
    days = {}
    for payments in data:
        if get_date(payments['payment_date']).weekday() in days:
            days[get_date(payments['payment_date']).weekday()] += payments['amount']
        else:
            days[get_date(payments['payment_date']).weekday()] = payments['amount']
    qw = payments['payment_date']
    return week_days[max(days, key=days.get)]

def get_most_expens_day_summ():
    get_most_expens_day()
    global qw
    date1 = get_statistic_data()
    count = 0
    for payments in date1:
        if payments['payment_date'] == qw:
            count += payments['amount']
    return count

def get_most_exp_month():
    data = get_statistic_data()
    month_list = ('0', "Январь", "Ферваль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь")
    days = {}
    for payments in data:
        if get_date(payments['payment_date']).month in days:
            days[get_date(payments['payment_date']).month] += payments['amount']
        else:
            days[get_date(payments['payment_date']).month] = payments['amount']
        return month_list[max(days, key=days.get)]

def form_plus():
    all_data = {'ac':{}, 'name':[]}
    result = {}
    querty = get_statistic_data()
    result = dict(querty)
    all_data['ac'] = {result[k]: k for k in result}
    all_data['expense_id'] = [v for v in result.values()]
    return all_data

def insert_payments(insert_payments):
    success = False
    with sqlite3.connect('database.db') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        querty = """ INSERT INTO payments(amount, payment_date, expense_id) VALUES (?, ?, ?)"""
        cursor.execute(querty, insert_payments)
        db.commit()
        success = True
    return success

def form_del_sfere(sfera): #удаление сферы через выпадающую форму
    flag = False
    data = get_statistic_data()
    for payments in data:
        if payments['expenses_id'] == sfera:
            with sqlite3.connect("database.db") as db:
                db.row_factory = sqlite3.Row
                cursor = db.cursor()
                querty = """DELETE FROM "payments" WHERE expenses_id=%a"""
                cursor.execute(querty, sfera)
                flag = True
    return flag

def form_del(): #удаление последнего ввода
    flag = False
    data = get_statistic_data()
    a = 0
    for payments in data:
        if payments['id']:
            a += 1
    if a > 1:
        with sqlite3.connect("database.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("""DELETE FROM payments WHERE id = (SELECT max(id) From payments)""")
            flag = True
    else:
        flag =False
    return flag

def date_proverka(d, a):
    flag = False
    with sqlite3.connect("database.db") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        params = (d, a)
        querty = """SELECT * from payments WHERE payment_date BETWEEN %d AND %a""" %params
        cursor.execute(querty)
        all_data = cursor
        print(all_data)
    return all_data
