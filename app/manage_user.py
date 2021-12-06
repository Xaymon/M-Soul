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
            sql = "SELECT username, password,roles,roworder FROM public.tb_user order by roworder "
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
            sql = """INSERT INTO tb_user(
                         username, password, roles)
                         values(%s,%s,%s)
                 """
            username = request.form['username']
            password = request.form['​password']
            roles = request.form['roles']
            data = (username, password, roles)
            cur.execute(sql, (data))
        gobal.con.commit()
        return redirect(url_for('manageadduser'))

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
