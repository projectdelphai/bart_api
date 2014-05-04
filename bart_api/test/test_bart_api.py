import unittest
try:
  from unittest.mock import patch, Mock
except ImportError:
  from mock import patch, Mock

from bart_api import BartApi
from lxml import etree

class TestBartApi(unittest.TestCase):

  def setUp(self):
    self.bart = BartApi()
  
  def test_api_key(self):
    expected = "MW9S-E7SL-26DU-VV8V"
    actual = self.bart.api_key
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_number_of_trains(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/train_count.xml') as f:
      raw_xml = f.read()
    mock_urlopen.return_value = raw_xml.encode('utf-8')
    expected="51"
    actual = self.bart.number_of_trains()
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_elevator_status(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/elev.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected=" Attention passengers: All elevators are in service. Thank You. "
    actual = self.bart.elevator_status()
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_get_stations(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/station_list.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "West Oakland"
    stations = self.bart.get_stations()
    actual = stations[1].get("name")
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_bsa_all(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/bsa.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected2 = "No delays reported."
    actual2 = self.bart.bsa()
    self.assertEqual(expected2, actual2)
  
  @patch('bart_api.urlopen')
  def test_bsa_specific(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/bsa_woak.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "No delays reported."
    actual = self.bart.bsa("WOAK")
    self.assertEqual(expected, actual)
  
  @patch('bart_api.urlopen')
  def test_station_info(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/station_info.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "94110"
    station_info = self.bart.station_info("24TH")
    actual = station_info.get("zipcode")
    self.assertEqual(expected, actual)
  
  @patch('bart_api.urlopen')
  def test_station_access(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/station_access.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = None
    station_info = self.bart.station_access("12TH", "1")
    actual = station_info.get("car_share")
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_etd(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/etd.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "2"
    station_info = self.bart.etd("RICH", "2", "s")
    actual = station_info[0].get("estimates")[0].get("platform")
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_routes(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/routes.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "1"
    station_info = self.bart.routes("26", "today")
    actual = station_info[0].get("number")
    self.assertEqual(expected, actual)
  
  @patch('bart_api.urlopen')
  def test_route_infO(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/route_info.xml') as f:
      raw_xml = f.read().encode('utf-8')
      mock_urlopen.return_value = raw_xml
    expected = "BALB"
    station_info = self.bart.route_info("6", "26", "today")
    actual = station_info.get('config')[1]
    self.assertEqual(expected, actual)
  
  @patch('bart_api.urlopen')
  def test_get_holidays(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/holiday.xml') as f:
      raw_xml = f.read().encode('utf-8')
      mock_urlopen.return_value = raw_xml
    expected = "Presidents' Day"
    actual = self.bart.get_holidays()[1].get('name')
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_get_schedules(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/schedules.xml') as f:
      raw_xml = f.read().encode('utf-8')
      mock_urlopen.return_value = raw_xml
    expected = "26"
    actual = self.bart.get_schedules()[0].get('id')
    self.assertEqual(expected, actual)
  
  @patch('bart_api.urlopen')
  def test_get_special_schedules(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/special_schedules.xml') as f:
      raw_xml = f.read().encode('utf-8')
      mock_urlopen.return_value = raw_xml
    expected = "DUBL"
    actual = self.bart.get_special_schedules().get('orig')
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_get_station_schedule(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/station_schedule.xml') as f:
      raw_xml = f.read().encode('utf-8')
      mock_urlopen.return_value = raw_xml
    expected = "ROUTE 7"
    actual = self.bart.get_station_schedule("12th")[0].get("line")
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_get_route_schedule(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/route_schedule.xml') as f:
      raw_xml = f.read().encode('utf-8')
      mock_urlopen.return_value = raw_xml
    expected = "6:13 AM"
    actual = self.bart.get_route_schedule("6","today").get("1").get("DALY").get("orig_time")
    self.assertEqual(expected, actual)

  @patch('bart_api.urlopen')
  def test_get_fare(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/fare.xml') as f:
      raw_xml = f.read().encode('utf-8')
      mock_urlopen.return_value = raw_xml
    expected = "3.15"
    actual = self.bart.get_fare("12th", "embr").get("fare")
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
