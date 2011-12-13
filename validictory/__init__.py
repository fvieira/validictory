#!/usr/bin/env python
import argparse
import copy
import json
import sys
from validictory.validator import SchemaValidator, ValidationError, SchemaError

__all__ = ['validate', 'SchemaValidator', 'ValidationError', 'SchemaError']
__version__ = '0.7.2'


def validate(data, schema, validator_cls=SchemaValidator,
             format_validators=None, required_by_default=True,
             blank_by_default=False):
    """
    Validates a parsed json document against the provided schema. If an
    error is found a :class:`ValidationError` is raised.

    If there is an issue in the schema a :class:`SchemaError` will be raised.

    :param data:  python data to validate
    :param schema: python dictionary representing the schema (see
        `schema format`_)
    :param validator_cls: optional validator class (default is
        :class:`SchemaValidator`)
    :param format_validators: optional dictionary of custom format validators
    :param required_by_default: defaults to True, set to False to make
        ``required`` schema attribute False by default.
    :param schemas: defaults to None, possible schemas to extend
    """
    v = validator_cls(format_validators, required_by_default, blank_by_default)
    return v.validate(data, schema)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Validate a JSON file")
    parser.add_argument("schemafile", type=argparse.FileType('r'),
                        help="JSON Schema file")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help="JSON file to validate")
    args = parser.parse_args()

    obj = json.load(args.infile)
    schema = json.load(args.schemafile)

    try:
        validate(obj, schema)
    except ValueError, e:
        raise SystemExit(e)
