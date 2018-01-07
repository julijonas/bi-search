import re
import json
import sys

class ValidationException(Exception):
    def __init__(self, key, message):
        super(ValidationException, self).__init__()
        self._key = key
        self._message = message

    def __str__(self):
        return "Failed to validate %s: %s" % (self._key, self._message)


class JSONCast:
    def __init__(self):
        pass

    def __call__(self, value):
        return json.loads(value)

    def __str__(self):
        return "JSON"


raw_json = JSONCast()


class Schema:
    def __init__(self, cast, length=None, bounds=None, optional=False, nullable=False, schema=None, regex=None,
                 values=None, default=None, force_present=False):
        """
        Defines a Schema to validate an object against.
        :param cast: What to cast the object as. (Calls cast as a method, valid values are: int, str, any callable obj.)
        :param length: Length ranges. Tuple of (min, max) ranges inclusive. None = no limit. Eg: (3, None)
        :param bounds: Value ranges. Tuple of (min, max) values inclusive. None = no limit. Eg: (3, None)
        :param optional: Requires the object to be present. Used for validating dictionary key values.
        :param nullable: Allows None as a valid value of the object.
        :param schema: What to validate inner objects as. For lists, this is just another Schema. For dicts, this is a
            dict of schemas with keys corresponding to the inner keys of the object.
        :param regex: Regex for string types.
        :param values: Allowed values. Must be list or tuple.
        :param default: Object is set to this if it is not present in the puter object. Used for dicts.
        :param force_present: Value is set to None if it is not present in the object. Used for dicts.
            (Can't do this with default argument, because if default=None then there is no default value)
        """
        self._cast = cast
        self._length = length
        self._bounds = bounds
        self._optional = optional
        self._nullable = nullable
        self._schema = schema
        self._regex = re.compile(regex) if regex else None
        self._values = values
        self._default = default
        self._force_present = force_present

    def optional(self):
        return self._optional

    def default(self):
        return self._default

    def force_present(self):
        return self._force_present

    def validate(self, key, value):
        """
        Validates the value against this schema.
        :param key: What this value is. If value fails to pass validation, key will be printed out in the debug message.
        :param value: The value to validate.
        :return: The validated value.
        """

        if value is None:
            if not self._nullable:
                raise ValidationException(key, "Value cannot be null!")
            return None

        try:
            value = self._cast(value)
        except ValueError:
            raise ValidationException(key, "Failed to cast %s as %s" % (value, str(self._cast)))
        except Exception as e:
            sys.stderr.write("Exception occurred in the validation casting stage: " + str(e))
            raise e

        if self._length is not None:
            l = len(value)
            if self._length[0] is not None and l < self._length[0]:
                raise ValidationException(
                    key,
                    "Must not be shorter than %s. Received length: %s" % (self._length[0], l)
                )
            if self._length[1] is not None and l > self._length[1]:
                raise ValidationException(
                    key,
                    "Must not be longer than %s. Received length: %s" % (self._length[1], l)
                )

        if self._bounds is not None:
            if self._bounds[0] is not None and value < self._bounds[0]:
                raise ValidationException(
                    key,
                    "Must be at least %s. Received: %s" % (self._bounds[0], value)
                )
            if self._bounds[1] is not None and value > self._bounds[1]:
                raise ValidationException(
                    key,
                    "Must be at most %s. Received %s" % (self._bounds[1], value)
                )

        if self._values is not None and value not in self._values:
            raise ValidationException(
                key,
                "Value '%s' is not among the allowed values. Allowed values: %s" %
                (value, ", ".join(["'%s'" % v for v in self._values]))
            )

        if self._cast == list:
            return [self._schema.validate(key + ("[%i]" % i), item) for i, item in enumerate(value)]

        if self._cast == dict:
            validated = dict()
            for k, v in self._schema.items():
                if k not in value:
                    if not v.optional():
                        raise ValidationException(key + ("['%s']" % k), "Key is missing!")
                    if v.default() is not None:
                        validated[k] = v.default()
                    elif v.force_present():
                        validated[k] = None
                else:
                    validated[k] = v.validate(key + ("['%s']" % k), value[k])
            return validated

        if self._cast is raw_json:
            value = self._schema.validate(key, value)

        if self._regex and not re.fullmatch(self._regex, value):
            raise ValidationException(key, "Value does not match the required regular expression.")

        return value
