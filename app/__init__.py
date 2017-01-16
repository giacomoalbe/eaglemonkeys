# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)
app.secret_key = 'thisimysecret:pleasekeepit!'

from app import views 

