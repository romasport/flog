from flask import g

from wtforms.validators import Email
from server import db, flask_bcrypt

from datetime import datetime
from itsdangerous import (
    JSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
SECRET_KEY = "szdvfgsdfvsdgsdtgtjkuykiuloi;ljhtgfsafas"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, info={'validators': Email()})
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = flask_bcrypt.generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.email

    def as_dict(self):
        jsondata = dict()
        for c in self.__table__.columns:
            jsondata.update({c.name: getattr(self, c.name)})
        return jsondata

    def verify_passwd(self, passwd):
        return flask_bcrypt.check_password_hash(self.password, passwd)

    def create_auth_token(self):
        s = Serializer(SECRET_KEY)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        token = bytes(token, encoding='utf-8')
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired as e:
            return None
        except BadSignature as e:
            return None

        user = User.query.get(data['id'])
        if user:
            return True
        else:
            return False

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=db.func.now())
    image = db.Column(db.String(300))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.user_id = g.user.id

    def __repr__(self):
        return '<Post %r>' % self.title

    def as_dict(self):
        jsondata = dict()
        for c in self.__table__.columns:
            if c.name == "created_at":
                value = datetime.strftime(
                    getattr(self, c.name), '%b %d %Y, %H:%M')
                jsondata.update({c.name: value})
            else:
                jsondata.update({c.name: getattr(self, c.name)})
        return jsondata