from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *
from flask.helpers import flash


@app.route('/dm')
def dm():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            # cur = gobal.con.cursor()
            # sql = """SELECT curency_code,curency_name || '-' ||  curency_name2 , roworder FROM public.tb_currencytype order by roworder"""
            # cur.execute(sql)
            # rate_ = cur.fetchall()

            # curs = gobal.con.cursor()
            # sql_cur = "SELECT curency_code,curency_name FROM public.tb_addcurrency"
            # curs.execute(sql_cur)
            # curent = curs.fetchall()
            return render_template('bank/dm.html')
@app.route('/wm')
def wm():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT curency_code,curency_name || '-' ||  curency_name2 , roworder FROM public.tb_currencytype order by roworder"""
            cur.execute(sql)
            rate_ = cur.fetchall()

            curs = gobal.con.cursor()
            sql_cur = "SELECT curency_code,curency_name FROM public.tb_addcurrency"
            curs.execute(sql_cur)
            curent = curs.fetchall()
            return render_template('manage/currency_type.html', rate_=rate_,curent=curent)
@app.route('/tm')
def tm():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT curency_code,curency_name || '-' ||  curency_name2 , roworder FROM public.tb_currencytype order by roworder"""
            cur.execute(sql)
            rate_ = cur.fetchall()

            curs = gobal.con.cursor()
            sql_cur = "SELECT curency_code,curency_name FROM public.tb_addcurrency"
            curs.execute(sql_cur)
            curent = curs.fetchall()
            return render_template('manage/currency_type.html', rate_=rate_,curent=curent)