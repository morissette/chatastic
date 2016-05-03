from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from aws import create_session
from models import *
import json, requests, urllib2

# Setup Core Flask
app = Flask(__name__)
app.config.from_object('config.Production')

CORS(app)
db = SQLAlchemy(app)
api = Api(app)

# DB Migrate and Upgrades
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Slack Handler
class Slack(Resource):

    def get(self):
        """
        Get a Slack Account
        """
      	account_id = 1
        provider_id = 2
        settings = get_creds(account_id, provider_id)
        if settings:
            return {"success": settings}
        else:
            return {"error": "No Slack Account Connected"}

    def post(self):
        """
        Connect to a Slack Account
        """
        data = request.get_json(force=True)
        account_id = 1
        provider_id = 2
        token = data.get('token')
        channel = data.get('channel')
        botname = data.get('botname')
        if token and channel and botname:
            new = ProviderSettings(account_id, provider_id, token, channel, botname)
            db.session.add(new)
            db.session.commit()
            return {"success": "Slack Integrated"}
        else:
            return {"error": "Missing required fields"}

    def put(self):
	message = request.get_json(force=True)['message']
        account_id = 1
        provider_id = 2
        settings = get_creds(account_id, provider_id)
        if settings:
            token = settings['token']
            channel = settings['channel']
            botname = settings['botname']
	    url = "https://slack.com/api/chat.postMessage?token=" + \
            token + "&channel=" + \
            channel + "&username=" + \
            botname + "&text=" + message
   	    try:
        	requests.get(url)
        	return {"success": "Message sent"}
    	    except requests.exceptions.ConnectionError:
        	return {"error": "Unable to connect to slack"}

# PagerDuty Handler
class PagerDuty(Resource):

    def get(self):
        """
        Get a Connected PagerDuty
        """
	account_id = 1
        provider_id = 1
        settings = get_creds(account_id, provider_id)
        if settings:
            return {"success": settings}
        else:
            return {"error": "No PagerDuty Account Connected"}


    def post(self):
        """
        Connect to a PagerDuty Connection
        """
	data = request.get_json(force=True)
        account_id = 1
        provider_id = 1
        token = data.get('token')
        channel = data.get('channel')
        botname = data.get('botname')
        if token and channel and botname:
            new = ProviderSettings(account_id, provider_id, token, channel, botname)
            db.session.add(new)
            db.session.commit()
            return {"success": "PagerDuty Integrated"}
        else:
            return {"error": "Missing required fields"}

    def put(self):
        message = request.get_json(force=True)['message']
        account_id = 1
        provider_id = 1
        settings = get_creds(account_id, provider_id)
        if settings:
            url = 'https://events.pagerduty.com/generic/2010-04-15/create_event.json'
            payload = json.dumps({
                "service_key": '798d0f7fd0ec4132a7f0cc6ac055d6ea',
                "event_type": 'trigger',
                "description": message
            })
            response = requests.post(url, payload)
            print response

# HipChat Handler
class HipChat(Resource):

    def get(self):
        """
        Get a Connected HipChat
        """
        account_id = 1
        provider_id = 3
        settings = get_creds(account_id, provider_id)
        if settings:
            return {"success": settings}
        else:
            return {"error": "No HipChat Account Connected"}


    def post(self):
        """
        Connect to a HipChat Connection
        """
	data = request.get_json(force=True)
        account_id = 1
        provider_id = 3
        token = data.get('token')
        channel = data.get('channel')
        botname = data.get('botname')
        if token and channel and botname:
            new = ProviderSettings(account_id, provider_id, token, channel, botname)
            db.session.add(new)
            db.session.commit()
            return {"success": "HipChat Integrated"}
        else:
            return {"error": "Missing required fields"}

    def put(self):
        """
        Send notifcation to hipchat
        """
        message = request.get_json(force=True)['message']
        account_id = 1
        provider_id = 3
        settings = get_creds(account_id, provider_id)
        if settings:
            url = 'https://api.hipchat.com/v2/room/2637466/notification?auth_token={}'.format(settings['token'])
            headers = {
                "Content-type": "application/json"
            }
            payload = json.dumps({
                "message": message,
            })
            response = requests.post(url, payload, headers=headers)
            return {"success": "Message Sent"}

class VictorOps(Resource):

    def get(self):
        account_id = 1
        provider_id = 4
        settings = get_creds(account_id, provider_id)
        if settings:
            return {"success": settings}
        else:
            return {"error": "No HipChat Account Connected"}

    def post(self):
        data = request.get_json(force=True)
        account_id = 1
        provider_id = 4
        token = data.get('token')
        botname = data.get('botname')
        if token and channel and botname:
            new = ProviderSettings(account_id, provider_id, token, channel, botname)
            db.session.add(new)
            db.session.commit()
            return {"success": "VictorOps Integrated"}
        else:
            return {"error": "Missing required fields"}

    def put(self):
        message = request.get_json(force=True)['message']
        account_id = 1
        provider_id = 4
        settings = get_creds(account_id, provider_id)
        if settings:
            api_id = '53c604c5'
            url = 'https://alert.victorops.com/integrations/generic/20131114/alert/69f3d1a0-05de-4b81-893c-c93497c12ca1/hackathon'
            payload = json.dumps({
                "message_type": "CRITICAL",
                "state_message": message
            })
            response = requests.post(url, payload)
            return {"success": "Message Sent"}

class Notification(Resource):

    def get(self):
        """
        Get a list of pending messages
        """
        session = create_session()
        response = session.get_queue_url(
            QueueName='MyChatQueue'
        )
        url = response['QueueUrl']
        if url:
            messages = session.receive_message(
                QueueUrl=url,
                AttributeNames=['All'],
                MaxNumberOfMessages=1,
                VisibilityTimeout=60,
                WaitTimeSeconds=5
            )
            if messages:
                return {"success": messages}
            else:
                return {"error": "Unable to retreive messages"}
        else:
            return {"error": "Unable to retreive queue"}

    def delete(self, message_id):
        """
        Delete Message id
        """
        session = create_session()
        pass

    def post(self):
        """
        create notification in SQS
        takes JSON
        [root@mori ~]# curl -X POST localhost:5000/notification -d '{"hello": "world"}'
        {
                "error": "Missing required fields"
        }
        [root@mori ~]# curl -X POST localhost:5000/notification -d '{"id": 1, "account_id": 1, "message": "hello"}'
        {
                "success": "Message queued"
        }
        """
        data = request.get_json(force=True)
        id = self.validate_number(data.get('id'))
        account_id = self.validate_number(data.get('account_id'))
        message = data.get('message')
        if id and account_id and message:
            message_json = json.dumps({
                "id": id,
                "account_id": account_id,
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


# Functions
def get_creds(account_id, provider_id):
    settings = ProviderSettings.query.filter_by(account_id = account_id, provider_id = provider_id).first()
    if settings:
        return settings.as_dict()

# Setup Routes
api.add_resource(Slack, '/slack')
api.add_resource(PagerDuty, '/pagerduty')
api.add_resource(HipChat, '/hipchat')
api.add_resource(VictorOps, '/victorops')

# Notification Routes
api.add_resource(Notification, '/notification')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
