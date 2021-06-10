from flask import Flask
import uuid
from random import seed
from random import random
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
app = Flask(__name__)

seed(1)

@app.route('/random')
def random_application():
    #generate uuid
    request_id = uuid.uuid1().hex
    response = {
                "uuid": request_id
                ,"consumer": "demonstration"
                ,"type": "request"
                , "value": random()
            }
    print(response)
    return  response

if __name__ == '__main__':
    app.run()