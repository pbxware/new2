# coding=utf-8
from decimal import Decimal
import string


def validation_simple(value, obj=None):
    """
    Validates that at least one character has been entered.
    Not change is made to the value.
    """
    if len(value) >= 1:
        return True, value
    else:
        return False, value


def validation_integer(value, obj=None):
    """
    Validates that value is an integer number.
    No change is made to the value
    """
    try:
        int(value)
        return True, value
    except:
        return False, value


def validation_yesno(value, obj=None):
    """
    Validates that yes or no is entered.
    Converts the yes or no to capitalized version
    """
    if string.upper(value) in ["YES", "NO"]:
        return True, string.capitalize(value)
    else:
        return False, value


def validation_decimal(value, obj=None):
    """
    Validates that the number can be converted to a decimal
    """
    try:
        Decimal(value)
        return True, value
    except:
        return False, value


def import_validator(validator_name):
    return globals().get(validator_name)


def validate_attribute_value(attribute, value, obj):
    return import_validator(attribute.validation)(value, obj)
