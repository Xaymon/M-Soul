from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route('/manage_rate')
def manage_rate():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT curency_code,curency_name, roworder FROM public.tb_addcurrency order by roworder"""
            cur.execute(sql)
            rate_ = cur.fetchall()

            return render_template('manage/addcurrency.html', rate_=rate_)

@app.route('/save_ratee', methods=['POST'])
def save_ratee():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = """INSERT INTO public.tb_addcurrency(
                         curency_code,curency_name)
                         values(%s,%s)
                  """
            
            curency_code = request.form['curency_code']
            curency_name = request.form['curency_name']
            data = (curency_code, curency_name)
            cur.execute(sql, (data))
            gobal.con.commit()
            return redirect(url_for('manage_rate'))

@app.route('/ratee_delete/<string:id>')
def ratee_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        cur = gobal.con.cursor()
        sql = "delete from public.tb_addcurrency where roworder=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('manage_rate'))

@app.route('/update_currency/<string:id>', methods=['POST'])
def update_currency(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            curency_code = request.form['curency_code']
            curency_name = request.form['curency_name']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.tb_addcurrency set curency_code=%s, curency_name=%s where roworder=%s',(curency_code, curency_name,(id,)))
            gobal.con.commit()
            return redirect(url_for('manage_rate'))