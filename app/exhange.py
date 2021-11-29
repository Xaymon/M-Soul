
from flask import Flask, render_template, request, redirect, url_for, session
from kk_con import *
from app import app


@app.route('/homeex')
def homeex():
    with gobal.con:
        cur = gobal.con.cursor()
        # sql = """
        #         select name_1,rate,cur_1,cur2 from (
        #         select rate_name||'-'||rate_name_2 as name_1,rate_va_sale as rate,'K' as cur_1,'B' as cur2 from exchange_rate where rate_code='01'
        #         union all
        #         select rate_name_2||'-'||rate_name as name_1,rate_va_buy as rate,'B' as cur_1,'K' as cur2 from exchange_rate  where rate_code='01'
        #         union all
        #         select rate_name||'-'||rate_name_2 as name_1,rate_va_sale as rate,'K' as cur_1,'D' as cur2 from exchange_rate where rate_code='02'
        #         union all
        #         select rate_name_2||'-'||rate_name as name_1,rate_va_buy as rate,'D' as cur_1,'K' as cur2 from exchange_rate  where rate_code='02'
        #         union all
        #         select rate_name||'-'||rate_name_2 as name_1,rate_va_sale as rate,'B' as cur_1,'D' as cur2 from exchange_rate where rate_code='03'
        #         union all
        #         select rate_name_2||'-'||rate_name as name_1,rate_va_buy as rate,'D' as cur_1,'B' as cur2 from exchange_rate  where rate_code='03'
        #         ) as a
        #     """
        # cur.execute(sql)
        # rate_by = cur.fetchall()
    return render_template('exchange/index.html',)
@app.route('/listeexch')
def listeexch():
    # with gobal.con:
        # cur = gobal.con.cursor()
        # sql = """SELECT rate_va_sale,case when rate_code='01' then 'ບາດ' else 'ໂດລາ' end as name_show
        # FROM public.exchange_rate;"""
        # cur.execute(sql)
        # rate_by = cur.fetchall()
    return render_template('exchange/listexchh.html')
