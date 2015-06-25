#!/usr/bin/env python2
# -*- encoding:utf-8 -*-

from flask import Flask
from flaskext.actions import Manager
import settings
from dinnertime import app
from gevent.wsgi import WSGIServer

if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("", 5555), app)
    server.serve_forever()

