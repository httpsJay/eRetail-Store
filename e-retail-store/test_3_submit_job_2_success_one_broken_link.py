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


    def test_submit_successful_bad_link(self):
        """ Successful job submit with incorrect image link """
        payload = json.dumps({
            "count": 2,
            "visits": [
                {
                    "store_id": "S00339218",
                    "image_url": [
                                "https://www.gstatic.com/webp/galleryy/2.jpg",  # incorrect link
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
        self.assertEqual(unicode, type(r.json['job_id']))  # Should return a job id
        self.assertEqual(r.status_code, 201)  # Should return status 201

        msg = "STATUS Check - <Success> - link|job success|status failed"
        table = [[str(msg)]]
        output = tabulate(table, tablefmt='grid')
        print(output)
        print(r.json)
        print(r.status_code)
        print("")


if __name__ == '__main__':
    unittest.main()