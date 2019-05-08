from app.database import BaseMixin, db
from app.serializer import ma
from app.api.user.models import User
from sqlalchemy.dialects.postgresql import JSON

class Revier(BaseMixin, db.Model):
    __tablename__ = 'reviere'

    revierID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))
    reviername = db.Column(db.String)
    koordinaten = db.Column(JSON)
    ort = db.Column(db.String)

    def __init__(self, reviername, ort):
        self.reviername = reviername
        self.ort = ort


class RevierSchema(ma.ModelSchema):
    class Meta:
        model = Revier