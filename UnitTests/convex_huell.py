'''
Created on 24.12.2017

@author: stevo
'''
import unittest
from utils.convex_huell import convexhull


class Test(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testName(self):
        # Example: convex hull of a 10-by-10 grid.
        vh = convexhull([(i // 10, i % 10) for i in range(100)])
        self.assertEqual(vh, [(0, 0), (9, 0), (9, 9), (0, 9)])

    def test_EastWest001(self):
        # Example: convex hull of a 10-by-10 grid.
        vh = convexhull([(-170, -10),
                         (-170, 10),
                         (-190, 10),
                         (-190, -10)
                         ])

        for entry in vh:
            print("[{},{}],".format(entry[0], entry[1]))
        print("[{},{}]".format(vh[0][0], vh[0][1]))

        self.assertEqual(vh, [(-190, -10), (-170, -10), (-170, 10), (-190, 10)])

    def test_EastWest002(self):
        # Example: convex hull of a 10-by-10 grid.
        vh = convexhull([(-170, -10),
                         (-170, 10),
                         (10, 10),
                         (10, -10)
                         ])

        for entry in vh:
            print("[{},{}],".format(entry[0], entry[1]))
        print("[{},{}]".format(vh[0][0], vh[0][1]))

        self.assertEqual(vh, [(-170, -10), (10, -10), (10, 10), (-170, 10)])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
