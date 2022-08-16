import sqlalchemy as sqla
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):

    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=60), unique=True)


class Book(Base):

    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=100), unique=True)
    publisher_id = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref='books')


class Shop(Base):

    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), unique=True)


class Stock(Base):

    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('shop.id'), nullable=False)

    book = relationship(Book, backref='stocks')
    shop = relationship(Shop, backref='stocks')


class Sale(Base):

    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    date_sale = Column(sqla.Date, nullable=False)
    count = Column(Integer, nullable=False)
    stock_id = Column(Integer, ForeignKey('stock.id'), nullable=False)

    stock = relationship(Stock, backref='sales')


def create_table(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
