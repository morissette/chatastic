from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from aws import create_session

# Setup Core Flask
app = Flask(__name__)
CORS(app)
db = SQLAlchemy(app)
api = Api(app)

# DB Migrate and Upgrades
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

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

class Notification(Resource):

    def post(self):
        """
        create notification in SQS
        takes JSON
        {
            "id": \d+,
            "account_id": \d+,
            "name": \S+,
            "provider": \d+,
            "message": \d+,
        }
        """

        pass

# Setup Routes
api.add_resource(Slack, '/slack')
api.add_resource(PagerDuty, '/pagerduty')
api.add_resource(HipChat, '/hipchat')

# Notification Routes
api.add_resource(Notification, '/notification')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
