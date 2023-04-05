from sqlalchemy import Column, Integer, DateTime, ForeignKey
from models.base import Base
from models.modelmixin import ModelMixin

class Like(Base, ModelMixin):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)

