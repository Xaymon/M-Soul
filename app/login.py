from flask import Flask, render_template, request, redirect, url_for,session,jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route("/")
def index():
    if not session.get("name"):
        return redirect("/login")
    return redirect (url_for('home'))
@app.route('/login')
def loginform():
    return render_template('/login/login.html')
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_login = request.form.get('username')
        pass_login = request.form.get('password')
        sql="SELECT roles FROM public.tb_user where username=%s and password=%s"
        cur = gobal.con.cursor()
        chuer=(user_login,pass_login,)
        cur.execute(sql,chuer)
        logii = cur.fetchone()
        if logii:
            print(logii[0])
            session["name"] = request.form.get("username")
            session["roles"] = logii[0]
            return redirect(url_for('home'))
        else:
            return redirect(url_for('logout'))
@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")
