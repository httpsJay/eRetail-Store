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

    def test_submit_fail_count_n_visit_mismatch(self):
        """ Incorrect job submit, count is not equal to visits """
        payload = json.dumps({
            "count": 5,
            "visits": [
                {
                    "store_id": "S00339218",
                    "image_url": [
                                "https://www.gstatic.com/webp/gallery/2.jpg",
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02T00:00:53"
                },
                {
                    "store_id": "S01408764",
                    "image_url": [
                                "https://www.gstatic.com/webp/gallery/3.jpg"
                    ],
                    "visit_time": "2020-09-02T00:00:56"
                }
            ]
        })
        r = self.app.post('http://localhost:5000/api/submit',
                          headers={"Content-Type": "application/json"}, data=payload)
        # Should return an error message
        self.assertEqual(unicode, type(r.json['error']))
        self.assertEqual(r.status_code, 400)  # Should return status 201

        msg = "STATUS Check - <Fail> - count!=len(visit)"
        table = [[str(msg)]]
        output = tabulate(table, tablefmt='grid')
        print(output)
        print(r.json)
        print(r.status_code)
        print("")



if __name__ == '__main__':
    unittest.main()