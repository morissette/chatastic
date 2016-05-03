from application import db, manager
from werkzeug import generate_password_hash, check_password_hash

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))

    def __init__(self, email):
        self.email = email


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

class ProviderSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'))
    token = db.Column(db.String(500))
    channel = db.Column(db.String(500))
    botname = db.Column(db.String(500))

    def __init__(self, account_id, provider_id, token, channel, botname):
        self.account_id = account_id
        self.provider_id = provider_id
        self.token = token
        self.channel = channel
        self.botname = botname

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

