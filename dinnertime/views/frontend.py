# -*- encoding:utf-8 -*-
from flask import Blueprint
from flask import Flask, render_template, request, Response

import os
import datetime
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue

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
    def notify():
        msg = 'start'
        print msg
        for sub in subscriptions[:]:
            sub.put(msg)
    
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


