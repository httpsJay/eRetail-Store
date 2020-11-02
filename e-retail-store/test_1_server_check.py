"""
Test API endpoint
"""

import io
import os
import json
import unittest
from app import *
from tabulate import tabulate

class TestDataObjects(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.app = app.test_client()

    @ classmethod
    def tearDownClass(self):
        "random"
        print('### Tearing down the flask server ###')


    def test_server_check(self):
        """ server_checking"""
        r = self.app.get('http://localhost:5000/')
        self.assertEqual(r.status_code, 200)

        msg = "Server Check"
        table = [[str(msg)]]
        output = tabulate(table, tablefmt='grid')
        print(output)
        print(r.json)
        print(r.status_code)


if __name__ == '__main__':
    unittest.main()