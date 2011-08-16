import json
import logging
import validictory.schemas
from mock import patch, Mock
from StringIO import StringIO
from unittest import TestCase
from validictory import SchemaError

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

SCHEMA_3 = {
    "type": "object",
    "extends": ["schema2", "schema3"],
    }

SCHEMA_4 = {
    "extends": "foo",
    "items":[
        {"type":"string", "extends":"bar"},
        {"type":"object", "extends":"baz",
         "properties":{
                "bar":{
                    "items":[
                        "schema_one",
                        "schema_two",
                        ]
                    }
                }
         }
        ]
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

    def test_find_two_schemas(self):
        schemas = validictory.schemas.find_schemas(SCHEMA_3)
        self.assertIn("schema2", schemas)
        self.assertIn("schema3", schemas)

    def test_find_all_schemas(self):
        schemas = validictory.schemas.find_schemas(SCHEMA_4)
        for schema in ["foo", "bar", "baz", "schema_one", "schema_two"]:
            self.assertIn(schema, schemas)

    @patch("validictory.schemas.load_schemas")
    def test_circular_dependency_detection(self, mock):
        mock.return_value = {
            "schema1": SCHEMA_3,
            "schema2": SCHEMA_2,
            "schema3": {}
            }
        with self.assertRaises(SchemaError):
            validictory.schemas.load("foo")
