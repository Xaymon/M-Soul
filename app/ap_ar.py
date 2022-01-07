from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *
from datetime import datetime


@app.route('/ap')
def ap():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT code, name_1, tel, b.prov_name, c.city_name, address, remark,a.city,a.province FROM public.ap_supplier a 
                    left join province b on a.province=b.prov_code 
                    left join city c on b.prov_code =c.prov_code and c.city_code = a.city"""
            cur.execute(sql)
            rate_trans = cur.fetchall()

            curb = gobal.con.cursor()
            sql_p = "select prov_code, prov_name from province order by prov_code"
            curb.execute(sql_p)
            prov_list = curb.fetchall()
            return render_template('ap & ar/ap.html', rate_trans=rate_trans, prov_list=prov_list, user=session.get("roles"))


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
            data = (codee, name_1, tel, province, city, address, remark)
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

            print(province, "city = ", city)

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

            return render_template('ap & ar/ap_pay.html', rate_trans=rate_trans, user=session.get("roles"))


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
            return render_template('ap & ar/ar.html', rate_trans=rate_trans, prov_list=prov_list, city_list=city_list, user=session.get("roles"))


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
            data = (codee, name_1, tel, province, city, address, remark)
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
            sql = """
                SELECT doc_no,to_char(doc_date,'DD-MM-YYYY'),cust_code,b.name_1,tel,item_name,to_char(total_value_2,'999G999G999G999D99')||' '||c.curency_name FROM public.ap_ar_trans a
                left join ap_supplier b on b.code=a.cust_code
                left join tb_addcurrency c on c.curency_code=a.currency_code
                where trans_flag='55'"""
            cur.execute(sql)
            rate_trans = cur.fetchall()
            cura = gobal.con.cursor()
            sqlap = "SELECT code,name_1,tel FROM ap_supplier"
            cura.execute(sqlap)
            ap_list = cura.fetchall()

            return render_template('ap & ar/set_ap.html', rate_trans=rate_trans, ap_list=ap_list, user=session.get("roles"))


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
            return render_template('ap & ar/set_ap_copy.html', rate_trans=rate_trans, user=session.get("roles"))


@app.route('/send_apid/<string:id>', methods=['GET'])
def send_apid(id):
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            sql_a = "SELECT public.ap_ar_trans.doc_date, public.ap_ar_trans.doc_no, public.ap_supplier.code, name_1, tel, item_name, total_value_2 FROM public.ap_supplier LEFT JOIN public.ap_ar_trans ON public.ap_ar_trans.cust_code = public.ap_supplier.code where public.ap_supplier.code=%s"
            cur = gobal.con.cursor()
            cur.execute(sql_a, (id,))
            selectapid = cur.fetchone()

            curs = gobal.con.cursor()
            sql_cur = "SELECT curency_code,curency_name FROM public.tb_addcurrency where curency_code !='03'"
            curs.execute(sql_cur)
            curent = curs.fetchall()
            dateTimeObj = datetime.now()
            doc_date = dateTimeObj.strftime("%Y-%m-%d")
            sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from ap_ar_trans where trans_flag='55'"""
            cur_d = gobal.con.cursor()
            cur_d.execute(sql_d)
            bil_no = cur_d.fetchone()
            doc_no = ''
            if bil_no[0] == None:
                doc_no = 'COB-100001'
            else:
                doc = bil_no[0]
                a = doc+1
                doc_no = "COB-"+str(a)
            doc_no = doc_no
            return render_template('ap & ar/set_ap_copy.html', selectapid=selectapid, curent=curent, doc_no=doc_no, doc_date=doc_date, user=session.get("roles"))


@app.route('/saveset_ap', methods=['POST'])
def saveset_ap():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """INSERT INTO public.ap_ar_trans (doc_date, doc_no, item_name, currency_code, total_value, total_value_2, cust_code,trans_flag,calc_flag)
                     VALUES(%s,%s,%s,%s,%s,%s,%s,55,1);
                  """
            doc_date = request.form['doc_date']
            doc_no = request.form['doc_no']
            item_name = request.form['item_name']
            currency_code = request.form['currency_code']
            total_value = request.form['total_value']
            total_value_2 = request.form['total_value_2']
            cust_code = request.form['cust_code']
            data = (doc_date, doc_no, item_name, currency_code,
                    total_value, total_value_2, cust_code)
            cur.execute(sql, data)
            gobal.con.commit()
            return redirect(url_for('setap'))


@app.route('/update_set_ap/<string:id>', methods=['POST'])
def update_set_ap(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            item_name = request.form['item_name']
            total_value_2 = request.form['total_value_2']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.ap_ar_trans set item_name=%s, total_value_2=%s where doc_no=%s',
                        (item_name, total_value_2, (id,)))
            gobal.con.commit()
            return redirect(url_for('setap'))
            # return render_template('ap & ar/set_ap_copy.html')


@app.route('/set_ap_delete/<string:id>')
def set_ap_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from public.ap_ar_trans where doc_no=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('setap'))
        # return render_template('ap & ar/set_ap_copy.html')


@app.route('/setar')
def setar():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """
                SELECT doc_no,to_char(doc_date,'DD-MM-YYYY'),cust_code,b.name_1,tel,item_name,to_char(total_value_2,'999G999G999G999D99')||' '||c.curency_name FROM public.ap_ar_trans a
                left join ar_customer b on b.code=a.cust_code
                left join tb_addcurrency c on c.curency_code=a.currency_code
                where trans_flag='44'"""
            cur.execute(sql)
            rate_trans = cur.fetchall()
            cura = gobal.con.cursor()
            sqlap = "SELECT code,name_1,tel FROM ar_customer"
            cura.execute(sqlap)
            ar_list = cura.fetchall()
            return render_template('ap & ar/set_ar.html', rate_trans=rate_trans, ar_list=ar_list, user=session.get("roles"))


@app.route('/send_arid/<string:id>', methods=['GET'])
def send_arid(id):
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            sql_a = "SELECT code,name_1,tel FROM ar_customer where code=%s"
            cur = gobal.con.cursor()
            cur.execute(sql_a, (id,))
            selectapid = cur.fetchone()
            curs = gobal.con.cursor()
            sql_cur = "SELECT curency_code,curency_name FROM public.tb_addcurrency where curency_code !='03'"
            curs.execute(sql_cur)
            curent = curs.fetchall()
            dateTimeObj = datetime.now()
            doc_date = dateTimeObj.strftime("%Y-%m-%d")
            sql_d = """select max(SPLIT_PART(doc_no,'-', 2))::int from ap_ar_trans where trans_flag='44'"""
            cur_d = gobal.con.cursor()
            cur_d.execute(sql_d)
            bil_no = cur_d.fetchone()
            doc_no = ''
            if bil_no[0] == None:
                doc_no = 'AOB-100001'
            else:
                doc = bil_no[0]
                a = doc+1
                doc_no = "AOB-"+str(a)
            doc_no = doc_no
            return render_template('ap & ar/set_ar_copy.html', selectapid=selectapid, curent=curent, doc_no=doc_no, doc_date=doc_date, user=session.get("roles"))


@app.route('/saveset_ar', methods=['POST'])
def saveset_ar():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """INSERT INTO public.ap_ar_trans (doc_date, doc_no, item_name, currency_code, total_value, total_value_2, cust_code,trans_flag,calc_flag)
                     VALUES(%s,%s,%s,%s,%s,%s,%s,44,1);
                  """
            doc_date = request.form['doc_date']
            doc_no = request.form['doc_no']
            item_name = request.form['item_name']
            currency_code = request.form['currency_code']
            total_value = request.form['total_value']
            total_value_2 = request.form['total_value_2']
            cust_code = request.form['cust_code']
            data = (doc_date, doc_no, item_name, currency_code,
                    total_value, total_value_2, cust_code)
            cur.execute(sql, data)
            return redirect(url_for('setar'))


@app.route('/update_set_ar/<string:id>', methods=['POST'])
def update_set_ar(id):
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            item_name = request.form['item_name']
            total_value_2 = request.form['total_value_2']

            # data = (item_name, cash_kip, cash_baht, cash_dollar, bill_date)
            cur.execute('update public.ap_ar_trans set item_name=%s, total_value_2=%s where doc_no=%s',
                        (item_name, total_value_2, (id,)))
            gobal.con.commit()
            return redirect(url_for('setar'))
            # return render_template('ap & ar/set_ap_copy.html')


@app.route('/set_ar_delete/<string:id>')
def set_ar_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        print(id)
        cur = gobal.con.cursor()
        sql = "delete from public.ap_ar_trans where doc_no=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('setar'))
        # return render_template('ap & ar/set_ap_copy.html')


# report balance
@app.route('/report_ap_balance')
def report_ap_balance():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            cur = gobal.con.cursor()
            sql = """SELECT doc_no,to_char(doc_date,'DD-MM-YYYY'),cust_code,b.name_1,item_name,to_char(total_value_2,'999G999G999G999D99')||' '||c.curency_name FROM public.ap_ar_trans a
                    left join ap_supplier b on b.code=a.cust_code
                    left join tb_addcurrency c on c.curency_code=a.currency_code
                    where trans_flag='55' and doc_date::date=current_date"""
            cur.execute(sql)
            ap_bl = cur.fetchall()

            return render_template('/ap & ar/report/ap_balance.html', ap_bl=ap_bl, from_date=timestampStr, to_date=timestampStr,user=session.get("roles"))

@app.route('/ap_bl_date', methods=['POST'])
def ap_bl_date():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            print(from_date, to_date)
            cur = gobal.con.cursor()
            sql = """SELECT doc_no,to_char(doc_date,'DD-MM-YYYY'),cust_code,b.name_1,item_name,to_char(total_value_2,'999G999G999G999D99')||' '||c.curency_name FROM public.ap_ar_trans a
                    left join ap_supplier b on b.code=a.cust_code
                    left join tb_addcurrency c on c.curency_code=a.currency_code
                    where trans_flag='55' and doc_date::date between %s and %s ORDER BY a.roworder ASC"""
            data = (from_date, to_date,)
            cur.execute(sql, data)
            ap_bl = cur.fetchall()
            return render_template('/ap & ar/report/ap_balance.html', ap_bl=ap_bl, from_date=from_date, to_date=to_date,user=session.get("roles"))

# report payment
@app.route('/report_ap_payment')
def report_ap_payment():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            cur = gobal.con.cursor()
            sql = """SELECT to_char(doc_date,'DD-MM-YYYY'), doc_no, doc_ref, cust_code, item_name, to_char(pay_value,'999G999G999G999D99') 
                    FROM payment where trans_flag=129 and doc_date::date=current_date ORDER BY roworder ASC"""
            cur.execute(sql)
            ap_pm = cur.fetchall()

            return render_template('/ap & ar/report/ap_payment.html', ap_pm=ap_pm, from_date=timestampStr, to_date=timestampStr,user=session.get("roles"))

@app.route('/ap_pm_date', methods=['POST'])
def ap_pm_date():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            print(from_date, to_date)
            cur = gobal.con.cursor()
            sql = """SELECT to_char(doc_date,'DD-MM-YYYY'), doc_no, doc_ref, cust_code, item_name, to_char(pay_value,'999G999G999G999D99') 
                    FROM payment where trans_flag=129 and doc_date::date between %s and %s ORDER BY roworder ASC"""
            data = (from_date, to_date,)
            cur.execute(sql, data)
            ap_pm = cur.fetchall()
            return render_template('/ap & ar/report/ap_payment.html', ap_pm=ap_pm, from_date=from_date, to_date=to_date,user=session.get("roles"))

# report ar balance
@app.route('/report_ar_balance')
def report_ar_balance():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            cur = gobal.con.cursor()
            sql = """SELECT to_char(doc_date,'DD-MM-YYYY'),doc_no,cust_code,b.name_1,item_name,to_char(total_value_2,'999G999G999G999D99')||' '||c.curency_name FROM public.ap_ar_trans a
                    left join ar_customer b on b.code=a.cust_code
                    left join tb_addcurrency c on c.curency_code=a.currency_code
                    where trans_flag='44' and doc_date::date=current_date"""
            cur.execute(sql)
            ar_bl = cur.fetchall()

            return render_template('/ap & ar/report/ar_balance.html', ar_bl=ar_bl, from_date=timestampStr, to_date=timestampStr,user=session.get("roles"))

@app.route('/ar_bl_date', methods=['POST'])
def ar_bl_date():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            print(from_date, to_date)
            cur = gobal.con.cursor()
            sql = """ SELECT to_char(doc_date,'DD-MM-YYYY'),doc_no,cust_code,b.name_1,item_name,to_char(total_value_2,'999G999G999G999D99')||' '||c.curency_name FROM public.ap_ar_trans a
                    left join ar_customer b on b.code=a.cust_code
                    left join tb_addcurrency c on c.curency_code=a.currency_code
                    where trans_flag='44'and doc_date between %s and %s order by a.roworder ASC"""
            data = (from_date, to_date,)
            cur.execute(sql, data)
            ar_bl = cur.fetchall()
            return render_template('ap & ar/report/ar_balance.html', ar_bl=ar_bl, from_date=from_date, to_date=to_date,user=session.get("roles"))

@app.route('/report_ar_payment')
def report_ar_payment():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            cur = gobal.con.cursor()
            sql = """SELECT to_char(doc_date,'DD-MM-YYYY'), doc_no, doc_ref, cust_code, item_name, to_char(pay_value,'999G999G999G999D99')||' '||c.curency_name FROM payment a
                    left join ar_customer b on b.code=a.cust_code
                    left join tb_addcurrency c on c.curency_code=a.currency_code
                    where trans_flag=139 and doc_date::date=current_date"""
                    # SELECT to_char(doc_date,'DD-MM-YYYY'), doc_no, doc_ref, cust_code, item_name, to_char(pay_value,'999G999G999G999D99') FROM payment where trans_flag=139
            cur.execute(sql)
            ar_pm = cur.fetchall()

            return render_template('/ap & ar/report/ar_payment.html', ar_pm=ar_pm, from_date=timestampStr, to_date=timestampStr,user=session.get("roles"))

@app.route('/ar_pm_date', methods=['POST'])
def ar_pm_date():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            print(from_date, to_date)
            cur = gobal.con.cursor()
            sql = """ SELECT to_char(doc_date,'DD-MM-YYYY'), doc_no, doc_ref, cust_code, item_name, to_char(pay_value,'999G999G999G999D99')||' '||c.curency_name FROM payment a
                    left join ar_customer b on b.code=a.cust_code
                    left join tb_addcurrency c on c.curency_code=a.currency_code
                   where trans_flag=139 and doc_date between %s and %s order by a.roworder ASC"""
            data = (from_date, to_date,)
            cur.execute(sql, data)
            ar_pm = cur.fetchall()
            return render_template('ap & ar/report/ar_payment.html', ar_pm=ar_pm, from_date=from_date, to_date=to_date,user=session.get("roles"))