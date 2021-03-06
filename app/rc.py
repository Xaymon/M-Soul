from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *
from datetime import datetime
from flask.helpers import flash


@app.route('/rchome')
def rchome():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT to_char(doc_date,'DD-MM-YYYY'), doc_no, doc_ref, cust_code, item_name, to_char(pay_value,'999G999G999G999D99') FROM payment where trans_flag=139"
            cur.execute(sql)
            payment_list = cur.fetchall()
            return render_template('ap & ar/rchome.html',payment_list=payment_list, user=session.get("roles"))


@app.route('/rclistar')
def rclistar():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """
                SELECT doc_no,to_char(doc_date,'DD-MM-YYYY'),cust_code,b.name_1,item_name,to_char(total_value_2,'999G999G999G999D99')||' '||c.curency_name FROM public.ap_ar_trans a
                left join ar_customer b on b.code=a.cust_code
                left join tb_addcurrency c on c.curency_code=a.currency_code
                where trans_flag='44' and total_value_2>0
                """
            cur.execute(sql)
            list_cob = cur.fetchall()

            return render_template('ap & ar/rclistar.html', list_cob=list_cob, user=session.get("roles"))


@app.route('/showar_detail/<string:id>')
def showar_detail(id):
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """
            SELECT doc_no,doc_date,cust_code,b.name_1,item_name,total_value_2,currency_code,c.curency_name FROM public.ap_ar_trans a
            left join ar_customer b on b.code=a.cust_code
            left join tb_addcurrency c on c.curency_code=a.currency_code
            where doc_no=%s
            """
            cur.execute(sql, (id,))
            showcob = cur.fetchone()
            dateTimeObj = datetime.now()
            doc_date = dateTimeObj.strftime("%Y-%m-%d")
            sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from payment where trans_flag='129'"""
            cur_d = gobal.con.cursor()
            cur_d.execute(sql_d)
            bil_no = cur_d.fetchone()
            doc_no = ''
            if bil_no[0] == None:
                doc_no = 'RC-100001'
            else:
                doc = bil_no[0]
                a = doc+1
                doc_no = "RC-"+str(a)
            doc_no = doc_no


            return render_template('ap & ar/showaobpay.html',doc_date=doc_date,doc_no=doc_no, showcob=showcob, user=session.get("roles"))


@app.route('/saveaob', methods=['POST'])
def saveaob():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql ="""
                    INSERT INTO payment(trans_flag, doc_date, doc_no, doc_ref, cust_code, item_name, currency_code, total_value, balance_amount, calc_flag,pay_value)
                    VALUES (139,%s,%s,%s,%s,%s,%s,%s,%s,1,%s);"""
            doc_no = request.form['doc_no']
            doc_date = request.form['doc_date']
            doc_ref = request.form['doc_ref']
            cust_code = request.form['cust_code']
            item_name = "?????????????????????"
            currency_code = request.form['currency_code']
            amount = request.form['t_amount']
            pay_amount = request.form['_pay']
            balance_amount = request.form['_still']
            val=(doc_date,doc_no,doc_ref,cust_code,item_name,currency_code,amount,balance_amount,pay_amount)
            cur.execute(sql,val)
            sql_cb="""INSERT INTO cb_trans_detail(doc_date, doc_no, trans_number, amount_1, exchange_rate, amount_2,calc_flag)
                            VALUES (%s, %s, %s, %s, %s,%s,%s);"""
            valss=(doc_date,doc_no,currency_code,pay_amount,1,pay_amount,1)
            curs = gobal.con.cursor()
            curs.execute(sql_cb,valss)
            sql_up="update ap_ar_trans set total_value_2=%s where doc_no=%s"
            valup=(balance_amount,doc_ref)
            curs = gobal.con.cursor()
            curs.execute(sql_up,valup)
            gobal.con.commit()
            return redirect(url_for('rclistar'))
