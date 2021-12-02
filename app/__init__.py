from flask import Flask
import os, sys
app = Flask(__name__)
from app import login,exhange,transfer,home,reeport_cash,manage
