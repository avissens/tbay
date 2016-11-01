from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

#creating an item model
from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

#creating a user model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
#adding relations between User and Item and Bid (one-to-many)
    items = relationship("Item", backref="owner")
    bids = relationship("Bid", backref="bidder")

#creating a table many-to-many relationship between items and bids
item_bid_table = Table('item_bid_association', Base.metadata,
    Column('item_id', Integer, ForeignKey('items.id')),
    Column('bid_id', Integer, ForeignKey('bids.id'))
)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
#one-to-many relationship with User
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
#creating a bid model
class Bid(Base):
    __tablename__ = "bids"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
#one-to-many relationship with User
    bid_id = Column(Integer, ForeignKey('users.id'), nullable=False)
#many-to-many relationship with Item
    bids = relationship("Bid", secondary="item_bid_association",
                            backref="items")
    
Base.metadata.create_all(engine)