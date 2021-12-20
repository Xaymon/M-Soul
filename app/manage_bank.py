from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route('/managebank')
def managebank():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT bank_id, bank_name, currency, roworder FROM public.tb_bank order by roworder "
            cur.execute(sql)
            rate_ = cur.fetchall()

            curs = gobal.con.cursor()
            sql_cur = "SELECT curency_code,curency_name FROM public.tb_addcurrency"
            curs.execute(sql_cur)
            curent = curs.fetchall()

            return render_template('manage/bank.html', rate_=rate_, curent = curent)

@app.route('/save_bank', methods=['POST'])
def save_bank():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = """INSERT INTO tb_bank(
                         bank_id, bank_name, currency,bank_loca)
                         values(%s,%s,%s,%s)
                  """
            
            bank_id = request.form['​bank_id']
            bank_name = request.form['​​bank_name']
            currency = request.form['currency']
            bank_loca = request.form['bank_loca']
            data = (bank_id, bank_name, currency,bank_loca)
            cur.execute(sql, (data))
            gobal.con.commit()
            return redirect(url_for('managebank'))

@app.route('/bank_delete/<string:id>')
def bank_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        cur = gobal.con.cursor()
        sql = "delete from public.tb_bank where roworder=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('managebank'))
