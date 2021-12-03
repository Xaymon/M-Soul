
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *


@app.route('/cashkip')
def cashkip():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(ex_date,'DD-MM-YYY HH24:MI:SS'),
                to_char(case when ex_1='K' then amount_1 else 0 end, '999G999G999G999D99'), 
                to_char(case when ex_2='K' then amount_2 else 0 end, '999G999G999G999D99'), 
                to_char(SUM((case when ex_1='K' then amount_1 else 0 end) - (case when ex_2='K' then amount_2 else 0 end))
                OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                FROM ic_trans
                order by ex_date"""
            cur.execute(sql)
            kip = cur.fetchall()
            return render_template('/report/cash/kip.html', kip=kip)


@app.route('/cashbaht')
def cashbaht():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(ex_date,'DD-MM-YYY HH24:MI:SS'),
                to_char(case when ex_1='B' then amount_1 else 0 end, '999G999G999G999D99'), 
                to_char(case when ex_2='B' then amount_2 else 0 end, '999G999G999G999D99'), 
                to_char(SUM((case when ex_1='B' then amount_1 else 0 end) - (case when ex_2='B' then amount_2 else 0 end))
                OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                FROM ic_trans
                order by ex_date"""
            cur.execute(sql)
            baht = cur.fetchall()
            return render_template('/report/cash/baht.html', baht=baht)


@app.route('/cashdollar')
def cashdollar():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(ex_date,'DD-MM-YYY HH24:MI:SS'),
                to_char(case when ex_1='D' then amount_1 else 0 end, '999G999G999G999D99'), 
                to_char(case when ex_2='D' then amount_2 else 0 end, '999G999G999G999D99'), 
                to_char(SUM((case when ex_1='D' then amount_1 else 0 end) - (case when ex_2='D' then amount_2 else 0 end))
                OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                FROM ic_trans
                order by ex_date"""
            cur.execute(sql)
            baht = cur.fetchall()
            return render_template('/report/cash/dolla.html', baht=baht)
