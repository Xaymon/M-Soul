from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *

@app.route('/ap')
def ap():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT code, name_1, tel, province, city, address, remark FROM public.ap_supplier "
            cur.execute(sql)
            rate_trans = cur.fetchall()
            return render_template('ap & ar/ap.html', rate_trans = rate_trans)

@app.route('/save_ap', methods=['POST'])
def save_ap():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """INSERT INTO public.ap_supplier (code, name_1, tel, province, city, address, remark)
                     VALUES(%s,%s,%s,%s,%s,%s,%s);
                  """
            # codee = request.form['codee']
            codee = request.form['codee']
            name_1 = request.form['name_1']
            tel = request.form['tel']
            province = request.form['province']
            city = request.form['city']
            address = request.form['address']
            remark = request.form['remark']
            data = (codee, name_1, tel, province,city, address, remark)
            cur.execute(sql, data)
            gobal.con.commit()

            return redirect(url_for('ap'))

@app.route('/update_ap/<string:id>', methods=['POST'])
def update_ap(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            codee = request.form['codee']
            name_1 = request.form['name_1']
            tel = request.form['tel']
            province = request.form['province']
            city = request.form['city']
            address = request.form['address']
            remark = request.form['remark']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.ap_supplier set code=%s, name_1=%s, tel=%s, province=%s, city=%s, address=%s, remark=%s where code=%s',
                        (codee, name_1, tel, province, city, address, remark, (id,)))
            gobal.con.commit()
            return redirect(url_for('ap'))

@app.route('/ap_delete/<string:id>')
def ap_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from public.ap_supplier where code=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('ap'))


@app.route('/ar')
def ar():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT code, name_1, tel, province, city, address, remark FROM public.ar_customer "
            cur.execute(sql)
            rate_tran = cur.fetchall()
            return render_template('ap & ar/ar.html', rate_tran = rate_tran)

@app.route('/save_ar', methods=['POST'])
def save_ar():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """INSERT INTO public.ar_customer (code, name_1, tel, province, city, address, remark)
                     VALUES(%s,%s,%s,%s,%s,%s,%s);
                  """
            # codee = request.form['codee']
            codee = request.form['codee']
            name_1 = request.form['name_1']
            tel = request.form['tel']
            province = request.form['province']
            city = request.form['city']
            address = request.form['address']
            remark = request.form['remark']
            data = (codee, name_1, tel, province,city, address, remark)
            cur.execute(sql, data)
            gobal.con.commit()

            return redirect(url_for('ar'))

@app.route('/update_ar/<string:id>', methods=['POST'])
def update_ar(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            codee = request.form['codee']
            name_1 = request.form['name_1']
            tel = request.form['tel']
            province = request.form['province']
            city = request.form['city']
            address = request.form['address']
            remark = request.form['remark']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.ar_customer set code=%s, name_1=%s, tel=%s, province=%s, city=%s, address=%s, remark=%s where code=%s',
                        (codee, name_1, tel, province, city, address, remark, (id,)))
            gobal.con.commit()
            return redirect(url_for('ar'))

@app.route('/ar_delete/<string:id>')
def ar_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from public.ar_customer where code=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('ar'))

