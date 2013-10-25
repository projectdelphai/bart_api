import unittest
from unittest.mock import patch, Mock
from bart_api import BartApi
import os

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
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected=51
    actual = self.bart.number_of_trains()
    self.assertEqual(expected, actual)
  
  @patch('bart_api.urllib.request.urlopen')
  def test_number_of_trains(self,mock_urlopen):
    a = Mock()
    with open('bart_api/test/mocks/elev.xml') as f:
      raw_xml = f.read().encode('utf-8')
    mock_urlopen.return_value = raw_xml
    expected=" Attention passengers: All elevators are in service. Thank You. "
    actual = self.bart.elevator_status()
    self.assertEqual(expected, actual)

if __name__ == '__main__':
  unittest.main()
