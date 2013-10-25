import urllib.request
from lxml import etree

class BartApi():
  def __init__(self, api_key="MW9S-E7SL-26DU-VV8V"):
    self.api_key = api_key

  def parse_response(self,raw_xml):
    parsed_xml = etree.fromstring(raw_xml, parser=etree.XMLParser(encoding='utf-8'))
    return parsed_xml

  def number_of_trains(self):
    url = "http://api.bart.gov/api/bsa.aspx?cmd=count&key=%s" % (self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    train_count = xml.xpath('traincount')[0].text
    return train_count

  def elevator_status(self):
    url = "http://api.bart.gov/api/bsa.aspx?cmd=elev&key=%s" % (self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    train_count = xml.xpath('bsa')[0].xpath('description')[0].text
    return train_count

