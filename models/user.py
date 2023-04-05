from sqlalchemy import Column, Integer, String
from models.base import Base
from models.modelmixin import ModelMixin

class User(Base, ModelMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)