from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api.revier.models import Revier, RevierSchema
from app.api.user.models import User 

class RevierListApi(Resource):
    @jwt_required
    def get(self):
        user = User.find_by_id(get_jwt_identity())
        reviere = Revier.query.filter_by(user_id=user.userID).all()
        revier_schema = RevierSchema(many=True)

        return revier_schema.dump(reviere).data, 200
    @jwt_required
    def post(self):
        pass

class RevierApi(Resource):
    @jwt_required
    def put(self, revier_id):



        