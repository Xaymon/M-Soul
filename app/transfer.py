from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from werkzeug import datastructures
from flask.helpers import flash
from kk_con import *
from app import app


@app.route('/hometf')
def hometf():
    sql = "SELECT to_char(created_on,'DD-MM-YYY HH24:MI:SS'),transfer_type,bank_from, bank_to, account_name, account_code, amount, service_charge, system_charge, total_amount,roworder FROM tb_transfer"
    cur = gobal.con.cursor()
    cur.execute(sql)
    all_rate = cur.fetchall()
    # print("keo")
    return render_template('transfer/index.html', all_rate=all_rate)


@app.route('/save_rate', methods=['POST'])
def save_rate():

    sql = """INSERT INTO tb_transfer(transfer_type, bank_from, bank_to, account_name, account_code, amount, service_charge, 
             system_charge, total_amount, created_on)
             VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, LOCALTIMESTAMP(0));
            """
    trans_type = request.form['trans_type']
    bank_from = request.form['bank_from']
    bank_to = request.form['bank_to']
    account_name = request.form['account_name']
    account_code = request.form['account_code']
    amount = request.form['amount']
    service_charge = request.form['service_charge']
    system_charge = request.form['system_charge']
    total_amount = int(amount)+int(service_charge)+int(system_charge)
    data = (trans_type, bank_from, bank_to, account_name, account_code,
            amount, service_charge, system_charge, total_amount)
    cur = gobal.con.cursor()
    cur.execute(sql, (data))
    gobal.con.commit()
    flash('ບັນທຶກສຳເລັດ')
    return redirect(url_for('hometf'))


@app.route('/transfer_delete/<string:id>')
def transfer_delete(id):
    with gobal.con:
        cur = gobal.con.cursor()
        sql = "delete from tb_transfer where roworder=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        flash('ລົບສຳເລັດ')
        return redirect(url_for('hometf'))
