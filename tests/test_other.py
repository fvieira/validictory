from unittest import TestCase

import validictory

class TestSchemaErrors(TestCase):

    valid_desc = { "description": "My Description for My Schema" }
    invalid_desc = { "description": 1233 }
    valid_title = { "title":"My Title for My Schema" }
    invalid_title = { "title": 1233 }
    valid_attribute = { "type" : "string" }
    invalid_attribute = { "tipe" : "string" }
    # doesn't matter what this is
    data = "whatever"

    def test_description_pass(self):
        try:
            validictory.validate(self.data, self.valid_desc)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_description_fail(self):
        self.assertRaises(ValueError, validictory.validate, self.data,
                          self.invalid_desc)

    def test_title_pass(self):
        try:
            validictory.validate(self.data, self.valid_title)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_title_fail(self):
        self.assertRaises(ValueError, validictory.validate, self.data,
                          self.invalid_title)

    def test_attribute_pass(self):
        try:
            validictory.validate(self.data, self.valid_attribute)
        except ValueError, e:
            self.fail("Unexpected failure: %s" % e)

    def test_attribute_fail(self):
        self.assertRaises(ValueError, validictory.validate, self.data,
                          self.invalid_attribute)

class TestUnimplementedWarning(TestCase):
    no_warn_schema = {"type": "object"}
    warn_schema = {"extends":"person"}
    data = {}

    def test_no_warn(self):
        import warnings
        with warnings.catch_warnings(record=True) as w:
            validictory.validate(self.data, self.no_warn_schema)
            assert len(w) == 0

    def test_warn(self):
        import warnings
        with warnings.catch_warnings(record=True) as w:
            validictory.validate(self.data, self.warn_schema)
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
