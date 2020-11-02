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


    def test_job_status_fail_jobid_wrong(self):
        """ Status of a non existing job"""
        r = self.app.get('http://localhost:5000/api/status?jobid=3004')
        self.assertEqual(r.status_code, 400)

        msg = "STATUS Check - <Fail - Wrong jobid>"
        table = [[str(msg)]]
        output = tabulate(table, tablefmt='grid')
        print(output)
        print(r.json)
        print(r.status_code)
        print("")


if __name__ == '__main__':
    unittest.main()