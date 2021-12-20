
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
import psycopg2
from app import app
from kk_con import *
from datetime import datetime, date


@app.route('/cashkip')
def cashkip():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                    FROM cb_trans_detail where trans_number='01' and doc_date::date=current_date order by roworder ASC"""
            cur.execute(sql)
            kip = cur.fetchall()

            return render_template('/report/cash/kip.html', kip=kip, from_date=timestampStr, to_date=timestampStr)


@app.route('/kipbydate', methods=['POST'])
def kipbydate():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            print(from_date, to_date)
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                    FROM cb_trans_detail where trans_number='01' and doc_date::date between %s and %s order by roworder ASC"""
            data = (from_date, to_date,)
            cur.execute(sql, data)
            kip = cur.fetchall()
            return render_template('/report/cash/kip.html', kip=kip, from_date=from_date, to_date=to_date)


@app.route('/cashbaht')
def cashbaht():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                    FROM cb_trans_detail where trans_number='00' order by roworder ASC"""
            cur.execute(sql)
            baht = cur.fetchall()
            return render_template('/report/cash/baht.html', baht=baht, from_date=timestampStr, to_date=timestampStr)


@app.route('/bahtbydate', methods=['POST'])
def bahtbydate():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            print(from_date, to_date)
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                                        FROM cb_trans_detail where trans_number='00' and doc_date::date between %s and %s order by roworder ASC"""
            data = (from_date, to_date,)
            cur.execute(sql, data)
            kip = cur.fetchall()
            return render_template('/report/cash/kip.html', kip=kip, from_date=from_date, to_date=to_date)


@app.route('/cashdollar')
def cashdollar():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                                        FROM cb_trans_detail where trans_number='02' order by roworder ASC"""
            cur.execute(sql)
            dollar = cur.fetchall()
            return render_template('/report/cash/dolla.html', dollar=dollar, from_date=timestampStr, to_date=timestampStr)


@app.route('/dollatbydate', methods=['POST'])
def dollatbydate():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            print(from_date, to_date)
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                                        FROM cb_trans_detail where trans_number='00' and doc_date::date between %s and %s order by roworder ASC"""
            data = (from_date, to_date,)
            cur.execute(sql, data)
            kip = cur.fetchall()
            return render_template('/report/cash/kip.html', kip=kip, from_date=from_date, to_date=to_date)


@app.route('/bank_report')
def bank_report():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                    FROM cb_trans_detail where trans_number='' order by roworder ASC"""
            cur.execute(sql)
            dollar = cur.fetchall()

            curs = gobal.con.cursor()
            sql = "SELECT bank_id, bank_name  FROM public.tb_bank where bank_loca='lao' order by roworder "
            curs.execute(sql)
            bank_from = curs.fetchall()
            bank_code = ''
            return render_template('/report/transfer/banklao.html', dollar=dollar, from_date=timestampStr, to_date=timestampStr, bank_from=bank_from, bank_code=bank_code)


@app.route('/bank_report_sch', methods=['POST'])
def bank_report_sch():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            bank_code = request.form['bank_code']
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            print(from_date, to_date)
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                                        FROM cb_trans_detail where trans_number=%s and doc_date::date between %s and %s order by roworder ASC"""
            data = (bank_code, from_date, to_date,)
            cur.execute(sql, data)
            kip = cur.fetchall()
            curs = gobal.con.cursor()
            sql = "SELECT bank_id, bank_name  FROM public.tb_bank where bank_loca='lao' order by roworder "
            curs.execute(sql)
            bank_from = curs.fetchall()
            return render_template('/report/transfer/banklao.html', kip=kip, from_date=from_date, to_date=to_date, bank_from=bank_from, bank_code=bank_code)


@app.route('/bank_thai')
def bank_thai():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            dateTimeObj = datetime.now()
            timestampStr = dateTimeObj.strftime("%Y-%m-%d")
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                    FROM cb_trans_detail where trans_number='' order by roworder ASC"""
            cur.execute(sql)
            dollar = cur.fetchall()

            curs = gobal.con.cursor()
            sql = "SELECT bank_id, bank_name  FROM public.tb_bank where bank_loca='thai' order by roworder "
            curs.execute(sql)
            bank_from = curs.fetchall()
            bank_code = ''
            return render_template('/report/transfer/bankthai.html', dollar=dollar, from_date=timestampStr, to_date=timestampStr, bank_from=bank_from, bank_code=bank_code)


@app.route('/bank_thai_sch', methods=['POST'])
def bank_thai_sch():
    with gobal.con:
        if not session.get("name"):
            return redirect("/login")
        else:
            bank_code = request.form['bank_code']
            from_date = request.form['from_date']
            to_date = request.form['to_date']
            print(from_date, to_date)
            cur = gobal.con.cursor()
            sql = """SELECT  to_char(doc_date,'DD-MM-YYY HH24:MI:SS'),doc_no,case when trans_type='0' or trans_type='1' then 'ໂອນ' when trans_type='2' 
                    then 'ແລກປ່ຽນ' when trans_type='5' then 'ລາຍຮັບອື່ນໆ' when  trans_type='6' then 'ລາຍຈ່າຍອື່ນໆ' when  trans_type='11' then 'ຝາກທະນາຄານ' 
                    when  trans_type='12' then 'ຖອນຈາກທະນາຄານ'  end as trans_type,
                    to_char(case when calc_flag='1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_in, 
                    to_char(case when calc_flag='-1' then amount_1 else 0 end , '999G999G999G999D99') as Amount_out, 
                    to_char(SUM((case when calc_flag='1' then amount_1 else 0 end) - (case when calc_flag='-1' then amount_1 else 0 end))
                    OVER (ORDER BY roworder ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), '999G999G999G999D99')  as Balance
                                        FROM cb_trans_detail where trans_number=%s and doc_date::date between %s and %s order by roworder ASC"""
            data = (bank_code, from_date, to_date,)
            cur.execute(sql, data)
            kip = cur.fetchall()
            curs = gobal.con.cursor()
            sql = "SELECT bank_id, bank_name  FROM public.tb_bank  where bank_loca='thai' order by roworder "
            curs.execute(sql)
            bank_from = curs.fetchall()
            return render_template('/report/transfer/bankthai.html', kip=kip, from_date=from_date, to_date=to_date, bank_from=bank_from, bank_code=bank_code)
