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
                    SELECT roworder,to_char(ex_date,'DD-MM-YYYY HH24:MI:SS'), to_char(amount_1,'999G999G999G999D99')||'-'|| case when ex_1='K' then 'ກີບ' when ex_1='B' then 'ບາດ' else 'ໂດລາ' end, exchange_rate, 
                    to_char(amount_2,'999G999G999G999D99')||'-'|| case when ex_2='K' then 'ກີບ' when ex_2='B' then 'ບາດ' else 'ໂດລາ' end,customer FROM public.ic_trans order by roworder DESC"""
            cur.execute(sql)
            rate_trans = cur.fetchall()
            return render_template('exchange/index.html', rate_trans=rate_trans)


@app.route("/product/<id>/<v>")
def product(id, v):
    sql = """SELECT exchange_rate,ex_1,ex_2,date_end FROM (
            select sale::text as exchange_rate,'01' as ex_1,'00' as ex_2,date_end  from public.exchange_rate where curency_code='01'
            union all
            select buy::text as exchange_rate,'00' as ex_1,'01' as ex_2,date_end from public.exchange_rate where curency_code='01'
            union all
            select sale::text as exchange_rate,'01' as ex_1,'03' as ex_2,date_end from public.exchange_rate where curency_code='02'
            union all
            select buy::text as exchange_rate,'03' as ex_1,'01' as ex_2,date_end from public.exchange_rate where curency_code='02'
            union all
            select sale::text as exchange_rate,'00' as ex_1,'03' as ex_2,date_end from public.exchange_rate where curency_code='03'
            union all
            select buy::text as exchange_rate,'03' as ex_1,'00' as ex_2,date_end from public.exchange_rate where curency_code='03') as a
            where date_end isnull and ex_1=%s and ex_2=%s"""
    cur = gobal.con.cursor()
    cur.execute(sql, (id, v))
    product = cur.fetchone()
    return jsonify({'product': product})


@app.route('/save_ex', methods=['POST'])
def save_ex():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = """INSERT INTO public.ic_trans(
                        ex_date, ex_1, ex_2, amount_1, exchange_rate, amount_2, tran_type,customer)
                        values(LOCALTIMESTAMP(0), %s, %s, %s, %s, %s,%s,%s)
                """
            customer_ = request.form['customer_']
            ex_1 = request.form['ex_1']
            ex_2 = request.form['ex_2']
            amount_1 = request.form['vale_tt']
            exchange_rate = request.form['rate_show']
            amount_2 = request.form['tt_amount']
            tran_type = request.form['rate_code']
            data = (ex_1, ex_2, amount_1, exchange_rate,
                    amount_2, tran_type, customer_)
            if amount_1 != 0:
                cur.execute(sql, (data))
                gobal.con.commit()
                flash('ບັນທຶກສຳເລັດ')
                return redirect(url_for('homeex'))
            else:
                return redirect(url_for('homeex'))


@app.route('/ex_delete/<string:id>')
def ex_delete(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = """delete from ic_trans where roworder=%s"""
            cur.execute(sql, (id,))
            gobal.con.commit()
            flash('ລົບສຳເລັດ ແລ້ວ')
            return redirect(url_for('homeex'))


@app.route('/sale')
def sale():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT bank_id, bank_name  FROM public.tb_bank order by roworder "
            cur.execute(sql)
            bank_from = cur.fetchall()
            return render_template('exchange/sale.html',bank_from=bank_from)


@app.route('/xchange_trans', methods=['POST'])
def xchange_trans():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            main_cur = request.form['main_cur']
            rate = request.form['rate']
            cash_recipt = request.form['cash_recipt']
            trans_in = request.form['trans_in']
            bank_amount = request.form['bank_amount']
            total_amount1 = request.form['total_amount1']
            second_cur = request.form['second_cur']
            cash_pay = request.form['cash_pay']
            bank_pay = request.form['bank_pay']
            bank_account_code = request.form['bank_account_code']
            bank_account_name = request.form['bank_account_name']
            bank_pay_amount = request.form['bank_pay_amount']
            fee = request.form['fee']
            total_amount2 = request.form['total_amount2']
            # bank_pay_amount = request.form['bank_pay_amount']

            return redirect(url_for('homeex'))
