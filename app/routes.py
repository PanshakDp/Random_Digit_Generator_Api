from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Pin
from app import db2
from random import randint



def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@app.route('/', methods=['GET'])
def index():
    """Root."""
    return make_response({
        'message_v1': 'To generate pin use this endpoint : /api/v1/pin/generate/, to validate pin use this endpoint /api/v1/pin/vaidate/<pin>/<serial>',
        'message_v2': 'To generate pin use this endpoint : /api/v2/pin/generate/, to validate pin use this endpoint /api/v2/pin/vaidate/<pin>/<serial>'
    })
    


@app.route('/api/v1/pin/generate/', methods=['GET'])
def generate_pin():
    """generate pin."""

    new_pin = Pin(
        digit=random_with_N_digits(15)
    )
    db.session.add(new_pin)  # Adds new User record to database
    db.session.commit()  # Commits all changes
    return make_response({'pin': new_pin.digit, 'serial': f'0{new_pin.id}', 'message': 'Pin generated sucesfully!'})


@app.route('/api/v1/pin/vaidate/<pin>/<serial>')
def validate_pin(pin, serial):
    """Validate pin"""
    pin = int(pin)
    serial = int(serial)
    db_pin = Pin.query.filter_by(digit=pin, id=serial).first()
    if db_pin:
        return make_response({'message': 'Pin valid'})
    return make_response({'message': 'Pin doest not exists ...!'}), 404


@app.route('/api/v2/pin/generate/', methods=['GET'])
def generate_pin2():
    pins = db2.pins
    digit = random_with_N_digits(15)
    serial = str(int(pins.find({}).count()) + 1)
    serial = '0'*(12 - len(serial))+serial
    pins.insert_one({'digit': digit, 'serial': serial})
    return make_response({'message': 'Pin generated sucesfully!', 'pin': digit, 'serial': f'0{serial}'})


@app.route('/api/v2/pin/validate/<pin>/<serial>')
def validate_pin2(pin, serial):
    pin = int(pin)
    serial = int(serial)

    pins = db2.pins
    serial = pins.find_one({'digit': pin, 'serial': serial})
    if serial:
        return make_response({'message': 'Pin valid'})
    return make_response({'message': 'Pin doest not exists ...!'}), 404
