import bcrypt
from app.database import BaseMixin, db
from app.serializer import ma

from sqlalchemy import and_
from sqlalchemy.dialects.postgresql import JSON

class User(BaseMixin, db.Model):
    __tablename__ = 'users'

    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    _password = db.Column(db.Binary(60))
    email = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    vorname = db.Column(db.String, default="Placeholder")
    nachname = db.Column(db.String, default="Placeholder")
    adresse = db.Column(JSON)
    
    datenschutz = db.Column(db.Boolean, default=False)
    free_user = db.Column(db.Boolean, default=True)
    pro_user = db.Column(db.Boolean, default=False)
    email_verification = db.Column(db.Boolean, default=False)
    

    def __init__(self, username, password, email, datenschutz):
        self.username = username
        self._password = self.hash_pw(password.encode('utf-8'))
        self.email = email
        self.datenschutz = datenschutz

    def hash_pw(self, password):
        return bcrypt.hashpw(password, bcrypt.gensalt(16))
    
    def check_pw(self, password, hashed_pw):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def check4admin(cls):
        if cls.query.filter_by(is_admin=True).first():
            return True
        return False


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "username",
            "is_admin",
            "is_active",
            "free_user",
            "pro_user",
            "email",
            "vorname",
            "nachname",
            "adresse"
        )
