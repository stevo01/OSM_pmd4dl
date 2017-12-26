'''
Created on 24.12.2017

@author: stevo
'''
import unittest
from utils.osmchart import osmchart_atlas


class Test(unittest.TestCase):


    def test_Atlas(self):
        a = osmchart_atlas('./../sample/OSM-OpenCPN2-KAP-Adria-20171122-1907.json')
        self.assertEqual(a.name,"./../sample/OSM-OpenCPN2-KAP-Adria-20171122-1907.json")
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()