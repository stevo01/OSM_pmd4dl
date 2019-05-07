'''
Created on 24.12.2017

@author: stevo
'''
import unittest
from utils.osmchart import osmchart_atlas
from utils.Helper import HandleDate


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
