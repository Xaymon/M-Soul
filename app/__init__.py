from flask import Flask
import os, sys
app = Flask(__name__)
from app import login,exhange, report_cash,transfer,home,manage
