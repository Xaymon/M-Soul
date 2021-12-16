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


@app.route('/setap')
def setap():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT code, name_1, tel, province, city, address, remark FROM public.ap_supplier "
            cur.execute(sql)
            rate_trans = cur.fetchall()
            return render_template('ap & ar/set_ap.html', rate_trans = rate_trans)

@app.route('/setapcopy')
def setapcopy():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT code, name_1, tel FROM public.ap_supplier "
            cur.execute(sql)
            rate_trans = cur.fetchall()
            return render_template('ap & ar/set_ap copy.html', rate_trans = rate_trans)

@app.route('/saveset_ap', methods=['POST'])
def saveset_ap():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """INSERT INTO public.set_ap (item_name, amount, currency_name, total)
                     VALUES(%s,%s,%s,%s);
                  """
            # codee = request.form['codee']
            item_name = request.form['item_name']
            amount = request.form['amount']
            currency_name = request.form['currency_name']
            total = request.form['total']
            data = (item_name, amount, currency_name, total)
            cur.execute(sql, data)
            gobal.con.commit()

            return redirect(url_for('setapcopy'))

@app.route('/send_ap', methods=['POST'])
def send_ap():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            codee = request.form['codee']
            name_1 = request.form['name_1']
            tel = request.form['tel']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.ap_supplier set code=%s, name_1=%s, tel=%s where code=%s',
                        (codee, name_1, tel))
            gobal.con.commit()
            return redirect(url_for('setapcopy'))

@app.route('/send_apid/<string:id>',methods=['GET'])
def send_apid(id):
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = "SELECT code, name_1, tel FROM public.ap_supplier where code=%s"
            cur = gobal.con.cursor()
            cur.execute(sql,(id,))
            selectapid = cur.fetchone()
            sql_b = "SELECT code, name_1, tel from public.ap_supplier"
            curs = gobal.con.cursor()
            curs.execute(sql_b)
        return render_template('ap & ar/set_ap copy.html',selectapid=selectapid)


