import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

from peewee import *


DATABASE = SqliteDatabase('cigar.db')


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
    
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


class Cigar(Model):
    """Model to create a new cigar into the database"""
    cigar_name = CharField(unique=True)
    brand = CharField()
    body = CharField()
    wrapper = CharField()
    binder = CharField()
    filler = CharField()
    orgin = CharField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_cigar(cls, cigar_name, brand, body, wrapper, binder, filler, orgin):
        try:  #attempt to create a new cigar, if name exisits will throught error
            with DATABASE.transaction():  
                cls.create(
                    cigar_name=cigar_name,
                    brand=brand,
                    body=body,
                    wrapper=wrapper,
                    binder=binder,
                    filler=filler,
                    orgin=orgin
                )
        except IntegrityError:
            raise ValueError("Cigar already exists")



class Rate(Model):
    """Model for storing cigar user ratings"""
    user = ForeignKeyField(User)
    cigar = ForeignKeyField(Cigar)
    size = CharField()
    comment = TextField()
    rating = IntegerField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)
    
   

    


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Cigar, Rate], safe=True)
    DATABASE.close()
