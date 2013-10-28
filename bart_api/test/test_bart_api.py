import unittest
from unittest.mock import patch, Mock
from bart_api import BartApi
from lxml import etree

class TestBartApi(unittest.TestCase):

  def setUp(self):
    self.bart = BartApi()
  
  def test_api_key(self):
    expected = "MW9S-E7SL-26DU-VV8V"
    actual = self.bart.api_key
    self.assertEqual(expected, actual)

  @patch('bart_api.urllib.request.urlopen')
  def test_number_of_trains(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/train_count.xml') as f:
      raw_xml = f.read()
    mock_urlopen.return_value = raw_xml.encode('utf-8')
    expected=str(51)
    actual = self.bart.number_of_trains()
    self.assertEqual(expected, actual)

  @patch('bart_api.urllib.request.urlopen')
  def test_elevator_status(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/elev.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected=" Attention passengers: All elevators are in service. Thank You. "
    actual = self.bart.elevator_status()
    self.assertEqual(expected, actual)

  @patch('bart_api.urllib.request.urlopen')
  def test_get_stations(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/station_list.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "West Oakland"
    stations = self.bart.get_stations()
    actual = stations[1].find("name").text
    self.assertEqual(expected, actual)

  @patch('bart_api.urllib.request.urlopen')
  def test_bsa_all(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/bsa.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected2 = "No delays reported."
    actual2 = self.bart.bsa()
    self.assertEqual(expected2, actual2)
  
  @patch('bart_api.urllib.request.urlopen')
  def test_bsa_specific(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/bsa_woak.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "No delays reported."
    actual = self.bart.bsa("WOAK")
    self.assertEqual(expected, actual)
  
  @patch('bart_api.urllib.request.urlopen')
  def test_station_info(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/station_info.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "94110"
    station_info = self.bart.station_info("24TH")
    actual = station_info.find(".//zipcode").text
    self.assertEqual(expected, actual)
  
  @patch('bart_api.urllib.request.urlopen')
  def test_station_access(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/station_access.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = " "
    station_info = self.bart.station_access("12TH", "1")
    actual = station_info.find(".//car_share").text
    self.assertEqual(expected, actual)

  @patch('bart_api.urllib.request.urlopen')
  def test_etd(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/etd.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "2"
    station_info = self.bart.etd("RICH", "2", "s")
    actual = station_info[0].find(".//platform").text
    self.assertEqual(expected, actual)

  @patch('bart_api.urllib.request.urlopen')
  def test_routes(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/routes.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "1"
    station_info = self.bart.routes("26", "today")
    actual = station_info[0].find(".//number").text
    self.assertEqual(expected, actual)

  @patch('bart_api.urllib.request.urlopen')
  def test_route_info(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/route_info.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected = "BALB"
    station_info = self.bart.route_info("6", "26", "today")
    actual = station_info.findall(".//station")[1].text
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
