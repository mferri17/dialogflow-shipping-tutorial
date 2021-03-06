#!/usr/bin/env python
import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):

    result = req.get("result")
    action = result.get("action")
    parameters = result.get("parameters")
    cost = {'Europe':100, 'North America':500000, 'South America':300, 'Asia':400, 'Africa':500}
    birthYears = {'Caravaggio':1571, 'Picasso':1881, 'Bellini':1433, 'Giotto':1267}
    birthCities = {'Caravaggio':'Milano', 'Picasso':'Malaga', 'Bellini':'Venezia', 'Giotto':'Vespignano'}
    
    if action == "author.birthdate":
        author = parameters.get("author")
        speech = author + " was born in " + str(birthYears[author]) + "."
    elif action == "author.birthcity":
        author = parameters.get("author")
        speech = author + " was born in " + str(birthCities[author]) + "."
    elif action == "shipping.cost":
        zone = parameters.get("shipping-zone")
        speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
    else:
        speech = "Sorry but I don't know this information, but I will improve myself :("
     
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
