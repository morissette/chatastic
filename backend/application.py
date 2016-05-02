from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from aws import create_session
import json

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
        """
        Get a Slack Account
        """
        pass

    def post():
        """
        Connect to a Slack Account
        """
        pass

# PagerDuty Handler
class PagerDuty(Resource):

    def get():
        """
        Get a Connected PagerDuty
        """
        pass

    def post():
        """
        Connect to a PagerDuty Connection
        """
        pass

# HipChat Handler
class HipChat(Resource):

    def get():
        """
        Get a Connected HipChat
        """
        pass

    def post():
        """
        Connect to a HipChat Connection
        """
        pass

class Notification(Resource):

    def get(self):
        """
        Get a list of pending messages
        """
        pass

    def delete(self, message_id):
        """
        Delete Message id
        """
        pass

    def post(self):
        """
        create notification in SQS
        takes JSON
        [root@mori ~]# curl -X POST localhost:5000/notification -d '{"hello": "world"}'
        {
                "error": "Missing required fields"
        }
        [root@mori ~]# curl -X POST localhost:5000/notification -d '{"id": 1, "account_id": 1, "provider": 1, "message": "hello", "name": "foo"}'
        {
                "success": "Message queued"
        }
        """
        data = request.get_json(force=True)
        id = self.validate_number(data.get('id'))
        account_id = self.validate_number(data.get('account_id'))
        name = self.validate_word(data.get('name'))
        provider = self.validate_number(data.get('provider'))
        message = data.get('message')
        if id and account_id and name and provider and message:
            message_json = json.dumps({
                "id": id,
                "account_id": account_id,
                "name": name,
                "provider": provider,
                "message": message,
            })
            session = create_session()
            response = session.get_queue_url(
                QueueName='MyChatQueue'
            )
            url = response['QueueUrl']

            if url:
                session.send_message(
                    QueueUrl=url,
                    MessageBody=message_json,
                    DelaySeconds=0,
                )
                return {"success": "Message queued"}
            else:
                return {"error": "Failed to get SQS queue"}
        else:
            return {"error": "Missing required fields"}

    def validate_number(self, number):
        return number

    def validate_word(self, word):
        return word

# Setup Routes
api.add_resource(Slack, '/slack')
api.add_resource(PagerDuty, '/pagerduty')
api.add_resource(HipChat, '/hipchat')

# Notification Routes
api.add_resource(Notification, '/notification')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
