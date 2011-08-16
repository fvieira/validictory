import logging
import validictory.schemas
from mock import patch, Mock
from StringIO import StringIO
from unittest import TestCase

import json

JSON_FOO = """
{
    "type": "object",
    "properties": {
        "foo": {
            "required": true
        }
    }
}
"""

SCHEMA_1 = {
    "type": "object",
    "properties": {
        "foo": {
            "required": True,
            },
        },
    }

SCHEMA_2 = {
    "type": "object",
    "extends": "schema1",
    }


class LoadingSchemasTest(TestCase):

    @patch("os.walk")
    @patch('__builtin__.open')
    def test_load_empty_folder(self, open_mock, walk_mock):
        walk_mock.return_value = [("src", [], ["file.xml"])]
        schemas = validictory.schemas.load("src")
        self.assertEquals(len(schemas), 0)

    @patch("os.walk")
    @patch('__builtin__.open')
    def test_load_one_schema(self, open_mock, walk_mock):
        walk_mock.return_value = [("src", [], ["file.json"])]
        open_mock.return_value = StringIO(JSON_FOO)
        schemas = validictory.schemas.load("src")
        self.assertIn("src/file.json", schemas)

    def test_find_no_schemas(self):
        schemas = validictory.schemas.find_schemas(SCHEMA_1)
        self.assertEquals(len(schemas), 0)

    def test_find_one_schemas(self):
        schemas = validictory.schemas.find_schemas(SCHEMA_2)
        self.assertIn("schema1", schemas)



