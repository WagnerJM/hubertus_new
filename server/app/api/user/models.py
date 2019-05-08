import bcrypt
from app.database import BaseMixin, db
from sqlalchemy import and_

class User(BaseMixin, db.Model):
    __tablename__ = 'users'

    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    _password = db.Column(db.Binary(60))
    email = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    

    free_user = db.Column(db.Boolean, default=True)
    pro_user = db.Column(db.Boolean, default=False)

    #profile = db.relationship('UserProfile', backref='User', lazy=False)


    def __init__(self, username, password, email):
        self.username = username
        self._password = self.hash_pw(password.encode('utf-8'))
        self.email = email

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


    def json(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "is_admin": self.is_admin,
            "is_active": self.is_active,
            "free_user": self.free_user,
            "pro_user": self.pro_user,
            "email": self.email
        }
class UserProfile(BaseMixin, db.Model):
    __tablename__ = 'userProfile'

    userProfileID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))
    vorname = db.Column(db.String)
    nachname = db.Column(db.String)
    
    def __init__(self,vorname, nachname):
        self.vorname = vorname
        self.nachname = nachname

    @classmethod
    def get_profile(cls, user_id):
        return cls.query.filter_by(_and(self.is_active == True, self.user_id == user_id )).first()

    def json(self):
        return {
            "id": str(self.id),
            "vorname": self.vorname,
            "nachname": self.nachname
        }
