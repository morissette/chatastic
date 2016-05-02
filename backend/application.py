from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

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

# Setup Routes
api.add_resource(Slack, '/slack')
api.add_resource(PagerDuty, '/pagerduty')
api.add_resource(HipChat, '/hipchat')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
