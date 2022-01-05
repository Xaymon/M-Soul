from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *
from datetime import datetime
from flask.helpers import flash


@app.route('/pvhome')
def pvhome():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            # cur = gobal.con.cursor()
            # sql = "SELECT username, password,roles,roworder FROM public.tb_user order by roworder "
            # cur.execute(sql)
            # rate_ = cur.fetchall()

            return render_template('ap & ar/pvhome.html', user=session.get("roles"))


@app.route('/pvlistap')
def pvlistap():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """
                SELECT doc_no,to_char(doc_date,'DD-MM-YYYY'),cust_code,b.name_1,item_name,to_char(total_value_2,'999G999G999G999D99')||' '||c.curency_name FROM public.ap_ar_trans a
                left join ap_supplier b on b.code=a.cust_code
                left join tb_addcurrency c on c.curency_code=a.currency_code
                where trans_flag='55'
                """
            cur.execute(sql)
            list_cob = cur.fetchall()

            return render_template('ap & ar/pvlistap.html',list_cob=list_cob,user=session.get("roles"))
@app.route('/showap_detail/<string:id>')
def showap_detail(id):
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql ="""
            SELECT doc_no,doc_date,cust_code,b.name_1,item_name,total_value_2,currency_code,c.curency_name FROM public.ap_ar_trans a
            left join ap_supplier b on b.code=a.cust_code
            left join tb_addcurrency c on c.curency_code=a.currency_code
            where doc_no=%s
            """
            cur.execute(sql,(id,))
            showcob = cur.fetchone()
            return render_template('ap & ar/showcobpay.html',showcob=showcob,user=session.get("roles"))
