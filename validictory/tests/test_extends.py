import validictory

from unittest import TestCase

class TestExtends(TestCase):

    schema1 = {
        "type": "object",
        "properties": {
            "foo": {
                "required": True,
                }
            },
    }

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
            validictory.validate({}, self.schema2, schemas=self.schemas)

    def test_good_data(self):
        try:
            validictory.validate({"foo": 1}, self.schema2,
                                 schemas=self.schemas)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_extends_schema_not_found(self):
        with self.assertRaises(ValueError):
            validictory.validate({"foo": 1}, self.schema2)
