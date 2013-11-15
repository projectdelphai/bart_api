import urllib.request
from lxml import etree

class BartApi():
  def __init__(self, api_key="MW9S-E7SL-26DU-VV8V"):
    self.api_key = api_key

  def parse_response(self,raw_xml):
    if isinstance(raw_xml, bytes):
      parsed_xml = etree.fromstring(raw_xml, parser=etree.XMLParser(encoding='utf-8'))
    else:
      parsed_xml = etree.parse(raw_xml)
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
    elevator_status = xml.xpath('bsa')[0].xpath('description')[0].text
    return elevator_status

  def get_stations(self):
    url = "http://api.bart.gov/api/stn.aspx?cmd=stns&key=%s" % (self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    return xml.find("stations").findall("station")

  def bsa(self, stn="ALL"):
    url = "http://api.bart.gov/api/stn.aspx?cmd=stninfo&orig=%s&key=%s" % (stn,self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    return xml.find(".//description").text

  def station_info(self, station):
    url = "http://api.bart.gov/api/stn.aspx?cmd=stninfo&orig=%s&key=%s" % (station,self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    return xml.find(".//station")

  def station_access(self, station, legend="1"):
    url = "http://api.bart.gov/api/stn.aspx?cmd=stnaccess&orig=%s&key=%s&l=%s" % (station,self.api_key,legend)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    return xml

  def etd(self, station="ALL", platform=None, direction=None):
    if station == "ALL":
      url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=ALL&key=%s" % (self.api_key)
    elif platform is None:
      url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=%s&direction=%s&key=%s" % (station,direction,self.api_key)
    elif direction is None:
      url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=%s&platform=%s&key=%s" % (station,platform,self.api_key)
    else:
      url = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=%s&platform=%s&direction=%s&key=%s" % (station,platform,direction,self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    return xml.findall(".//etd")

  def routes(self, sched=None, date="today"):
    if sched is None:
      url = "http://api.bart.gov/api/route.aspx?cmd=routes&date=%s&key=%s" % (date,self.api_key)
    else:
      url = "http://api.bart.gov/api/route.aspx?cmd=routes&sched=%s&key=%s" % (sched,self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    return xml.findall(".//route")

  def route_info(self, route="all", sched=None, date="today"):
    if sched is None:
      url = "http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=%s&date=%s&key=%s" % (route,date,self.api_key)
    else:
      url = "http://api.bart.gov/api/route.aspx?cmd=routeinfo&route=%s&sched=%s&date=%s&key=%s" % (route,sched,date,self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    return xml.find(".//route")

  def get_item(self, item_name, xml):
    item_list = xml.findall(".//" + item_name)
    if len(item_list) == 1:
      return [item_list[0].text]
    else:
      list_of_items = []
      for entry in item_list:
          list_of_items.append(entry.text)
      return list_of_items

  def get_holidays(self):
    url = "http://api.bart.gov/api/route.aspx?cmd=holiday&key=%s" % (self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    raw_holidays = xml.findall(".//holiday")
    return raw_holidays

  def get_schedules(self):
    url = "http://api.bart.gov/api/route.aspx?cmd=scheds&key=%s" % (self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    raw_schedules = xml.findall(".//schedule")
    schedules = []
    for schedule in raw_schedules:
        id = schedule.get('id')
        effective_date = schedule.get('effectivedate')
        schedules.append([id, effective_date])
    return schedules

  def get_special_schedules(self, legend="1"):
    url = "http://api.bart.gov/api/stn.aspx?cmd=special&key=%s&l=%s" % (self.api_key,legend)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    return xml
  
  def get_station_schedule(self, station):
    url = "http://api.bart.gov/api/stn.aspx?cmd=stnsched&orig=%s&key=%s" % (station,self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    raw_schedules = xml.findall('.//item')
    schedule_list = []
    for item in raw_schedules:
        schedule_dict = { "line" : item.get('line'), "train_head_station" : item.get('trainHeadStation'), "orig_time" : item.get('origTime'), "dest_time" : item.get('destTime'), "train_idx" : item.get('trainIdx'), "bikeflag" : item.get('bikeflag') }
        schedule_list.append(schedule_dict)
    return schedule_list

  def get_route_schedule(self, sched='', date='today', legend="1"):
    if not sched=='':
      url = "http://api.bart.gov/api/stn.aspx?cmd=special&sched=%s&key=%s&l=%s" % (sched,self.api_key,legend)
    elif sched == '':
      url = "http://api.bart.gov/api/stn.aspx?cmd=special&date=%s&key=%s&l=%s" % (date,self.api_key,legend)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    raw_routes = xml.findall(".//train")
    trains = {}
    for train in raw_routes:
        stops = {}
        raw_stops = train.findall(".//stop")
        for stop in raw_stops:
            raw_dict = { "orig_time" : stop.get("origTime"), "bikeflags" : stop.get("bikeflag") }
            stops[stop.get("station")] = raw_dict
        trains[train.get("index")] = stops
    return trains

  def get_fare(self, orig, dest):
    url = "http://api.bart.gov/api/stn.aspx?cmd=fare&orig=%s&dest=%s&key=%s" % (orig,dest,self.api_key)
    raw_response = urllib.request.urlopen(url)
    xml = self.parse_response(raw_response)
    raw_fare = xml.find(".//trip")
    fare_dict = { "fare" : raw_fare.find("fare").text, "clipper_fare" : raw_fare.find(".//clipper").text }
    return fare_dict
