from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

#creating a user model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
#adding relations between User and Item and Bid (one-to-many)
    items = relationship("Item", backref="owner")
    bids = relationship("Bid", backref="bidder")

#creating an item model
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
#one-to-many relationship with User
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#one-to-many relationship with Bid
    bids = relationship("Bid", backref="auction_item")
    
#creating a bid model
class Bid(Base):
    __tablename__ = "bids"
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
#one-to-many relationship with User
    bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#one-to-many relationship with Item
    action_item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    
Base.metadata.create_all(engine)

#creating instances for User
user1 = User(username = "anna", password = "lalalala")
user2 = User()
user3 = User(username = "max", password = "lulululu")

#creating instances for Item
item1 = Item(name = "baseball", description = "red", start_time = "2016-11-1 12:50:00", owner_i = user1)

#creating instances for Bid
bid1 = Bid(price = "27.50", bidder_id = user2)
bid2 = Bid(price = "37.50", bidder_id = user3)

#add and commit all instances
session.add_all([user1, user2, user3, item1, bid1, bid2])
session.commit()