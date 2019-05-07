from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.revier.models import revier
from app.api.user.models import User 

class RevierListApi(Resource):
    def get(self):
        user = User.find_by_id(get_jwt_identity())

        