'''
Created on 24.12.2017

@author: stevo
'''
import re
import unittest
from utils.osmchart import osmchart_atlas
from datetime import datetime


def HandleDate(date):
    # 2018-03-12T05:30:30.801Z
    # 20171012-1120"

    a = re.match("[\d]{8}-[\d]{4}", date)

    if a is not None:
        b = a.group()
        datetime_object = datetime.strptime(b, '%Y%m%d-%H%M')
        b = datetime_object.isoformat('T')+'Z'

        return b

    return date


class Test(unittest.TestCase):

    def test_Atlas(self):
        a = osmchart_atlas('./../sample/OSM-OpenCPN2-KAP-Adria-20171122-1907.json')
        self.assertEqual(a.name, "./../sample/OSM-OpenCPN2-KAP-Adria-20171122-1907.json")
        pass

    def test_Date(self):
        date1 = "2018-03-12T05:30:30.801Z"
        date2 = "20171012-1120"

        res = HandleDate(date1)
        self.assertEqual(res, date1)
        res = HandleDate(date2)
        self.assertEqual(res, "2017-10-12T11:20:00Z")
