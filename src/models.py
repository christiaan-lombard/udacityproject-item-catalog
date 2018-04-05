from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class Model(Base):
    """ Base database model class with active record features.

    Inspired by absent1706/sqlalchemy-mixins, https://github.com/absent1706/sqlalchemy-mixins

    """

    __abstract__ = True

    def __init__(self):
        self.session = self.get_session()

    @classmethod
    def use_session(cls, session):
        cls._session = session

    @classmethod
    def get_session(cls):
        if cls._session is not None:
            return cls._session
        else:
            raise RuntimeError('Cant get session.'
                                 'Call Model.use_session() to set a session reference')

    @classmethod
    def make(cls, **kwargs):
        return cls().fill(**kwargs)

    @classmethod
    def query(cls):
        return cls._session.query(cls)

    @classmethod
    def find(cls, key):
        return cls.query().get(key)

    def fill(self, **kwargs):
        for name in kwargs.keys():
            setattr(self, name, kwargs[name])
        return self

    def delete(self):
        self.session.delete(self)
        self.session.commit()

    def save(self):
        self.session.add(self)
        self.session.commit()


class User(Model):

    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(128), nullable = False)
    email = Column(String(256), nullable = False)
    password_hash = Column(String(256), nullable = False)

    def setPassword(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verifyPassword(self, password):
        return pwd_context.verify(password, self.password_hash)

    @property
    def serialize(self):
	    """Return User data in serializeable format"""
	    return {
            'email' : self.email,
            'name' : self.name,
            'id' : self.id,
	    }

class Category(Model):

    __tablename__ = 'category'

    slug = Column(String(20), primary_key = True)
    title = Column(String(100), nullable = False)
    description = Column(Text)

    items = relationship("Item", back_populates="category")

    @property
    def serialize(self):
        """Return Category data in serializeable format"""
        return {
            'name' : self.name,
            'picture' : self.picture,
            'price' : self.price,
            'description' : self.description
        }

class Item(Model):

    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable = False)
    picture = Column(String(256))
    description = Column(Text())
    price = Column(String(64))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    category_slug = Column(String(20), ForeignKey('category.slug'))
    category = relationship("Category", back_populates="items")

    @property
    def serialize(self):
        """Return Item data in serializeable format"""
        return {
            'name' : self.name,
            'picture' : self.picture,
            'price' : self.price,
            'description' : self.description
        }


def init_db():

    # create the database tables as defined
    engine = create_engine('sqlite:///catalog.db')
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