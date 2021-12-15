from flask import Flask, render_template, request, redirect, url_for, session
from kk_con import *
from app import app


@app.route('/home')
def home():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = "SELECT curency_code, curency_name, buy, sale FROM public.exchange_rate where date_end isnull order by curency_code "
            cur.execute(sql)
            rate_ = cur.fetchall()
            return render_template('index.html', rate_=rate_)
