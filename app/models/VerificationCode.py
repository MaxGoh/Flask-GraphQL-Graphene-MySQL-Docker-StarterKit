import datetime
import random

from app import db


class VerificationCode(db.Model):
    __tablename__ = "verification_code"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    verification_code = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.verification_code = self.generate_verification_code()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def is_valid(self):
        time_diff = datetime.datetime.now() - self.created_at
        if time_diff < datetime.timedelta(minutes=1):
            return True

        return False

    @staticmethod
    def generate_verification_code():
        return random.randint(1000, 9999)
