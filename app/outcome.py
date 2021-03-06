from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *
from datetime import datetime
from flask.helpers import flash


@app.route('/outcome')
def outcome():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """
                   SELECT to_char(doc_date,'DD-MM-YYYY') , doc_no, cust_name, tel, item_name, to_char(amount,'999G999G999G999D99')||'-'||(select curency_name from tb_addcurrency where curency_code=a.item_code) FROM cb_trans a where trans_type=6;
                  """
            cur.execute(sql)
            rate_trans = cur.fetchall()
            dateTimeObj = datetime.now()
            doc_date = dateTimeObj.strftime("%Y-%m-%d")
            return render_template('In-Outcome/outcome.html', rate_trans=rate_trans, doc_date=doc_date,user=session.get("roles"))


@app.route('/save_outcome', methods=['POST'])
def save_outcome():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from cb_trans where trans_type=6"""
            cur = gobal.con.cursor()
            cur.execute(sql_d)
            bil_no = cur.fetchone()
            print(bil_no)
            if bil_no[0] == None:
                doc_no = 'EP-100001'
            else:
                doc = bil_no[0]
                a = doc+1
                doc_no = "EP-"+str(a)

            sql = """INSERT INTO cb_trans (doc_date, doc_no, cust_name, tel, item_code, item_name, amount, trans_type)
                     VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                  """
            cusname = request.form['cusname']
            custel = request.form['custel']
            item_name = request.form['item_name']
            cur_code = request.form['cur_code']
            amount = request.form['amount']
            bill_date = request.form['bill_date']
            data = (bill_date, doc_no, cusname, custel,
                    cur_code, item_name, amount, 6)
            curh = gobal.con.cursor()
            curh.execute(sql, data,)
            gobal.con.commit()
            if cur.rowcount > 0:
                sql_dt = """INSERT INTO cb_trans_detail(doc_date, doc_no, trans_number, amount_1, exchange_rate, amount_2,trans_type,calc_flag)
                            VALUES (%s, %s, %s, %s,%s,%s,%s,%s);
                """
                val1 = (bill_date, doc_no, cur_code, amount, 1, amount, 6,-1)
                curdt = gobal.con.cursor()
                curdt.execute(sql_dt, val1,)
                gobal.con.commit()
                flash('????????????????????????????????????')
            return redirect(url_for('outcome'))

@app.route('/outcome_delete/<string:id>')
def outcome_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from cb_trans where doc_no=%s"
        cur.execute(sql, (id,))
        curs = gobal.con.cursor()
        sql = "delete from cb_trans_detail where doc_no=%s"
        curs.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('outcome'))


@app.route('/update_outcome/<string:id>', methods=['POST'])
def update_outcome(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            item_name = request.form['item_name']
            cash_kip = request.form['cash_kip']
            cash_baht = request.form['cash_baht']
            cash_dollar = request.form['cash_dollar']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.tb_outcome set item_name=%s, cash_kip=%s, cash_baht=%s, cash_dollar=%s where roworder=%s',
                        (item_name, cash_kip, cash_baht, cash_dollar, (id,)))
            gobal.con.commit()
            return redirect(url_for('outcome'))
