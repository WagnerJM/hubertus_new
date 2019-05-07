from app.database import BaseMixin, db
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

    def json(self):
        return {
            "id": str(self.id),
            "reviername": self.reviername,
            "koordinaten": self.koordinaten,
            "ort": self.ort
        }
    
