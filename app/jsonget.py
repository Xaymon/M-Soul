from flask import Flask, render_template, request, redirect, url_for, session, jsonify, json
from flask.helpers import flash
from werkzeug import datastructures
from kk_con import *
from app import app


@app.route("/exchangerate/<id>")
def exchangerate(id):
    sql = """select buy::text  from exchange_rate where curency_code=%s and date_end isnull"""
    cur = gobal.con.cursor()
    cur.execute(sql, (id, ))
    rate = cur.fetchone()
    return jsonify({'rate': rate})