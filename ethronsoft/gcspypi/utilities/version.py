from __future__ import division
from ethronsoft.gcspypi.exceptions import InvalidParameter
import functools


def complete_version(v):
    """adds missing '0' to a version that has less than 3 components
    
    Arguments:
        v {str} -- The version to update
    
    Returns:
        str -- The modified version
    """

    tokens = [x for x in v.split(".") if x.strip()]
    if len(tokens) > 3:
        raise InvalidParameter("Invalid Version")
    for i in range(3 - len(tokens)):
        tokens.append("0")
    return ".".join(tokens)
