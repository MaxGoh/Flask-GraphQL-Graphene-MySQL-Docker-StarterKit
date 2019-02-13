import datetime

from passlib.context import CryptContext
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from flask import current_app as app

from app import db
from app.models.VerificationCode import VerificationCode


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Integer, nullable=False, default=1)
    is_verified = db.Column(db.Integer, nullable=False, default=0)
    last_logged_in = db.Column(db.DateTime, default=datetime.datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def __init__(self, email, password):
        self.email = email
        self._hash_password(password)

    def save(self):
        """ Shorthand method to update User object """
        db.session.add(self)
        db.session.commit()

    def _verify_user(self, verification_code):
        verification_code_object = db.session.query(VerificationCode).\
            filter(VerificationCode.user_id == self.id).\
            filter(VerificationCode.verification_code == verification_code).\
            scalar()

        if verification_code_object and verification_code_object.is_valid():
            self.is_verified = 1
            self.save()
            return True

        return False

    def _hash_password(self, password):
        userctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
        self.password = userctx.hash(password)

    def _verify_password(self, password):
        userctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
        return userctx.verify(password, self.password)

    def _generate_access_token(self):
        with app.app_context():
            expires = datetime.timedelta(days=365)
            access_token = create_access_token(self.id, expires_delta=expires)
            # access_token = create_access_token(self.id)
            return access_token

    def _generate_refresh_token(self):
        with app.app_context():
            refresh_token = create_refresh_token(self.id)
            return refresh_token
