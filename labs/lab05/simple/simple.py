from json import dumps
from flask import Flask, request

APP = Flask(__name__)

# GLOBAL VARIABLE BELOW
names = []
# GLOBAL VARIABLE ABOVE

def getNames():
    global names
    return names

@APP.route('/names', methods=['GET'])
def get():
    data = getNames()
    return dumps({
        'names' : data,
    })

@APP.route('/name/add', methods=['POST'])
def create():
    data = getNames()
    data.append(request.form.get('name'))
    return dumps({})

@APP.route('/name/remove', methods=['DELETE'])
def update():
    data = getNames()
    data.remove(request.form.get('name'))
    return dumps({})

if __name__ == '__main__':
    APP.run()
