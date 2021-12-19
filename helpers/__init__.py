"""
(ENV VARIABLE PICKER):
    Simple helper-methods meant for parsing application config settings from
    environmental variables.  The intention of this module is to make 'config.py'
    more readable.
"""

__all__ = ['_str', '_bool', '_int', '_float']

# SESSION : ENV VARIABLE PICKER
import os

__environment_prefix = "WOR_"


def __env(varname, default=None, type=str):
    """ Fetches an environmental variable and returns it's value as type.
    :param `str` varname: The non-prefixed variable name
    :param `object` default: Value to return if env var is not defined.
    :param `callable` type: A single-parameter function to use to convert
        the environmental variable's value to it's final python type.
    :return: An object representing whatever
    """
    value = os.getenv(__environment_prefix + varname)

    if value is None:
        return default

    return type(value)


_str = __env


def _bool(varname, default=None):
    """ Fetched the named environmental variable, and returns as a boolean.
    :param `str` varname: Non-prefixed environmental variable name.
    :param `bool` default: Value to return if varname is not defined.
    :return: A boolean representing the environmental variable.
    :rtype: bool
    """
    return __env(
        varname=varname,
        default=default,
        type=lambda x: x.lower() in ['1', 'true', 't'],
    )


def _int(varname, default=None):
    """ Fetches the named environmental variable, and returns as an integer.
    :param `str` varname: Non-prefixed environmental variable name.
    :param `int` default: Value to return if varname is not defined.
    :return: An int representing the environmental variable.
    :rtype: int
    """
    return __env(
        varname=varname,
        default=default,
        type=int
    )


def _float(varname, default=None):
    """ Fetches the named environmental variable, and returns as an float.
    :param `str` varname: Non-prefixed environmental variable name.
    :param `float` default: Value to return if varname is not defined.
    :return: A float representing the environmental variable.
    :rtype: float
    """
    return __env(
        varname=varname,
        default=default,
        type=float
    )
# END : ENV VARIABLE PICKER
