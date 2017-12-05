from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.dialects.postgresql import \
    ARRAY, INTEGER, INT4RANGE, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# many-to-many reference table for publications - authors
publication_authors = Table('publication_authors', Base.metadata,
  Column('publication_id', INTEGER, ForeignKey('publications.id')),
  Column('author_id', INTEGER, ForeignKey('authors.id'))
)

class Publication(Base):
  __tablename__ = 'publications'

  id = Column(INTEGER, primary_key=True)
  title = Column(VARCHAR)
  #pages = Column(INT4RANGE)
  year = Column(INTEGER)
  authors = Column(INTEGER, ForeignKey('authors.id'))

  #author = relationship("Author", backref=backref('publications', order_by=id))
  # many to many Publications<->Authors
  authors = relationship('Author', secondary=publication_authors, backref='publications')

  def __repr__(self):
    return "<Publication(title='%s')>" % (self.title)

class Author(Base):
  __tablename__ = 'authors'

  id = Column(INTEGER, primary_key=True)
  name = Column(VARCHAR, unique=True)

  def __repr__(self):
    return "<Author(name='%s')>" % (self.name)
