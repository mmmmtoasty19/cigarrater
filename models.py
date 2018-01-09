import datetime
import hashlib
import requests

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash


from peewee import *


DATABASE = SqliteDatabase('cigar.db')  



# Code for pythonanywhere
# DATABASE = MySQLDatabase('mmmmtoasty19$CigarRater',
#     host="mmmmtoasty19.mysql.pythonanywhere-services.com",
#     port=3306,
#     user="mmmmtoasty19",
#     password="j76Q$l5hmTRymlgEmQc4G@%52",
# )


class User(UserMixin, Model):
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
    
    @classmethod
    def create_user(cls, username, email, password, first_name, last_name, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin,
                    first_name=first_name,
                    last_name=last_name)
        except IntegrityError:
            raise ValueError("User already exists")

    def avatar(self, size):
        """used to get Gravatar avatar."""
        return 'http://www.gravatar.com/avatar/{}?d=mm&s={}'.format(hashlib.md5(self.email.encode('utf-8')).hexdigest(), size)

    def total_cigar_rating(self):
        return Rate.select(fn.Count(Rate.cigar)).where(Rate.user==self).scalar()

    def unique_cigar_rating(self):
        return Rate.select(fn.Count(fn.Distinct(Rate.cigar))).where(Rate.user==self).scalar()


class Cigar(Model):
    """Model to create a new cigar into the database"""
    cigar_name = CharField(unique=True)
    brand = CharField()
    body = CharField()
    wrapper = CharField()
    binder = CharField()
    filler = CharField()
    orgin = CharField()
    avg_rating = FloatField()

    class Meta:
        database = DATABASE

    @classmethod
    def create_cigar(cls, cigar_name, brand, body, wrapper, binder, filler, orgin, avg_rating=0):
        try:  #attempt to create a new cigar, if name exisits will throught error
            with DATABASE.transaction():  
                cls.create(
                    cigar_name=cigar_name,
                    brand=brand,
                    body=body,
                    wrapper=wrapper,
                    binder=binder,
                    filler=filler,
                    orgin=orgin,
                    avg_rating=avg_rating
                )
        except IntegrityError:
            raise ValueError("Cigar already exists")

    def average(self):
        """returns average rating for cigar"""
        query = Rate.select().where(Rate.cigar == self)
        avg_rate = []
        for rating in query:
            avg_rate.append(rating.rating)
        avg = round(sum(avg_rate)/float(len(avg_rate)),2)
        self.avg_rating = avg
        self.save()
    
    def rating_amount(self):
        return Rate.select().where(Rate.cigar == self)



class Rate(Model):
    """Model for storing cigar user ratings"""
    user = ForeignKeyField(User)
    cigar = ForeignKeyField(Cigar)
    size = CharField()
    comment = TextField()
    rating = IntegerField()
    location = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)
    

    def get_name(self,venue_id):
        """returns name of venue based on ID"""
        params = {
        "client_id": 'LRYLMHH5W1GEZYJWGM2XWIBAEOM0HLY5QY0BXJ5UIWFRB0LL',
        "client_secret" : 'D141PZTEO5QQ40OZZ2OZELACVKDXWKUHRZLVY5EJ5JCWZ12K',
        "v": 20180103
        }
        url = 'https://api.foursquare.com/v2/venues/' + venue_id
        search_req = requests.get(url=url, params=params)
        search_json = search_req.json()
        # print(search_json['response']['venue']['name'])
        return search_json['response']['venue']['name']
        

   

    


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Cigar, Rate], safe=True)
    DATABASE.close()
