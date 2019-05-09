from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt, get_jwt_identity

from app.database import db
from app.utils import str2uuid
from app.security import TokenBlacklist
from app.api.user.models import User, UserSchema

class UserRegisterApi(Resource):
    def post(self):
        data = request.get_json()

        if User.find_by_username(data['username']):
            return {
                "msg": "Dieser Username ist leider bereits vergeben"
            }, 500
        
        user = User(
           username=data['username'],
           password=data['password'],
           email=data['email']
        )
        

        try:
            user.save()
            return {
                "msg": "User wurde angelegt"
            }, 201
        except:
            return {
                "msg": "Etwas ist beim Speichern des Users schief gelaufen, wenden Sie sich bitte an den Administrator unter {Email}"
            }, 500

class UserLoginApi(Resource):
    def post(self):
        data = request.get_json()
        user = User.find_by_username(data['username'])

        if user and user.check_pw(data['password'], user._password):
            token = create_access_token(identity=str(user.id), fresh=True)
            return {
                "username": user.username,
                "token": token
            }, 201
        else:
            return {
                "msg": "Username und/oder Passwort falsch."
            }, 401

class UserLogoutApi(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        token = TokenBlacklist(jti=jti)
        token.save()
        return {
            "msg": "Sie wurden erfolgreich ausgeloggt."
        }

class UserApi(Resource):
    @jwt_required
    def get(self):
        user = User.find_by_id(get_jwt_identity())
        user_schema = UserSchema()
        if not user or not user.is_active:
            return {
                "msg": "User konnte nicht gefunden werden."
            }
        else:
            return user_schema.dump(user).data
    
    @jwt_required
    def put(self):
        user = User.query.filter_by(id=get_jwt_identity())
        user.update(request.json)
       
        db.session.commit()

        us = UserSchema()

        return us.dump(user.first()).data
        
        