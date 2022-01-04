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

            return render_template('ap & ar/pvhome.html',user=session.get("roles"))
@app.route('/pvlistap')
def pvlistap():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            # cur = gobal.con.cursor()
            # sql = "SELECT username, password,roles,roworder FROM public.tb_user order by roworder "
            # cur.execute(sql)
            # rate_ = cur.fetchall()

            return render_template('ap & ar/pvlistap.html',user=session.get("roles"))
            