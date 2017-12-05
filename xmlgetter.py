import urllib2

print '<?xml version="1.0"?>'
print '<dblp>'

# TODO pass as argument
f = urllib2.urlopen('http://www.informatik.uni-trier.de/~ley/db/conf/cav/')

import lxml.html
cav_overview = lxml.html.fromstring(f.read())
cav_urls = cav_overview.xpath("//ul/li[@class='entry editor']//div[@class='head']/a")

cav_urls = map(lambda y: y.attrib['href'], filter(lambda x: x.attrib['href'].endswith(".html"), cav_urls))
# Add Automatic Verification Methods for Finite State Systems 1989: Grenoble, France
# by hand. First CAV under different name.
cav_urls.append("http://www.informatik.uni-trier.de/~ley/db/conf/avmfss/avmfss1989.html")
for cav_url in cav_urls:
  f = urllib2.urlopen(cav_url)

  raw_string = lxml.html.fromstring(f.read())

  raw_html = raw_string.xpath("//ul/li")
  for item in raw_html:
    if ('id' in item.attrib.keys() and
      'class' in item.attrib.keys() and
      item.attrib['class'] != "entry editor" and 
      item.attrib['class'] == "entry inproceedings"):
      # don't overload dblp with requests
      import time
      time.sleep(1)

      dblp_key = item.attrib['id']
      inproceedings_url = 'http://dblp.uni-trier.de/rec/bibtex/' + dblp_key + '.xml'
      f = urllib2.urlopen(inproceedings_url)
      from lxml import etree
      entry = etree.tostring(etree.parse(f).xpath("/dblp/inproceedings")[0])
      print entry
    elif ('id' in item.attrib.keys() and
      'class' in item.attrib.keys() and 
      item.attrib['class'] != "entry editor" and 
      item.attrib['class'] != "entry inproceedings"):
      # somewhere not entry inproceedings?
      print "Not 'entry inproceedings' for", item.attrib['id']

print '</dblp>'
