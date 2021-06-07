from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from .base import Base
from .coin import Coin


class ActionRecommendation(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = "action_recommendation"
    id = Column(Integer, primary_key=True)
    trade_action = Column(String(8))
    price = Column(Float)
    datetime = Column(DateTime)
    margin = Column(Float)

    def __init__(self):
        self.datetime = datetime.utcnow()

    def info(self):
        return {"datetime": self.datetime.isoformat(), "price": self.price, "margin": self.margin, "trade_action": self.trade_action}
