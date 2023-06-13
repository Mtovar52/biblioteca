from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data
from sqlalchemy import Text

books = Table(
    'books', meta_data,
    Column('id', Integer, primary_key=True),
    Column('title', String(255), nullable=False),
    Column('subtitle', String(255), nullable=False),
    Column('author', String(255), nullable=False),
    Column('category', String(255), nullable=False),
    Column('publisher', String(255), nullable=False),
    Column('publishedDate', String(255), nullable=False),
    Column('description', Text, nullable=False),
    Column('image', Text, nullable=False),
    Column('state', Integer, nullable=False)
    #Column('publication_date', DateTime, nullable=False)
)

users = Table(
    'users', meta_data,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('email', String(255), nullable=False),
    Column('password', String(255), nullable=False)
)

meta_data.create_all(engine)