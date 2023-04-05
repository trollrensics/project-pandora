from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from models.base import Base
from models.modelmixin import ModelMixin

class Movie(Base, ModelMixin):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sharelink = Column(String(255), nullable=False)
    tiktoklink = Column(String(255), nullable=True)
    videolink = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)

    __table_args__ = (UniqueConstraint('sharelink'),)

    views = relationship('View', backref='movie', lazy=True)
    shares = relationship('Share', backref='movie', lazy=True)
    likes = relationship('Like', backref='movie', lazy=True)

