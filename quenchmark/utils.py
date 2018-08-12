"""
Implements utilities and helper functions.
"""

import subprocess


class classproperty(object):
    """
    Implement the property interface for class methods.
    """

    def __init__(self, method):
        self.method = method

    def __get__(self, obj, arg):
        return self.method(arg)


def run(args, encoding='ascii'):
    child = subprocess.Popen(
        [str(arg) for arg in args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = child.communicate()
    code = child.returncode

    return stdout.decode(encoding), stderr.decode(encoding), code
