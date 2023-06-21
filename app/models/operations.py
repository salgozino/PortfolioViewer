import os

from app.extensions import db

from sqlalchemy import Column, Date, Float, Integer, String
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine


secret_key = os.environ.get('SECRET_KEY')


class Operation(db.Model):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(255))
    entry_date = Column(Date)
    entry_price = Column(Float)
    size = Column(Float)
    broker = Column(String(255))
    type = Column(String(255))
    close_price = Column(Float)
    close_date = Column(Date)
    pnl = Column(Float)
    pnl_percentage = Column(Float)
    user = Column(EncryptedType(String, secret_key, AesEngine, 'pkcs5'), nullable=False)

    def __init__(self, ticker, entry_date, entry_price, size, broker, type, user,
                 close_price=None, close_date=None, pnl=None, pnl_percentage=None):
        self.ticker = ticker
        self.entry_date = entry_date
        self.entry_price = entry_price
        self.size = size
        self.broker = broker
        self.type = type
        self.close_price = close_price
        self.close_date = close_date
        self.pnl = pnl
        self.pnl_percentage = pnl_percentage
        self.user = user

    def __repr__(self):
        return f'<Operation {self.ticker} @ {self.entry_price} since {self.entry_date}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def close_trade(self, close_date, close_price, portfolio_value):
        self.close_date = close_date
        self.close_price = close_price

        # Calculate P&L
        pnl = (close_price - self.entry_price) * self.size
        self.pnl = pnl

        # Calculate P&L percentage
        pnl_percentage = (pnl / portfolio_value) * 100
        self.pnl_percentage = pnl_percentage

        # Save the updated trade
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
