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

            return render_template('manage/bank.html', rate_=rate_)

@app.route('/save_bank', methods=['POST'])
def save_bank():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = """INSERT INTO tb_bank(
                         bank_id, bank_name, currency)
                         values(%s,%s,%s)
                  """
            
            bank_id = request.form['​bank_id']
            bank_name = request.form['​​bank_name']
            currency = request.form['currency']
            data = (bank_id, bank_name, currency)
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
