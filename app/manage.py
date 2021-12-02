from flask import Flask, render_template, request, redirect, url_for,session,jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route('/manageexrate')
def manageexrate():
    # cur = gobal.con.cursor()
    # sql="SELECT curency_code, curency_name, buy, sale FROM public.exchange_rate where date_end isnull order by roworder "
    # cur.execute(sql)
    # rate_ = cur.fetchall()

    return render_template('manage/index.html')
