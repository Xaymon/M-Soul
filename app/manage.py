from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route('/manageexrate')
def manageexrate():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT to_char(date_start,'DD-MM-YYYY'),curency_code, curency_name, to_char(buy,'999G999G999G999D99'),to_char(sale,'999G999G999G999D99'),roworder FROM public.exchange_rate order by date_start::date DESC "
            cur.execute(sql)
            rate_ = cur.fetchall()
            return render_template('manage/addrate.html', rate_=rate_,user=session.get("roles"))




@app.route('/saverate', methods=['POST'])
def saverate():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            currency_code = request.form['currency_code']
            buy = request.form['buy']
            sale = request.form['sale']
            curen_ = ""
            if currency_code == '01':
                curen_ = 'THB'
            elif currency_code == '02':
                curen_ = 'USD'
            else:
                curen_ = 'THB-USD'
            data = (currency_code, curen_, buy, sale)
            cur = gobal.con.cursor()
            sql = "update exchange_rate set date_end=LOCALTIMESTAMP(0) where date_end isnull and curency_code=%s"
            cur.execute(sql, (currency_code,))
            curs = gobal.con.cursor()
            sqls = "INSERT INTO exchange_rate( curency_code, curency_name, buy, sale, date_start) VALUES (%s,%s,%s,%s,LOCALTIMESTAMP(0));"
            curs.execute(sqls, (data))
            gobal.con.commit()
            return redirect(url_for('manageexrate'))


@app.route('/rate_delete/<string:id>')
def rate_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        cur = gobal.con.cursor()
        sql = "delete from exchange_rate where roworder=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('manageexrate'))