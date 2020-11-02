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


    def test_submit_fail_req_field_miss(self):
        """Incorrect job submit fields are missing """
        payload = json.dumps({
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

        msg = "STATUS Check - <Fail> - fields missing"
        table = [[str(msg)]]
        output = tabulate(table, tablefmt='grid')
        print(output)
        print(r.json)
        print(r.status_code)
        print("")


if __name__ == '__main__':
    unittest.main()