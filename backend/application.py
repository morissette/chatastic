from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

# Slack Handler
class Slack(Resource):

    def get():
        pass

    def post():
        pass

# PagerDuty Handler
class PagerDuty(Resource):

    def get():
        pass

    def post():
        pass

# HipChat Handler
class HipChat(Resource):

    def get():
        pass

    def post():
        pass

# Setup Routes
api.add_resource(Slack, '/slack')
api.add_resource(PagerDuty, '/pagerduty')
api.add_resource(HipChat, '/hipchat')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
