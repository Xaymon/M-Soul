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
        return render_template('transfer/index.html', all_rate=all_rate, bank_from=bank_from)


@app.route('/save_lao_thai', methods=['POST'])
def save_lao_thai():
    if not session.get("name"):
        return redirect("/login")
    else:
        sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from cb_trans where trans_flag=4"""
        cur = gobal.con.cursor()
        cur.execute(sql_d)
        bil_no = cur.fetchone()
        print(bil_no)
        if bil_no[0] == None:
            doc_no = 'TL-100001'
        else:
            doc = bil_no[0]
            print(type(doc))
            a = doc+1
            doc_no = "TL-"+str(a)
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
        INSERT INTO cb_trans(doc_date, doc_no, cust_name, tel,account_book, bank_account_name, item_code,item_code_2, amount, trans_flag, calc_flag,service_charge)
	    VALUES ( LOCALTIMESTAMP(0),%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s)"""
        val1 = (doc_no, customername, tel, bankaccountname, bank_account_code,
                'LAO', bank_to, total_pays, 4, 1,service_charge)
        val2 = (doc_no, customername, tel, bankaccountname,
                bank_account_code, bank_to, bank_from, total_pays, 5, -1, service_charge)
        valn = [(val1), (val2)]
        print(valn)
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
                # val1 = ('TL00001', cash_currency_code,
                #         cash_value, rate_con, total_baht, 4, 1)
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
            sql = "delete from tb_transfer where roworder=%s"
            cur.execute(sql, (id,))
            gobal.con.commit()
            flash('ລົບສຳເລັດ')
            return redirect(url_for('hometf'))
