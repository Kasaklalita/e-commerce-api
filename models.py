from sqlalchemy import Column, Integer, String, Boolean, Date, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    is_verified = Column(Boolean, default=False)
    join_date = Column(Date, default=datetime.utcnow)
    profile_picture = Column(String, nullable=False, default='user.jpg')
    businesses = relationship(
        'Business', back_populates='owner', cascade="all,delete")


class Business(Base):
    __tablename__ = "businesses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False, unique=True)
    city = Column(String(100), nullable=False, default='Unspecified')
    region = Column(String(100), nullable=False, default='Unspecified')
    description = Column(Text, nullable=True)
    logo = Column(String, nullable=False, default='business.jpg')
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship(
        'User', back_populates='businesses')
    products = relationship(
        'Product', back_populates='business', cascade="all,delete")


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    category = Column(String(30), index=True)
    original_price = Column(Float)
    percentage_discount = Column(Integer)
    offer_expiration_data = Column(Date, default=datetime.utcnow)
    product_image = Column(String(200), nullable=False,
                           default='product.jpg')
    business_id = Column(Integer, ForeignKey('businesses.id'))
    business = relationship('Business', back_populates='products')
