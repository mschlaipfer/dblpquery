from sqlalchemy import *
from sqlalchemy.orm import *

from tables import *

engine = create_engine("postgresql://cavuser:cavuser@localhost:5432/cav_dblp")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_name(author_id):
  return engine.execute(text("SELECT name FROM authors WHERE id=:id;"), id=author_id).fetchall()[0]

import operator

def coauthors_within_5y_span():
  print "Number of coauthors within 5 year span"
  for l in range(1989, 2010):
    print l, "to", (l+5)
    co_authors_in_range = dict()
    for author in session.query(Author):
      # I'm sure there is a much better way to do this using SQL and SQL Alchemy
      co_authors_in_range[author.id] = len(engine.execute(text("""
        SELECT DISTINCT ON (limited_to_author.author_id)
        pub.year, limited_to_author.author_id, limited_to_author.publication_id
        FROM publications pub
        INNER JOIN (
          SELECT pa.publication_id, pa.author_id
          FROM publication_authors pa
          WHERE pa.publication_id IN (
            (SELECT publication_id
            FROM publication_authors
            WHERE author_id=:id)
          )) limited_to_author
        ON pub.id=limited_to_author.publication_id
        WHERE year>=:lower AND year<:upper; 
      """), id = author.id, lower=l, upper=(l+5)).fetchall())
    m = sorted(co_authors_in_range.iteritems(), key=operator.itemgetter(1))[-3:]
    m.reverse()
    for i in range(3):
      print (i+1), ")", get_name(m[i][0]), "with", m[i][1]

def publications_within_5y_span():
  print "Number of publications within 5 year span"
  for l in range(1989, 2010):
    print l, "to", (l+5)
    publications_in_range = dict()
    for author in session.query(Author):
      # I'm sure there is a much better way to do this using SQL and SQL Alchemy
      publications_in_range[author.id] = len(engine.execute(text("""
        SELECT
        pub.year, limited_to_author.author_id, limited_to_author.publication_id
        FROM publications pub
        INNER JOIN (
          (SELECT author_id, publication_id
          FROM publication_authors
          WHERE author_id=:id)
          ) limited_to_author
        ON pub.id=limited_to_author.publication_id
        WHERE year>=:lower AND year<:upper; 
      """), id = author.id, lower=l, upper=(l+5)).fetchall())
    m = sorted(publications_in_range.iteritems(), key=operator.itemgetter(1))[-3:]
    m.reverse()
    for i in range(3):
      print (i+1), ")", get_name(m[i][0]), "with", m[i][1]


def single_author_papers():
  print "Single author papers"
  publications = dict()
  for author in session.query(Author):
    # I'm sure there is a much better way to do this using SQL and SQL Alchemy
    publications[author.id] = len(engine.execute(text("""
      SELECT pub.author_id, pub.publication_id
      FROM publication_authors pub
      INNER JOIN (
        SELECT publication_id
        FROM publication_authors
        GROUP BY publication_id
        HAVING COUNT(author_id) = 1
      ) single_author_papers
      ON pub.publication_id = single_author_papers.publication_id
      WHERE author_id=:id;
    """), id = author.id).fetchall())
  m = sorted(publications.iteritems(), key=operator.itemgetter(1))[-3:]
  m.reverse()
  for i in range(3):
    print (i+1), ")", get_name(m[i][0]), "with", m[i][1]

single_author_papers()
print ""
coauthors_within_5y_span()
print ""
publications_within_5y_span()

