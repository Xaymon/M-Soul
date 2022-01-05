from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *

# @app.route('/ap')
# def ap():
#     with gobal.con:
#         if not session.get("name"):
#             return redirect("/login")
#         else:
#             cur = gobal.con.cursor()
#             sql = """SELECT code, name_1, tel, b.prov_name, c.city_name, address, remark FROM public.ap_supplier a 
#             left join province b on a.province=b.prov_code 
#             left join city c on b.prov_code =c.prov_code and c.city_code = a.city"""
#             cur.execute(sql)
#             rate_trans = cur.fetchall()

#             curb = gobal.con.cursor()
#             sql_p = "select prov_code, prov_name from province order by prov_code"
#             curb.execute(sql_p)
#             prov_list = curb.fetchall()

#             curc = gobal.con.cursor()
#             sql_c = "select city_code, city_name from city order by city_code"
#             curc.execute(sql_c)
#             city_list = curc.fetchall()
#             return render_template('ap & ar/ap.html', rate_trans = rate_trans, prov_list = prov_list, city_list = city_list)

@app.route('/ap')
def ap():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT code, name_1, tel, b.prov_name, c.city_name, address, remark FROM public.ap_supplier a 
            left join province b on a.province=b.prov_code 
            left join city c on b.prov_code =c.prov_code and c.city_code = a.city"""
            cur.execute(sql)
            rate_trans = cur.fetchall()

            curb = gobal.con.cursor()
            sql_p = "select prov_code, prov_name from province order by prov_code"
            curb.execute(sql_p)
            prov_list = curb.fetchall()
            return render_template('ap & ar/ap.html', rate_trans = rate_trans, prov_list = prov_list,user=session.get("roles"))

@app.route("/predict/<id>")
def predict(id):
    sql_city = "SELECT city_code, city_name FROM city WHERE prov_code=%s"
    curc = gobal.con.cursor()
    curc.execute(sql_city, (id,))
    cityss = curc.fetchall()
    return jsonify({'citylist': cityss})

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
            province = request.form['up_province']
            city = request.form['up_city']
            address = request.form['address']
            remark = request.form['remark']

            print(province, "city = ",city)

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

@app.route('/ap_pay')
def ap_pay():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT public.ap_supplier.code, name_1, tel, item_name, amount, currency_name, total FROM public.ap_supplier LEFT JOIN public.set_ap ON public.set_ap.code = public.ap_supplier.code"""
            cur.execute(sql)
            rate_trans = cur.fetchall()

            return render_template('ap & ar/ap_pay.html', rate_trans = rate_trans,user=session.get("roles"))


# @app.route('/ar')
# def ar():
#     with gobal.con:
#         if not session.get("name"):
#             return redirect("/login")
#         else:
#             cur = gobal.con.cursor()
#             sql = "SELECT code, name_1, tel, province, city, address, remark FROM public.ar_customer "
#             cur.execute(sql)
#             rate_tran = cur.fetchall()
#             return render_template('ap & ar/ar.html', rate_tran = rate_tran)
@app.route('/ar')
def ar():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT code, name_1, tel, b.prov_name, c.city_name, address, remark FROM public.ar_customer a 
            left join province b on a.province=b.prov_code 
            left join city c on b.prov_code =c.prov_code and c.city_code = a.city"""
            cur.execute(sql)
            rate_trans = cur.fetchall()

            curb = gobal.con.cursor()
            sql_p = "select prov_code, prov_name from province order by prov_code"
            curb.execute(sql_p)
            prov_list = curb.fetchall()

            curc = gobal.con.cursor()
            sql_c = "select city_code, city_name from city order by city_code"
            curc.execute(sql_c)
            city_list = curc.fetchall()
            return render_template('ap & ar/ar.html', rate_trans = rate_trans, prov_list = prov_list, city_list = city_list,user=session.get("roles"))

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
            sql = "SELECT public.ap_ar_trans.doc_date, public.ap_ar_trans.doc_no, public.ap_supplier.code, name_1, tel, item_name, total_value FROM public.ap_supplier LEFT JOIN public.ap_ar_trans ON public.ap_ar_trans.cust_code = public.ap_supplier.code"
            cur.execute(sql)
            rate_trans = cur.fetchall()
            return render_template('ap & ar/set_ap.html', rate_trans = rate_trans,user=session.get("roles"))
@app.route('/setapcopy')
def setapcopy():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT code, name_1, tel, province, city, address, remark FROM public.ap_supplier"
            cur.execute(sql)
            rate_trans = cur.fetchall()
            return render_template('ap & ar/set_ap_copy.html', rate_trans = rate_trans,user=session.get("roles"))

@app.route('/send_apid/<string:id>',methods=['GET'])
def send_apid(id):
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            sql_a = "SELECT public.ap_ar_trans.doc_date, public.ap_ar_trans.doc_no, public.ap_supplier.code, name_1, tel, item_name, total_value FROM public.ap_supplier LEFT JOIN public.ap_ar_trans ON public.ap_ar_trans.cust_code = public.ap_supplier.code where public.ap_supplier.code=%s"
            cur = gobal.con.cursor()
            cur.execute(sql_a,(id,))
            selectapid = cur.fetchone()
            # # sql_b = "SELECT z_ap.code, name_1, tel, item_name, amount, currency_name, total FROM z_ap LEFT JOIN z_set_ap ON z_set_ap.code = z_ap.code"
            # # sql_b = "SELECT code, name_1, tel FROM public.z_ap"
            # # curs = gobal.con.cursor()
            # # curs.execute(sql_b))

            # cura= gobal.con.cursor()
            # sql = "SELECT public.ap_supplier.code, name_1, tel, item_name, amount, currency_name, total FROM public.ap_supplier LEFT JOIN public.set_ap ON public.set_ap.code = public.ap_supplier.code"
            # cura.execute(sql)
            # # select = cura.fetchone()
            rate_trans = cur.fetchall()

            curs = gobal.con.cursor()
            sql_cur = "SELECT curency_code,curency_name FROM public.tb_addcurrency"
            curs.execute(sql_cur)
            curent = curs.fetchall()
            

            gobal.con.commit()
            return render_template('ap & ar/set_ap_copy.html',selectapid=selectapid,rate_trans = rate_trans, curent=curent,user=session.get("roles"))

@app.route('/saveset_ap', methods=['POST'])
def saveset_ap():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            # curb = gobal.con.cursor()
            # codee = request.form['codee']
            # curb.execute('update z_ap set code=%s where code=%s',
            #             (codee, (id,)))
            # gobal.con.commit()

            cur = gobal.con.cursor()
            sql = """INSERT INTO public.ap_ar_trans (doc_date, doc_no, item_name, currency_code, total_value, total_value_2, cust_code)
                     VALUES(%s,%s,%s,%s,%s,%s,%s);
                  """
            doc_date = request.form['doc_date']
            doc_no = request.form['doc_no']
            item_name = request.form['item_name']
            currency_code = request.form['currency_code']
            total_value = request.form['total_value']
            total_value_2 = request.form['total_value_2']
            cust_code = request.form['cust_code']
            data = (doc_date, doc_no, item_name, currency_code, total_value, total_value_2, cust_code)
            cur.execute(sql, data)
            # curb = gobal.con.cursor()
            # codee = request.form['codee']
            # curb.execute('insert into z_set_ap (code) values(%s)')
            # gobal.con.commit()
            return redirect(url_for('send_apid', id = cust_code))
            # return render_template('ap & ar/set_ap_copy.html')

@app.route('/update_set_ap/<string:id>', methods=['POST'])
def update_set_ap(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            item_name = request.form['item_name']
            amount = request.form['amount']
            currency_name = request.form['currency_name']
            total = request.form['total']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.set_ap set item_name=%s, amount=%s, currency_name=%s,total=%s where code=%s',
                        (item_name, amount, currency_name, total, (id,)))
            gobal.con.commit()
            return redirect(url_for('send_apid', id = id))
            # return render_template('ap & ar/set_ap_copy.html')

@app.route('/set_ap_delete/<string:id>')
def set_ap_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from public.set_ap where code=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('send_apid', id = id))
        # return render_template('ap & ar/set_ap_copy.html')

@app.route('/setar')
def setar():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            # sql = "SELECT code, name_1, tel, province, city, address, remark FROM public.ar_customer"
            sql = "SELECT public.ar_customer.code, public.ar_customer.code, public.ar_customer.code, name_1, tel, item_name, amount FROM public.ar_customer LEFT JOIN public.set_ar ON public.set_ar.code = public.ar_customer.code"
            cur.execute(sql)
            rate_trans = cur.fetchall()
            return render_template('ap & ar/set_ar.html', rate_trans = rate_trans,user=session.get("roles"))

@app.route('/send_arid/<string:id>',methods=['GET'])
def send_arid(id):
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            # sql_a = "SELECT public.ar_customer.code, name_1, tel FROM public.ar_customer where public.ar_customer.code=%s"
            sql_a = "SELECT public.ap_ar_trans.doc_date, public.ap_ar_trans.doc_no, public.ar_customer.code, name_1, tel, item_name, total_value FROM public.ar_customer LEFT JOIN public.ap_ar_trans ON public.ap_ar_trans.cust_code = public.ar_customer.code where public.ar_customer.code=%s"
            cur = gobal.con.cursor()
            cur.execute(sql_a,(id,))
            selectarid = cur.fetchone()
            # # sql_b = "SELECT z_ap.code, name_1, tel, item_name, amount, currency_name, total FROM z_ap LEFT JOIN z_set_ap ON z_set_ap.code = z_ap.code"
            # # sql_b = "SELECT code, name_1, tel FROM public.z_ap"
            # # curs = gobal.con.cursor()
            # # curs.execute(sql_b))

            cura= gobal.con.cursor()
            sql = "SELECT public.ap_ar_trans.doc_date, public.ap_ar_trans.doc_no, public.ar_customer.code, name_1, tel, item_name, total_value FROM public.ar_customer LEFT JOIN public.ap_ar_trans ON public.ap_ar_trans.cust_code = public.ar_customer.code"
            cura.execute(sql)
            # select = cura.fetchone()

            rate_trans = cura.fetchall()

            curs = gobal.con.cursor()
            sql_cur = "SELECT curency_code,curency_name FROM public.tb_addcurrency"
            curs.execute(sql_cur)
            curent = curs.fetchall()
            

            gobal.con.commit()
        return render_template('ap & ar/set_ar_copy.html',selectarid=selectarid,rate_trans = rate_trans, curent=curent,user=session.get("roles"))



@app.route('/saveset_ar', methods=['POST'])
def saveset_ar():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            # curb = gobal.con.cursor()
            # codee = request.form['codee']
            # curb.execute('update z_ap set code=%s where code=%s',
            #             (codee, (id,)))
            # gobal.con.commit()

            cur = gobal.con.cursor()
            sql = """INSERT INTO public.ap_ar_trans (doc_date, doc_no, item_name, currency_code, total_value, total_value_2, cust_code)
                     VALUES(%s,%s,%s,%s,%s,%s,%s);
                  """
                #   INSERT INTO z_set_ap (code)
                #   SELECT code
                #   FROM z_ap
            doc_date = request.form['doc_date']
            doc_no = request.form['doc_no']
            item_name = request.form['item_name']
            currency_code = request.form['currency_code']
            total_value = request.form['total_value']
            total_value_2 = request.form['total_value_2']
            cust_code = request.form['cust_code']
            data = (doc_date, doc_no, item_name, currency_code, total_value, total_value_2, cust_code)
            cur.execute(sql, data)
            # curb = gobal.con.cursor()
            # codee = request.form['codee']
            # curb.execute('insert into z_set_ap (code) values(%s)')
            # gobal.con.commit()
            print(data)
            return redirect(url_for('send_arid', id = cust_code))
@app.route('/update_set_ar/<string:id>', methods=['POST'])
def update_set_ar(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            item_name = request.form['item_name']
            amount = request.form['amount']
            currency_name = request.form['currency_name']
            total = request.form['total']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.set_ar set item_name=%s, amount=%s, currency_name=%s,total=%s where code=%s',
                        (item_name, amount, currency_name, total, (id,)))
            gobal.con.commit()
            return redirect(url_for('send_arid', id = id))
            # return render_template('ap & ar/set_ap_copy.html')

@app.route('/set_ar_delete/<string:id>')
def set_ar_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from public.set_ar where code=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('send_arid', id = id))
        # return render_template('ap & ar/set_ap_copy.html')
