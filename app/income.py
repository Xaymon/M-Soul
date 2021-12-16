from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route('/income')
def income():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """
                    SELECT roworder,bill_no, item_name, bill_date, cash_kip, cash_baht, cash_dollar FROM public.tb_income order by roworder DESC
                  """

                    # SELECT roworder,bill_no, item_name, bill_date, cash_kip, cash_baht, cash_dollar FROM public.tb_outcome order by roworder DESC
                    # VALUES(%s,%s,%s, LOCALTIMESTAMP(0),%s,%s,%s)"""
            cur.execute(sql)
            rate_trans = cur.fetchall()
            return render_template('In-Outcome/income.html', rate_trans=rate_trans)

@app.route('/save_income', methods=['POST'])
def save_income():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = """INSERT INTO public.tb_income (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
                     VALUES(%s,%s,%s,%s, %s)
                  """
            item_name = request.form['item_name']
            cash_kip = request.form['cash_kip']
            cash_baht = request.form['cash_baht']
            cash_dollar = request.form['cash_dollar']
            bill_date = request.form['bill_date']

            data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            print(data)
            cur.execute(sql, data,)
            gobal.con.commit()
            return redirect(url_for('income'))

@app.route('/income_delete/<string:id>')
def income_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from public.tb_income where roworder=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('income'))

@app.route('/update_income/<string:id>', methods=['POST'])
def update_income(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            item_name = request.form['item_name']
            cash_kip =  request.form['cash_kip']
            cash_baht = request.form['cash_baht']
            cash_dollar = request.form['cash_dollar']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.tb_income set item_name=%s, cash_kip=%s, cash_baht=%s, cash_dollar=%s where roworder=%s',(item_name, cash_kip, cash_baht, cash_dollar,(id,)))
            gobal.con.commit()
            return redirect(url_for('income'))
