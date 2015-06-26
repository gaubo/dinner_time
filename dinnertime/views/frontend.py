# -*- encoding:utf-8 -*-
from flask import Blueprint
from flask import Flask, render_template, request, Response

import os
import datetime
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from scrape import get_meal_info, get_meal_info2

frontend = Blueprint('frontend',__name__)
subscriptions = []

class ServerSentEvent(object):
    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) 
                 for k, v in self.desc_map.iteritems() if k]
        
        return "%s\n\n" % "\n".join(lines)

@frontend.route('/', methods=['GET', 'POST'])
def index():
    url = 'https://www.quantcast.com/'
    if request.method == "POST":
        # get url that the user has entered
        try:
            url = request.form['url']
        except:
            url = 'https://www.quantcast.com/'
    print url
    return render_template('index.html', iframe=url)

@frontend.route("/start")
def start():

    def notify2():

        meal_info = get_meal_info()
        vendor_html = '''
                <div class="dish">
                    <div class="item-header">
                        <h4 class="item-name">''' + meal_info['vendor'] + '''</h4>
                    </div>
                    <div class="dietary-info">
                        <h6 class="item-name">''' + meal_info['order'] + '''</h4>
                    </div>
                    <div class="dietary-info">
                        <h6 class="item-name">''' + meal_info['description'] + '''</h4>
                    </div>
                    <div class="dietary-info">
                        <img src ="''' + meal_info['img_url'] + '''">
                    </div>
                </div>
        '''

        dish_html_format = '''
                    <div class="item-header">
                        <h4 class="item-name">{}</h4>
                    </div>
                    <div class="dietary-info">
                        <h6 class="item-name">{}</h4>
                    </div>
        '''

        dish_img_format = '''
                    <div class="dietary-info">
                        <img src ="{}">
                    </div>
        '''

        items_html = ""
        for item in meal_info['items']:
            item_html = str.format(dish_html_format, item['name'], item['description'])
            if item['img_url']:
                item_html += str.format(dish_img_format, item['img_url'])
            item_html = '''
                <div class="dish">
                    ''' + item_html + '''
                </div>
            '''
            items_html += item_html
        html = '''
        <marquee behavior="scroll" direction="left">
            <div class="row">
                ''' + vendor_html + items_html + '''
            </div>
        </marquee>
        '''

    def notify():

        data = get_meal_info2()
        overview_html = data['overview']
        overview_html = '''
        <div class = "col-xs-6">
        <div class = "overview">
            ''' + overview_html + '''
        </div>
        </div>
        '''
        menu_html = data['menu']
        menu_html = '''
        <div class = "col-xs-6">
        <div class = "menu">
        <marquee behavior="scroll" direction="up">
            ''' + menu_html + '''
        </marquee>
        </div>
        </div>
        '''
        html = '''
        <div class = "container">
        <div class = "row">
        <div class = "dinner">
            ''' + overview_html + menu_html + '''
        </div>
        </div>
        </div>
        '''
        html = html.replace('\n', '')

        for sub in subscriptions[:]:
            sub.put(html)
    
    gevent.spawn(notify)
    
    return "Message sent ..."

@frontend.route("/end")
def end():
    def notify():
        msg = 'end'
        print msg
        for sub in subscriptions[:]:
            sub.put(msg)
    
    gevent.spawn(notify)
    
    return "Message sent ..."

@frontend.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: 
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")
