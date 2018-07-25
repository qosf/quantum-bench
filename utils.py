"""
Implements utilities and helper functions.
"""


class classproperty(object):
    """
    Implement the property interface for class methods.
    """

    def __init__(self, method):
        self.method = method

    def __get__(self, obj, arg):
        return self.method(arg)
