import json
from datetime import  datetime
from sqlalchemy import Column, Integer, Unicode, Boolean, UnicodeText, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property

# dictated by sql-alchemy
Base =declarative_base()

# use to find out food is fruit to veg.
DIET_MAP = {
    'banana': 'fruit',
    'orange': 'fruit',
    'apple': 'fruit',
    'strawberry': 'fruit',
    'celery': 'veg',
    'carrot': 'veg',
    'cucumber': 'veg',
    'beetroot': 'veg'
}

class Company(Base):
    __tablename__ = 'company'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(Unicode(80), unique=True, nullable=False)

    def __init__(self, index=None, company=None):
        self.id = index
        self.name = company

class Person(Base, SerializerMixin):

    __tablename__ = 'person'
    __table_args__ = {'extend_existing': True}

    _id = Column('_id', Unicode(32),primary_key=True, autoincrement=False)
    index = Column(Integer, nullable=False)
    guid = Column(Unicode(64), unique=True, nullable=False)
    has_died = Column(Boolean, default=False)
    balance = Column(Unicode(255), nullable=True)
    picture = Column(Unicode(255), nullable=True)
    age = Column(Integer, nullable=True)
    eyeColor = Column(Unicode(32), nullable=True)
    name = Column(Unicode(255), nullable=True)
    gender = Column(Unicode(10), nullable=True)
    company_id = Column(Integer,nullable=True,)
    email = Column(Unicode(255), nullable=True)
    phone = Column(Unicode(255), nullable=True)
    address = Column(Unicode(255), nullable=True)
    about = Column(UnicodeText(500), nullable=True)
    registered =  Column(DateTime, nullable=True)
    _tags = Column('tags', Unicode(255), nullable=True, default='[]', server_default='[]')
    _friends = Column('friends',Unicode(500), nullable=True, default='[]', server_default='[]')
    greeting = Column(Unicode(255), nullable=True)
    _favourite_food = Column('favourite_food',Unicode(255), nullable=True, default='[]', server_default='[]')

    def __init__(self,
                 _id=None,
                 index=None,
                 guid=None,
                 has_died=False,
                 balance='0',
                 picture=None,
                 age=None,
                 eyeColor=None,
                 name=None,
                 gender=None,
                 company_id=None,
                 email=None,
                 phone=None,
                 address=None,
                 about=None,
                 registered=None,
                 tags =None,
                 friends=None,
                 greeting=None,
                 favouriteFood=None
                 ):

        self._id = str(_id)
        self.index = index
        self.name = name
        self.guid = guid
        self.gender = gender
        self.has_died = has_died
        self.balance = balance
        self.picture = picture
        self.age = age
        self.eyeColor = eyeColor
        self.company_id = company_id
        self.email = email
        self.phone = phone
        self.address = address
        self.about = about
        self.registered = datetime.strptime(registered, "%Y-%m-%dT%H:%M:%S %z") if registered is not None else None
        self.tags = tags
        self.friends = friends
        self.greeting = greeting
        self.favourite_food = favouriteFood

    @hybrid_property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, tags):
        self._tags = json.dumps(tags)

    @hybrid_property
    def friends(self):
        return json.loads(self._friends)

    @friends.setter
    def friends(self, friends):
        self._friends = json.dumps(friends)

    @hybrid_property
    def favourite_food(self):
        return json.loads(self._favourite_food)

    @favourite_food.setter
    def favourite_food(self, favourite_food):
        self._favourite_food = json.dumps(favourite_food)

    def _veges(self):
        return [food for food in self.favourite_food if DIET_MAP.get( food,'') == 'veg']

    def _fruits(self):
        return [food for food in self.favourite_food if DIET_MAP.get( food,'') == 'fruit']

    def get_diet(self):
        return {
            'vegetables': self._veges(),
            'fruits': self._fruits(),
            'username':self.name,
            'age': self.age
         }

    def to_dict_full_info(self):
        return self.to_dict(rules=('-_tags', '-_friends', '-_favourite_food', 'tags', 'friends', 'favourite_food'))

    def get_common_friends_indexes(self, other_person):

        self_friends = set(map(lambda f: f.get('index', None),self.friends))
        other_friends = set(map(lambda f: f.get('index', None),other_person.friends))

        return list(self_friends.intersection(other_friends))

