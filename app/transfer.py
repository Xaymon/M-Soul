from flask import Flask, render_template, request, redirect, url_for,session
import psycopg2
from app import app



@app.route('/hometf')
def hometf():
    return render_template('transfer/index.html')
