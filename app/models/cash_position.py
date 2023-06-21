import os

from app.extensions import db
from sqlalchemy import Column, Date, Float, String
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine


secret_key = os.environ.get('SECRET_KEY')


class CashPosition(db.Model):
    __tablename__ = 'cash_positions'

    id = Column(db.Integer, primary_key=True)
    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)
    user = Column(EncryptedType(String, secret_key, AesEngine, 'pkcs5'))

    def __init__(self, date, value, user):
        self.date = date
        self.value = value
        self.user = user

    def __repr__(self):
        return f'<CashPosition {self.date} - {self.value}>'

    def save(self):
        db.session.add(self)
        db.session.commit()
