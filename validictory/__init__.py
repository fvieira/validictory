#!/usr/bin/env python
import copy

from validictory.validator import SchemaValidator, ValidationError, SchemaError

__all__ = ['validate', 'load_extends', 'SchemaValidator',
           'ValidationError', 'SchemaError']
__version__ = '0.7.0'


def validate(data, schema, validator_cls=SchemaValidator,
             format_validators=None, required_by_default=True):
    '''
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
    '''
    v = validator_cls(format_validators, required_by_default)
    return v.validate(data, schema)

def load_extends(schema, schemas):
    newschema = copy.deepcopy(schema)
    _load_schemas(newschema, schemas)
    return newschema

def _load_schemas(schema, schemas, last_key=None):
    """
    Extend the schema using a list of possible schemas.

    Recursively searches the schema dictionary, replacing the extends
    keyword with the referenced schema.

    Currently updates dictionaries, which isn't correct behavior.
    Also only supports one layer of extension
    """
    allowed = ["properties", "additionalProperties"]

    for k, v in schema.iteritems():
        # Check for schema extension
        if k == "extends" and last_key not in allowed:
            if schemas.has_key(v):
                del schema["extends"]
                schema.update(schemas[v])
            else:
                raise ValidationError("Schemea %s could not be found" % v)
        # Recurse into nested schemas
        elif isinstance(v, dict):
            _load_schemas(v, schemas, last_key=k)
        elif isinstance(v, list):
            for s in v:
                if isinstance(v, dict):
                    _load_schemas(s, schemas)

if __name__ == '__main__':
    import sys
    import json
    if len(sys.argv) == 2:
        if sys.argv[1] == "--help":
            raise SystemExit("%s SCHEMAFILE [INFILE]" % (sys.argv[0],))
        schemafile = open(sys.argv[1], 'rb')
        infile = sys.stdin
    elif len(sys.argv) == 3:
        schemafile = open(sys.argv[1], 'rb')
        infile = open(sys.argv[2], 'rb')
    else:
        raise SystemExit("%s SCHEMAFILE [INFILE]" % (sys.argv[0],))
    try:
        obj = json.load(infile)
        schema = json.load(schemafile)
        validate(obj, schema)
    except ValueError, e:
        raise SystemExit(e)
