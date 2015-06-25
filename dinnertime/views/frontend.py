# -*- encoding:utf-8 -*-
from flask import Blueprint
from flask import Flask, render_template, request
import os

frontend = Blueprint('frontend',__name__)

@frontend.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    url = 'https://www.quantcast.com/'
    if request.method == "POST":
        # get url that the user has entered
        try:
            url = request.form['url']
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )
    print url
    return render_template('index.html', iframe=url)


