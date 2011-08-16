import validictory
import logging

from unittest import TestCase

class TestExtends(TestCase):

    schema1 = None

    schema2 = {
        "type": "object",
        "extends": "schema1",
        }

    schemas = {
        "schema1": schema1,
        "schema2": schema2,
        }

    def test_bad_data(self):
        with self.assertRaises(ValueError):
            schema = validictory.load_extends(self.schema2, self.schemas)
            logging.debug(schema)
            validictory.validate({}, schema)

    def test_good_data(self):
        try:
            schema = validictory.load_extends(self.schema2, self.schemas)
            validictory.validate({"foo": 1}, schema)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_extends_schema_not_found(self):
        with self.assertRaises(ValueError):
            validictory.validate({"foo": 1}, self.schema2)
