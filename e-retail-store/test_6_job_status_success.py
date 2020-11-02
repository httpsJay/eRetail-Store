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


    def test_job_status_successful(self):
        """ Status of a Successful job"""
        r = self.app.get('http://localhost:5000/api/status?jobid=efc746a4-194d-11eb-8dda-000c29c626fa')    #This jobid will be dynamic

        msg = "STATUS Check - <Success>"
        table = [[str(msg)]]
        output = tabulate(table, tablefmt='grid')
        print(output)
        print(r.json)
        print(r.status_code)
        print("")
        self.assertEqual(unicode, type(r.json['status']))  # Should return a status
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
