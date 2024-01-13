from sqlalchemy import Column, Integer, Float, String, String, Boolean, TIMESTAMP, Enum, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__= 'users'
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String,nullable=False, unique=True)
    display_name = Column(String, nullable=False, unique=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    location = Column(String)
    auctions = relationship('Auction', back_populates='user')
    bids = relationship("Bid", back_populates='bidder')
    

class ItemCategory(Base):
    __tablename__='item_categories'
    category_id = Column(Integer, nullable=False, primary_key=True)
    category_name = Column(String, nullable=False)
    auctions = relationship('Auction', back_populates='itemcategory')


class Auction(Base):
    __tablename__ = 'auctions'
    auction_id = Column(Integer, nullable=False, primary_key=True)
    item_name = Column(String, nullable=False)
    item_description = Column(String, nullable=False)
    item_category = Column(Integer, ForeignKey("item_categories.category_id", ondelete='CASCADE'), nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    current_bid = Column(Float, nullable=False, server_default=text('0.00'))
    reserve_status = Column(Enum("Reserve", "No Reserve", name="reserve_status_enum"), nullable=False, default='No Reserve')
    reserve_price = Column(Float, nullable=False, server_default=text('0.00'))
    auction_status = Column(Enum("Ongoing","Sold","Cancelled","Reserve price not met", name="auction_status_enum"), default="Ongoing")
    seller = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    user = relationship('User', back_populates='auctions')
    itemcategory = relationship('ItemCategory', back_populates='auctions')
    images = relationship('AuctionImages', back_populates='auction')
    bids = relationship("Bid", back_populates='auction')


class AuctionImages(Base):
    __tablename__='auction_images'
    image_id = Column(Integer, nullable=False, primary_key=True)
    image_description = Column(Integer, nullable=True)
    image_url = Column(String, nullable=False)
    auction_id = Column(Integer, ForeignKey("auctions.auction_id", ondelete='CASCADE'), nullable=True)
    auction = relationship('Auction', back_populates='images')


class Bid(Base):
    __tablename__='bids'
    bid_id = Column(Integer, nullable=False, primary_key=True)
    auction_id = Column(Integer, ForeignKey('auctions.auction_id', ondelete='CASCADE'), nullable=False)
    bidder_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    amount = Column(Float, nullable=False)
    auction = relationship('Auction', back_populates='bids')
    bidder = relationship("User", back_populates='bids')