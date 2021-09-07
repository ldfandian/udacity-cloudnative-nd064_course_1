from flask import Flask
app = Flask(__name__)

import json

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/status")
def getStatus():
    return json.dumps({
        'result':'OK - healthy'
    })

@app.route("/metrics")
def getMetrics():
    return json.dumps({
        'data': {
            'userCount': 140,
            'userCountActive': 23
        }
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0')
