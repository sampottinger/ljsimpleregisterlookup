import collections
import copy
import unittest
import json
import os


import lj_error_scribe

from ljm_constants import ljmmm

EXPECTED_ERRORS = [
    {
        "error": 0,
        "string": "LJ_SUCCESS"
    },
    {
        "error": 200,
        "string": "LJME_WARNINGS_BEGIN",
        "description": "test01"
    },
    {
        "error": 399,
        "string": "LJME_WARNINGS_END",
        "description": "test02"
    },
    {
        "error": 201,
        "string": "LJME_FRAMES_OMITTED_DUE_TO_PACKET_SIZE",
        "description": "test03"
    }
]

ONE_TEST_ERROR = [({'string': 'LJ_SUCCESS', 'error': 0},)]
EXPECTED_ERRORS = list(zip(EXPECTED_ERRORS))

class LJErrorScribeTests(unittest.TestCase):

    def test_find_error_range_from_errors_gets_all_errors(self):
        errors = lj_error_scribe.find_error_range_from_errors(0, 399, EXPECTED_ERRORS)
        self.assertEqual(EXPECTED_ERRORS, errors)

    def test_find_error_range_from_errors_gets_one_error(self):
        errors = lj_error_scribe.find_error_range_from_errors(0, 0, EXPECTED_ERRORS)
        self.assertEqual(ONE_TEST_ERROR, errors)

if __name__ == "__main__":
    unittest.main()
