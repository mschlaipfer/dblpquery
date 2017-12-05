from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.dialects.postgresql import \
    ARRAY, INTEGER, INT4RANGE, VARCHAR

from tables import *

engine = create_engine("postgresql://cavuser:cavuser@localhost:5432/cav_dblp")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

from lxml import etree

from StringIO import StringIO
#context = etree.iterparse(open('cav.xml', 'r').read())
cav_xml = open('cav.xml', 'r').read()
context = etree.iterparse(StringIO(cav_xml), tag='inproceedings')

for action, elem in context:
  author_names = map(lambda x: etree.tostring(x, method='text', encoding="UTF-8").strip(), elem.xpath('author'))
  pages = etree.tostring(elem.xpath('pages')[0], method='text', encoding="UTF-8").strip().split('-')

  publication = Publication(
    title=etree.tostring(elem.xpath('title')[0], method='text', encoding="UTF-8").strip(),
    #pages=INT4RANGE(int(pages[0]), int(pages[1])),
    year=int(etree.tostring(elem.xpath('year')[0], method='text', encoding="UTF-8").strip())
  )
  session.add(publication)
  session.commit()

  for author_name in author_names:
    # check if author already inserted
    q = session.query(Author).filter_by(name=author_name)
    author = q.first()
    if not(author):
      author = Author(name=author_name)
      session.add(author)
    author.publications.append(publication)
    session.commit()

