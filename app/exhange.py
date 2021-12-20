from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from flask.helpers import flash
from werkzeug import datastructures
from kk_con import *
from app import app


@app.route('/homeex')
def homeex():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """
                    select to_char(doc_date, 'DD-MM-YYY HH24:MI:SS'),doc_no,cust_name,tel,(select curency_name from tb_addcurrency where curency_code=a.item_code) as item_code,to_char(amount,'999G999G999G999D99'),exchange_rate,
                    (select curency_name from tb_addcurrency where curency_code=a.item_code_2) as item_code_2 ,to_char(amount_2,'999G999G999G999D99') from cb_trans a where trans_type='2'
                     """
            cur.execute(sql)
            rate_trans = cur.fetchall()
            currate = gobal.con.cursor()
            sql = "SELECT curency_code, curency_name, buy, sale FROM public.exchange_rate where date_end isnull order by curency_code "
            currate.execute(sql)
            rate_ = currate.fetchall()
            return render_template('exchange/index.html', rate_trans=rate_trans, rate_=rate_,user=session.get("roles"))


@app.route("/product/<id>/<v>")
def product(id, v):
    sql = """SELECT exchange_rate,ex_1,ex_2,date_end FROM (
            select sale::text as exchange_rate,'01' as ex_1,'00' as ex_2,date_end  from public.exchange_rate where curency_code='01'
            union all
            select buy::text as exchange_rate,'00' as ex_1,'01' as ex_2,date_end from public.exchange_rate where curency_code='01'
            union all
            select sale::text as exchange_rate,'01' as ex_1,'02' as ex_2,date_end from public.exchange_rate where curency_code='02'
            union all
            select buy::text as exchange_rate,'02' as ex_1,'01' as ex_2,date_end from public.exchange_rate where curency_code='02'
            union all
            select sale::text as exchange_rate,'00' as ex_1,'02' as ex_2,date_end from public.exchange_rate where curency_code='03'
            union all
            select buy::text as exchange_rate,'02' as ex_1,'00' as ex_2,date_end from public.exchange_rate where curency_code='03') as a
            where date_end isnull and ex_1=%s and ex_2=%s"""
    cur = gobal.con.cursor()
    cur.execute(sql, (id, v))
    product = cur.fetchone()
    return jsonify({'product': product})


@app.route('/ex_delete/<string:id>')
def ex_delete(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "delete from cb_trans where doc_no=%s"
            cur.execute(sql, (id,))
            gobal.con.commit()
            sql = "delete from cb_trans_detail where doc_no=%s"
            cur.execute(sql, (id,))
            gobal.con.commit()
            flash('ລົບສຳເລັດ')
            return redirect(url_for('homeex'))


@app.route('/sale')
def sale():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT bank_id, bank_name  FROM public.tb_bank where bank_loca='lao' order by roworder "
            cur.execute(sql)
            bank_from = cur.fetchall()
            return render_template('exchange/sale.html', bank_from=bank_from)


@app.route('/xchange_trans', methods=['POST'])
def xchange_trans():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            customername = request.form['customername']
            tel = request.form['tel']
            main_cur = request.form['main_cur']
            rate = request.form['rate']
            cash_recipt = float(request.form['cash_recipt'])
            trans_in = request.form['trans_in']
            bank_amount = request.form['bank_amount']
            total_amount1 = request.form['total_amount1']
            second_cur = request.form['second_cur']
            cash_pay = float(request.form['cash_pay'])
            bank_pay = request.form['bank_pay']
            bank_account_code = request.form['bank_account_code']
            bank_account_name = request.form['bank_account_name']
            bank_pay_amount = request.form['bank_pay_amount']
            fee = request.form['fee']
            total_amount2 = request.form['total_amount2']
            sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from cb_trans where trans_type=2"""
            cur = gobal.con.cursor()
            cur.execute(sql_d)
            bil_no = cur.fetchone()
            if bil_no[0] == None:
                doc_no = 'EX-100001'
            else:
                doc = bil_no[0]
                a = doc+1
                doc_no = "EX-"+str(a)

            curh = gobal.con.cursor()
            sql = """
            INSERT INTO cb_trans(doc_date, doc_no, cust_name, tel, item_code,item_code_2,amount,amount_2,exchange_rate, trans_type )
            VALUES (LOCALTIMESTAMP(0), %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            val1 = (doc_no, customername, tel, main_cur, second_cur,
                    total_amount1, total_amount2, rate, 2)
            curh.execute(sql, val1)
            gobal.con.commit()
            print(type(cash_recipt))
            if curh.rowcount > 0:
                sql_dt = """INSERT INTO cb_trans_detail(doc_date, doc_no, trans_number, amount_1, exchange_rate, amount_2,calc_flag, account_code, account_name,fee,trans_type)
                            VALUES (LOCALTIMESTAMP(0), %s, %s, %s, %s,%s,%s, %s, %s, %s,2);
                """
                if cash_recipt != 0 and trans_in != '' and cash_pay != 0 and bank_pay != '':
                    val1 = (doc_no, main_cur, cash_recipt,
                            1, cash_recipt, 1, '', '', 0)
                    val2 = (doc_no, trans_in, bank_amount,
                            1, bank_amount, 1, '', '', 0)
                    val3 = (doc_no, second_cur, cash_pay,
                            '1', cash_pay, -1, '', '', 0)
                    val4 = (doc_no, bank_pay, bank_pay_amount, '1',
                            bank_pay_amount, -1, bank_account_code, bank_account_name, fee)
                    valct = [(val1), (val2), (val3), (val4)]
                    cur.executemany(sql_dt, valct)
                    gobal.con.commit()
                    flash('all')
                    return redirect(url_for('homeex'))
                elif cash_recipt == 0 and trans_in != '' and cash_pay != 0 and bank_pay != '':
                    # print('trans in pay all')
                    # val1 = (doc_no, main_cur,cash_recipt, 1, cash_recipt,1, '', '', 0)
                    val2 = (doc_no, trans_in, bank_amount,
                            1, bank_amount, 1, '', '', 0)
                    val3 = (doc_no, second_cur, cash_pay,
                            '1', cash_pay, -1, '', '', 0)
                    val4 = (doc_no, bank_pay, bank_pay_amount, '1',
                            bank_pay_amount, -1, bank_account_code, bank_account_name, fee)
                    valct = [(val2), (val3), (val4)]
                    cur.executemany(sql_dt, valct)
                    gobal.con.commit()
                    flash('trans in pay all')
                    # return redirect(url_for('homeex'))
                elif cash_recipt != 0 and trans_in == '' and cash_pay != 0 and bank_pay != '':
                    # print('cash in pay all')

                    val1 = (doc_no, main_cur, cash_recipt,
                            1, cash_recipt, 1, '', '', 0)
                    # val2 = (doc_no,trans_in ,bank_amount, 1, bank_amount,1,'', '', 0)
                    val3 = (doc_no, second_cur, cash_pay,
                            '1', cash_pay, -1, '', '', 0)
                    val4 = (doc_no, bank_pay, bank_pay_amount, '1',
                            bank_pay_amount, -1, bank_account_code, bank_account_name, fee)
                    valct = [(val1), (val3), (val4)]
                    cur.executemany(sql_dt, valct)
                    gobal.con.commit()
                    flash('cash in pay all')
                    # return redirect(url_for('homeex'))
                elif cash_recipt != 0 and trans_in != '' and cash_pay == 0 and bank_pay != '':
                    val1 = (doc_no, main_cur, cash_recipt,
                            1, cash_recipt, 1, '', '', 0)
                    val2 = (doc_no, trans_in, bank_amount,
                            1, bank_amount, 1, '', '', 0)
                    # val3 = (doc_no, second_cur, cash_pay,'1', cash_pay,-1, '', '', 0)
                    val4 = (doc_no, bank_pay, bank_pay_amount, '1',
                            bank_pay_amount, -1, bank_account_code, bank_account_name, fee)
                    valct = [(val1), (val2), (val4)]
                    cur.executemany(sql_dt, valct)
                    gobal.con.commit()
                    flash('in all pay trans')
                    # return redirect(url_for('homeex'))
                elif cash_recipt != 0 and trans_in != '' and cash_pay != 0 and bank_pay == '':
                    val1 = (doc_no, main_cur, cash_recipt,
                            1, cash_recipt, 1, '', '', 0)
                    val2 = (doc_no, trans_in, bank_amount,
                            1, bank_amount, 1, '', '', 0)
                    val3 = (doc_no, second_cur, cash_pay,
                            '1', cash_pay, -1, '', '', 0)
                    # val4 = (doc_no, bank_pay, bank_pay_amount,'1', bank_pay_amount, -1, bank_account_code, bank_account_name,fee)
                    valct = [(val1), (val2), (val3)]
                    cur.executemany(sql_dt, valct)
                    gobal.con.commit()
                    flash('in all pay cash')
                elif cash_recipt != 0 and trans_in == '' and cash_pay != 0 and bank_pay == '':
                    val1 = (doc_no, main_cur, cash_recipt,
                            1, cash_recipt, 1, '', '', 0)
                    # val2 = (doc_no, trans_in, bank_amount,
                    # 1, bank_amount, 1, '', '', 0)
                    val3 = (doc_no, second_cur, cash_pay,
                            '1', cash_pay, -1, '', '', 0)
                    # val4 = (doc_no, bank_pay, bank_pay_amount,'1', bank_pay_amount, -1, bank_account_code, bank_account_name,fee)
                    valct = [(val1), (val3)]
                    cur.executemany(sql_dt, valct)
                    gobal.con.commit()
                    flash('in cash pay cash')
                else:
                    # val1 = (doc_no, main_cur, cash_recipt,1, cash_recipt, 1, '', '', 0)
                    val2 = (doc_no, trans_in, bank_amount,
                            1, bank_amount, 1, '', '', 0)
                    # val3 = (doc_no, second_cur, cash_pay,'1', cash_pay, -1, '', '', 0)
                    val4 = (doc_no, bank_pay, bank_pay_amount, '1',
                            bank_pay_amount, -1, bank_account_code, bank_account_name, fee)
                    valct = [(val2), (val4)]
                    cur.executemany(sql_dt, valct)
                    gobal.con.commit()
                    flash('in trans pay trans')
                    # print('all in pay cash')
                    # return redirect(url_for('hometf'))
        return redirect(url_for('homeex'))


@app.route('/showex_detail/<string:id>')
def showex_detail(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:

            return render_template('exchange/showdetail.html')
