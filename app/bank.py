from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *
from flask.helpers import flash


@app.route('/dm')
def dm():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT bank_id, bank_name  FROM public.tb_bank order by roworder "
            cur.execute(sql)
            bank_from = cur.fetchall()
            # list Transfer
            curlist = gobal.con.cursor()
            sqlist = "select to_char(doc_date, 'DD-MM-YYY HH24:MI:SS'),doc_no,(select curency_name from tb_addcurrency where curency_code=a.item_code) as item_code,item_code_2,to_char(amount,'999G999G999G999D99') from cb_trans a where trans_type='11'"
            curlist.execute(sqlist)
            dm = curlist.fetchall()
            return render_template('bank/dm.html', bank_from=bank_from, dm=dm)


@app.route('/dm_save', methods=['POST'])
def dm_save():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from cb_trans where trans_type=11"""
            cur = gobal.con.cursor()
            cur.execute(sql_d)
            bil_no = cur.fetchone()
            print(bil_no)
            if bil_no[0] == None:
                doc_no = 'DM-100001'
            else:
                doc = bil_no[0]
                a = doc+1
                doc_no = "DM-"+str(a)

            sql = """INSERT INTO cb_trans (doc_date, doc_no, item_code, item_code_2, amount, trans_type)
                     VALUES(LOCALTIMESTAMP(0),%s,%s,%s,%s,11)
                  """
            cur_code = request.form['cur_code']
            amount = request.form['amount']
            bank_in = request.form['bank_in']
            amount_2 = request.form['amount_2']
            data = (doc_no, cur_code, bank_in, amount_2)
            curh = gobal.con.cursor()
            curh.execute(sql, data,)
            gobal.con.commit()
            if cur.rowcount > 0:
                sql_dt = """INSERT INTO cb_trans_detail(doc_date, doc_no, trans_number, amount_1, exchange_rate, amount_2,trans_type,calc_flag)
                            VALUES (LOCALTIMESTAMP(0), %s, %s, %s,%s,%s,%s,%s);
                """
                val1 = (doc_no, cur_code, amount, 1, amount, 11, -1)
                val2 = (doc_no, bank_in, amount, 1, amount, 11, 1)
                vlan = [(val1), (val2)]
                curdt = gobal.con.cursor()
                curdt.executemany(sql_dt, vlan)
                gobal.con.commit()
            flash('ບັນທຶກສຳເລັດ')
            return redirect(url_for('dm'))
@app.route('/dm_delete/<string:id>')
def dm_delete(id):
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
        return redirect(url_for('dm'))

@app.route('/wm')
def wm():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT bank_id, bank_name  FROM public.tb_bank order by roworder "
            cur.execute(sql)
            bank_from = cur.fetchall()
            # list Transfer
            curlist = gobal.con.cursor()
            sqlist = "select to_char(doc_date, 'DD-MM-YYY HH24:MI:SS'),doc_no,item_code, (select curency_name from tb_addcurrency where curency_code=a.item_code_2) as item_code_2,to_char(amount,'999G999G999G999D99') from cb_trans a where trans_type='12'"
            curlist.execute(sqlist)
            wm = curlist.fetchall()
            return render_template('bank/wm.html', bank_from=bank_from, list=wm)


@app.route('/wm_save', methods=['POST'])
def wm_save():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from cb_trans where trans_type=12"""
            cur = gobal.con.cursor()
            cur.execute(sql_d)
            bil_no = cur.fetchone()
            print(bil_no)
            if bil_no[0] == None:
                doc_no = 'WM-100001'
            else:
                doc = bil_no[0]
                a = doc+1
                doc_no = "WM-"+str(a)

            sql = """INSERT INTO cb_trans (doc_date, doc_no, item_code, item_code_2, amount, trans_type)
                     VALUES(LOCALTIMESTAMP(0),%s,%s,%s,%s,12)
                  """
            cur_code = request.form['cur_code']
            amount = request.form['amount']
            bank_out = request.form['bank_out']
            amount_2 = request.form['amount_2']
            data = (doc_no,bank_out,cur_code, amount_2)
            curh = gobal.con.cursor()
            curh.execute(sql, data,)
            gobal.con.commit()
            if cur.rowcount > 0:
                sql_dt = """INSERT INTO cb_trans_detail(doc_date, doc_no, trans_number, amount_1, exchange_rate, amount_2,trans_type,calc_flag)
                            VALUES (LOCALTIMESTAMP(0), %s, %s, %s,%s,%s,%s,%s);
                """
                val1 = (doc_no, bank_out, amount, 1, amount, 12, -1)
                val2 = (doc_no, cur_code, amount, 1, amount, 12, 1)
                vlan = [(val1), (val2)]
                curdt = gobal.con.cursor()
                curdt.executemany(sql_dt, vlan)
                gobal.con.commit()
            flash('ບັນທຶກສຳເລັດ')
            return redirect(url_for('wm'))

# 
@app.route('/wm_delete/<string:id>')
def wm_delete(id):
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
        return redirect(url_for('wm'))

@app.route('/tm')
def tm():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT curency_code,curency_name || '-' ||  curency_name2 , roworder FROM public.tb_currencytype order by roworder"""
            cur.execute(sql)
            rate_ = cur.fetchall()

            curs = gobal.con.cursor()
            sql_cur = "SELECT curency_code,curency_name FROM public.tb_addcurrency"
            curs.execute(sql_cur)
            curent = curs.fetchall()
            return render_template('manage/currency_type.html', rate_=rate_, curent=curent)
