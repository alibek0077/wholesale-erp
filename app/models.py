from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from .database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String, unique=True)

    password = Column(String)


class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    category = Column(String)

    quantity = Column(Integer)


class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    phone = Column(String)

    email = Column(String)


class WarehouseItem(Base):

    __tablename__ = "warehouse_items"

    id = Column(Integer, primary_key=True, index=True)

    product = Column(String)

    location = Column(String)

    stock = Column(Integer)