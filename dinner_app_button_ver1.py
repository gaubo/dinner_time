__author__ = 'jtom'

from urllib2 import Request, urlopen
import urllib2 
import time
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19,GPIO.OUT)

def update_hip_chat():
    V2TOKEN = 'E7CxTea1vztonzfDCvEqPJYJWkDGola4UzPnKB0A'
    ROOMID = 1670106
    url = 'https://api.hipchat.com/v2/room/%d/notification' % ROOMID
    message = "Dinner Is Here! <a href="https://zerocater.com/menu/uVGcXhj/"> Menu </a>"
    headers = {
        "content-type": "application/json",
        "authorization": "Bearer %s" % V2TOKEN}
    datastr = json.dumps({
        'message': message,
        'color': 'red',
        'message_format': 'html',
        'notify': True})
    request = Request(url, headers=headers, data=datastr)
    uo = urlopen(request)
    rawresponse = ''.join(uo)
    uo.close()
    assert uo.code == 204

def show_dinner_is_here():
    url='http://hackathon-dinner-time.ad-optimization.cloud2.qc:5555/start'
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        print response.info()
        print html
        response.close()

    except:
        print 'BROKEN!'



def stop_showing_dinner_is_here():
    url='http://hackathon-dinner-time.ad-optimization.cloud2.qc:5555/end'
    try:
        response = urllib2.urlopen(url)
        html = response.read()
        print response.info()
        print html
        response.close()
        return 'red light'

    except:
        print 'red light'


while True:
    input_state = GPIO.input(18)
    if input_state == False:
        GPIO.output(19,True)
        show_dinner_is_here()
        update_hip_chat()
        time.sleep(10.0)
        stop_showing_dinner_is_here()
        GPIO.output(19,False)

