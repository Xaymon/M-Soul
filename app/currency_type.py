from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route('/currencytype')
def currencytype():
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

@app.route('/save_currency', methods=['POST'])
def save_currency():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = """INSERT INTO public.tb_currencytype(
                         curency_code,curency_name,curency_name2)
                         values(%s,%s,%s)
                  """
            
            curency_code = request.form['curency_code']
            curency_name = request.form['curency_name']
            curency_name2 = request.form['curency_name2']
            data = (curency_code, curency_name, curency_name2)
            cur.execute(sql, (data))
            gobal.con.commit()
            return redirect(url_for('currencytype'))

@app.route('/currency_delete/<string:id>')
def currency_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from public.tb_currencytype where roworder=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('currencytype'))
