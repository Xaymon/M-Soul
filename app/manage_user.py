from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route('/manageadduser')
def manageadduser():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT username, password,roles FROM public.tb_user order by roworder "
            cur.execute(sql)
            rate_ = cur.fetchall()

            return render_template('manage/adduser.html', rate_=rate_)

@app.route('/save_user', methods=['POST'])
def save_user():
    with gobal.con:
        cur = gobal.con.cursor()
        if not session.get("name"):
            return redirect("/login")
        else:
            sql = """INSERT INTO public.tb_user(
                        username, password, roles)
                        values(%s,%s,%s)
                """
        username = request.form['username']
        password = request.form['password']
        roles = request.form['roles']
        data = (username, password, roles)
        cur.execute(sql, (data))
        gobal.con.commit()
        return redirect(url_for('manageadduser'))

# @app.route('/saverate', methods=['POST'])
# def saverate():
#     with gobal.con:
#         if not session.get("name"):
#             return redirect("/login")
#         else:
#             currency_code = request.form['currency_code']
#             buy = request.form['buy']
#             sale = request.form['sale']
#             curen_ = ""
#             if currency_code == '01':
#                 curen_ = 'THB'
#             elif currency_code == '02':
#                 curen_ = 'USD'
#             else:
#                 curen_ = 'THB-USD'
#             data = (currency_code, curen_, buy, sale)
#             cur = gobal.con.cursor()
#             sql = "update exchange_rate set date_end=LOCALTIMESTAMP(0) where date_end isnull and curency_code=%s"
#             cur.execute(sql, (currency_code,))
#             curs = gobal.con.cursor()
#             sqls = "INSERT INTO exchange_rate( curency_code, curency_name, buy, sale, date_start) VALUES (%s,%s,%s,%s,LOCALTIMESTAMP(0));"
#             curs.execute(sqls, (data))
#             gobal.con.commit()
#             return redirect(url_for('manageexrate'))


@app.route('/user_delete/<string:id>')
def user_delete(id):
    if not session.get("name"):
        return redirect("/login")
    else:
        cur = gobal.con.cursor()
        sql = "delete from public.tb_user where roworder=%s"
        cur.execute(sql, (id,))
        gobal.con.commit()
        return redirect(url_for('manageadduser'))
