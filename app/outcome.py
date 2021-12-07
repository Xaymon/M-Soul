from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route('/outcome')
def outcome():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """
                    SELECT roworder,bill_no, item_name, to_char(bill_date,'DD-MM-YYYY HH24:MI:SS') as bill_date,
                    '₭'||to_char(cash_kip,'999G999G999D99') as cash_kip,
                    '฿'||to_char(cash_baht,'999G999G999D99') as cash_baht,
                    '$'||to_char(cash_baht,'999G999G999D99') as cash_dollar FROM public.tb_outcome order by roworder DESC
                  """

                    # SELECT roworder,bill_no, item_name, bill_date, cash_kip, cash_baht, cash_dollar FROM public.tb_outcome order by roworder DESC
                    # VALUES(%s,%s,%s, LOCALTIMESTAMP(0),%s,%s,%s)"""
            cur.execute(sql)
            rate_trans = cur.fetchall()
            return render_template('In-Outcome/outcome.html', rate_trans=rate_trans)

@app.route('/save_outcome', methods=['POST'])
def save_outcome():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = """INSERT INTO public.tb_outcome (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
                     VALUES(%s,%s,%s,%s, LOCALTIMESTAMP(0))
                  """
            item_name = request.form['item_name']
            cash_kip = request.form['cash_kip']
            cash_baht = request.form['cash_baht']
            cash_dollar = request.form['cash_dollar']
            bill_date = format(request.form['bill_date'])

            data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            print(data)
            cur.execute(sql, (data))
            gobal.con.commit()
            return redirect(url_for('outcome'))

@app.route('/outcome_delete/<string:id>')
def outcome_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from public.tb_outcome where roworder=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('outcome'))

