from flask import Flask, render_template, request, redirect, url_for,session
import psycopg2
from app import app



@app.route('/')
def index():

    return render_template('index.html')
