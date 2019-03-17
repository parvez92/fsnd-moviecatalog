#!/usr/bin/env python3

import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class UserDetails(Base):
    __tablename__ = 'userdetails'

    users_id = Column(Integer, primary_key=True)
    users_name = Column(String(50), nullable=False)
    users_email = Column(String(100), nullable=False)
    users_image = Column(String(250))


class MovieCategory(Base):
    __tablename__ = 'movie_category'

    id = Column(Integer, primary_key=True)
    genre = Column(String(50), nullable=False)
    users_id = Column(Integer, ForeignKey('userdetails.users_id'))
    user = relationship(UserDetails)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'genre': self.genre,
        }


class MovieDetails(Base):
    __tablename__ = 'movie_details'

    name = Column(String(70), nullable=False)
    description = Column(String(250))
    id = Column(Integer, primary_key=True)
    movie_category_id = Column(Integer, ForeignKey('movie_category.id'))
    moviecategory = relationship(MovieCategory)
    users_id = Column(Integer, ForeignKey('userdetails.users_id'))
    user = relationship(UserDetails)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'moviecategory': self.moviecategory.genre,
            'name': self.name,
            'description': self.description
        }

engine = create_engine('sqlite:///catalogformovies.db')
Base.metadata.create_all(engine)
