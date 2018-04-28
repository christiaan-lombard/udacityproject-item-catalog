from sqlalchemy import (Column, Integer, String, Text, ForeignKey,
                        DateTime, func, desc)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from flask import url_for
from passlib.apps import custom_app_context as pwd_context
from werkzeug.exceptions import HTTPException
import datetime

Base = declarative_base()


"""Application database models"""
__author__ = "Christiaan Lombard <base1.christiaan@gmail.com>"


class ModelNotFoundError(HTTPException):
    code = 404
    description = "The requested resource could not be found"


class Model(Base):
    """ Base database model class with active record features.

    Inspired by absent1706/sqlalchemy-mixins,
    https://github.com/absent1706/sqlalchemy-mixins

    """

    __abstract__ = True
    _session = None

    @classmethod
    def use_session(cls, session):
        """Set the class-bound db session"""
        cls._session = session

    @classmethod
    def get_session(cls):
        """Get the class-bound db session"""
        if cls._session is not None:
            return cls._session
        else:
            raise RuntimeError('Session not set.')

    @classmethod
    def make(cls, **kwargs):
        """Make a new instance and fill from keyword args"""
        return cls().fill(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        """Make new instance, fill and persist the instance"""
        return cls().fill(**kwargs).save()

    @classmethod
    def query(cls):
        """Create a new query"""
        return cls._session.query(cls)

    @classmethod
    def find(cls, key):
        """Find record by primary key"""
        return cls.query().get(key)

    @classmethod
    def find_or_fail(cls, key):
        """Find record by primary key or raise error if not found"""
        model = cls.find(key)
        if model is None:
            msg = "{} with primary key {} does not exist."\
                    .format(cls.__name__, key)
            raise ModelNotFoundError(msg)
        return model

    def fill(self, **kwargs):
        """Fill instance attributes from keyword arguments"""
        for name in kwargs.keys():
            setattr(self, name, kwargs[name])
        return self

    def delete(self):
        """Execute delete on the current instance"""
        s = self.get_session()
        s.delete(self)
        s.commit()

    def save(self):
        """Execute update/create on the current instance"""
        s = self.get_session()
        s.add(self)
        s.commit()
        return self


class User(Model):
    """Database model representing a user"""

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    picture = Column(String)
    password_hash = Column(String(256), nullable=False)

    @classmethod
    def find_by_email(cls, email):
        return cls.query() \
                  .filter(User.email == email) \
                  .first()

    def set_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def serialize(self):
        """Return User data in serializeable format"""
        return {
            'email': self.email,
            'name': self.name,
            'id': self.id
        }


class Category(Model):
    """Database model representing a category"""

    __tablename__ = 'category'

    slug = Column(String(20), primary_key=True)
    title = Column(String(100), nullable=False)
    # description = Column(Text)

    items = relationship("Item", back_populates="category")

    @property
    def serialize(self):
        """Return Category data in serializeable format"""
        return {
            'slug': self.slug,
            'title': self.title,
        }

    @classmethod
    def all(cls):
        return cls.query() \
                  .order_by(Category.title) \
                  .all()


class Item(Model):
    """Database model representing an item"""

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    picture = Column(String(256))
    description = Column(Text())

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    category_slug = Column(String(20), ForeignKey('category.slug'))
    category = relationship("Category", back_populates="items")

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    @classmethod
    def latest(cls, limit):
        return cls.query() \
                  .order_by(desc(Item.created_at)) \
                  .limit(limit) \
                  .all()

    @classmethod
    def for_user(cls, user_id):
        return cls.query() \
                  .order_by(desc(Item.created_at)) \
                  .filter(Item.user_id == user_id) \
                  .order_by(desc(Item.created_at)) \
                  .all()

    def set_picture_upload(self, filename):
        self.picture = 'UPLOAD:' + filename

    def set_picture_link(self, link):
        self.picture = 'LINK:' + link

    def get_picture_info(self):
        if not self.picture:
            return ('NONE', '')
        parts = self.picture.split(':')
        t = parts.pop(0)
        return (t, ":".join(parts))

    def get_picture_url(self):
        t, url = self.get_picture_info()
        if t == 'UPLOAD':
            return url_for('uploaded_file', filename=url)
        else:
            return url

    def has_picture(self):
        return bool(self.picture)

    @property
    def serialize(self):
        """Return Item data in serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'picture': self.picture,
            'description': self.description,
            'category_slug': self.category_slug}


def init_db():
    """Initialize the database and session"""

    # create the database tables as defined
    engine = create_engine('sqlite:///catalog.db', echo=True)
    Base.metadata.create_all(engine)

    # create a session
    Base.metadata.bind = engine
    BaseSession = sessionmaker(bind=engine)
    session = BaseSession()

    # set the shared Model session
    Model.use_session(session)

    return (engine, session)


if __name__ == '__main__':
    init_db()
