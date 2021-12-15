from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from werkzeug import datastructures
from flask.helpers import flash
from kk_con import *
from app import app
from datetime import datetime, date


class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self):
        print(self.firstname, self.lastname)


@app.route('/hometf')
def hometf():
    if not session.get("name"):
        return redirect("/login")
    else:
        sql = "SELECT doc_date,doc_no,cust_name,tel,item_code,item_code_2,bank_account_name,account_book,to_char(amount,'999G999G999G999D99') FROM public.cb_trans where trans_flag='4' order by doc_date"
        cur = gobal.con.cursor()
        cur.execute(sql)
        all_rate = cur.fetchall()

        cur = gobal.con.cursor()
        sql = "SELECT bank_id, bank_name  FROM public.tb_bank order by roworder "
        cur.execute(sql)
        bank_from = cur.fetchall()
        currate = gobal.con.cursor()
        sql = "SELECT curency_code, curency_name, buy, sale FROM public.exchange_rate where date_end isnull order by curency_code "
        currate.execute(sql)
        rate_ = currate.fetchall()
        return render_template('transfer/index.html', all_rate=all_rate, bank_from=bank_from, rate_=rate_)


@app.route('/save_lao_thai', methods=['POST'])
def save_lao_thai():
    if not session.get("name"):
        return redirect("/login")
    else:
        sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from cb_trans where trans_flag=4 and calc_flag=1"""
        cur = gobal.con.cursor()
        cur.execute(sql_d)
        bil_no = cur.fetchone()
        print(bil_no)
        if bil_no[0] == None:
            doc_no = 'LT-100001'
        else:
            doc = bil_no[0]
            print(type(doc))
            a = doc+1
            doc_no = "LT-"+str(a)
        print(doc_no)
        # ຂໍ້ມູນລູຄ້າ
        customername = request.form['customername']
        tel = request.form['tel']
        # ປາຍທາງ
        bank_to = request.form['bank_to']
        bankaccountname = request.form['bankaccountname']
        bank_account_code = request.form['bank_account_code']
        total_pays = request.form['total_pays']
        # cash amount
        cash_currency_code = request.form['cash_currency_code']
        cash_value = request.form['cash_value']
        rate_con = request.form['rate_con']
        total_baht = request.form['total_baht']
        # trans amount
        bank_from = request.form['bank_from']
        bank_amount = request.form['bank_amount']
        rate_bank = request.form['rate_bank']
        total_bank_amount = request.form['total_bank_amount']
        # service and fee
        service_charge = request.form['service_charge']
        # total_amount
        total_amount = request.form['total_amount']

        cur = gobal.con.cursor()
        sql = """
        INSERT INTO cb_trans(doc_date, doc_no, cust_name, tel,account_book, bank_account_name, item_code,item_code_2, amount, trans_flag, calc_flag,service_charge,trans_type)
	    VALUES ( LOCALTIMESTAMP(0),%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,0)"""
        val1 = (doc_no, customername, tel, bankaccountname, bank_account_code,
                'LAO', bank_to, total_pays, 4, 1, service_charge)
        val2 = (doc_no, customername, tel, bankaccountname,
                bank_account_code, bank_to, bank_from, total_pays, 5, -1, service_charge)
        valn = [(val1), (val2)]
        cur.executemany(sql, valn)
        gobal.con.commit()
        if cur.rowcount > 0:
            sqldetail = """
            INSERT INTO public.cb_trans_detail(
            doc_date, doc_no, trans_number, amount_1, exchange_rate, amount_2, trans_flag, calc_flag)
            VALUES (LOCALTIMESTAMP(0), %s, %s, %s, %s, %s, %s, %s);
            """
            if cash_currency_code != '' and bank_from != '':
                val1 = (doc_no, cash_currency_code,
                        cash_value, rate_con, total_baht, 4, 1)
                val2 = (doc_no, bank_from,
                        bank_amount, rate_bank, total_bank_amount, 4, 1)
                val3 = (doc_no, bank_to, total_pays,
                        '1', total_pays, 5, -1)
                valct = [(val1), (val2), (val3)]
                cur.executemany(sqldetail, valct)
                gobal.con.commit()
                flash('ບັນທຶກສຳເລັດ')
                return redirect(url_for('hometf'))
            elif cash_currency_code == '' and bank_from != '':
                val2 = (doc_no, bank_from,
                        bank_amount, rate_bank, total_bank_amount, 4, 1)
                val3 = (doc_no, bank_to, total_pays,
                        '1', total_pays, 5, -1)
                valct = [(val2), (val3)]
                cur.executemany(sqldetail, valct)
                gobal.con.commit()
                flash('ບັນທຶກສຳເລັດ')
                return redirect(url_for('hometf'))
            else:
                val1 = (doc_no, cash_currency_code,
                        cash_value, rate_con, total_baht, 4, 1)
                val3 = (doc_no, bank_to, total_pays,
                        '1', total_pays, 5, -1)
                valct = [(val1), (val3)]
                cur.executemany(sqldetail, valct)
                gobal.con.commit()
                flash('ບັນທຶກສຳເລັດ')
        return redirect(url_for('hometf'))


@app.route('/transfer_delete/<string:id>')
def transfer_delete(id):
    with gobal.con:
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
            return redirect(url_for('hometf'))


@app.route('/save_thai_lao', methods=['POST'])
def save_thai_lao():
    if not session.get("name"):
        return redirect("/login")
    else:
        sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from cb_trans where trans_flag=4 and calc_flag=1 and trans_type=1"""
        cur = gobal.con.cursor()
        cur.execute(sql_d)
        bil_no = cur.fetchone()
        print(bil_no)
        if bil_no[0] == None:
            doc_no = 'TL-100001'
        else:
            doc = bil_no[0]
            a = doc+1
            doc_no = "TL-"+str(a)
        customername = request.form['customername_tl']
        tel = request.form['tel_tl']

        from_bank_tl = request.form['from_bank_tl']
        trans_incom = request.form['trans_incom']

        service_charge_tl = request.form['service_charge_tl']
        total_befor_pay_tl = request.form['total_befor_pay_tl']

        currency_code_tl = request.form['currency_code_tl']
        total_baht_tl = request.form['total_baht_tl']
        rate_c_tl = request.form['rate_c_tl']
        cash_value_tl = request.form['cash_value_tl']

        from_bank_pay = request.form['from_bank_pay']
        bank_account_code = request.form['bank_account_code']
        bank_account_name = request.form['bank_account_name']
        total_bank_amount_tl = request.form['total_bank_amount_tl']
        fee_tl = request.form['fee_tl']

        rate_bank_tl = request.form['rate_bank_tl']
        bank_amount_tl = request.form['bank_amount_tl']
        total_amount_tt_tl = request.form['total_amount_tt_tl']
        cur = gobal.con.cursor()
        sql = """
        INSERT INTO cb_trans(doc_date, doc_no, cust_name, tel, item_code,item_code_2, amount, trans_flag, calc_flag,service_charge,trans_type)
	    VALUES ( LOCALTIMESTAMP(0),%s, %s, %s, %s,%s,%s,%s,%s,%s,1)"""
        val1 = (doc_no, customername, tel, 'Thai', '',
                trans_incom, 4, 1, service_charge_tl)
        val2 = (doc_no, customername, tel, 'Lao', '',
                trans_incom, 5, -1, service_charge_tl)
        valn = [(val1), (val2)]
        cur.executemany(sql, valn)
        gobal.con.commit()
        if cur.rowcount > 0:
            sqldetail = """
            INSERT INTO public.cb_trans_detail(
            doc_date, doc_no, trans_number, amount_1, exchange_rate, amount_2, trans_flag, calc_flag,account_code, account_name, fee)
            VALUES (LOCALTIMESTAMP(0), %s, %s, %s, %s, %s, %s, %s,%s, %s, %s);
            """
            if currency_code_tl != '' and from_bank_pay != '':
                val1 = (doc_no, currency_code_tl, cash_value_tl,
                        rate_c_tl, total_baht_tl, 5, -1, '', '', 0,)
                val2 = (doc_no, from_bank_pay, bank_amount_tl, rate_bank_tl,
                        total_bank_amount_tl, 5, -1, bank_account_code, bank_account_name, fee_tl,)
                val3 = (doc_no, from_bank_tl, trans_incom,
                        '1', trans_incom, 4, 1, '', '', 0)
                valct = [(val1), (val2), (val3)]
                cur.executemany(sqldetail, valct)
                gobal.con.commit()
                flash('ບັນທຶກສຳເລັດ')
                return redirect(url_for('hometf'))
            elif currency_code_tl == '' and from_bank_pay != '':
                # val1 = (doc_no, currency_code_tl,
                #         cash_value_tl, rate_c_tl, total_baht_tl, 5, -1)
                val2 = (doc_no, from_bank_pay, bank_amount_tl, rate_bank_tl,
                        total_bank_amount_tl, 5, -1, bank_account_code, bank_account_name, fee_tl,)
                val3 = (doc_no, from_bank_tl, trans_incom,
                        '1', trans_incom, 4, 1, '', '', 0,)
                valct = [(val2), (val3)]
                cur.executemany(sqldetail, valct)
                gobal.con.commit()
                flash('ບັນທຶກສຳເລັດ')
                return redirect(url_for('hometf'))
            else:
                val1 = (doc_no, currency_code_tl, cash_value_tl,
                        rate_c_tl, total_baht_tl, 5, -1, '', '', 0,)
                # val2 = (doc_no, from_bank_pay,
                #         bank_amount_tl, rate_bank_tl, total_bank_amount_tl, 5, -1)
                val3 = (doc_no, from_bank_tl, trans_incom,
                        '1', trans_incom, 4, 1, '', '', 0,)
                valct = [(val1), (val3)]
                cur.executemany(sqldetail, valct)
                gobal.con.commit()
                flash('ບັນທຶກສຳເລັດ')
        return redirect(url_for('hometf'))
