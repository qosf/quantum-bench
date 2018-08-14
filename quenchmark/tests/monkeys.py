"""
Monkey classes to patch the PyGithub functionality
with unittest.mock in the tests.
"""

class MonkeyGithub():
    search_users = lambda self, x: [MonkeyUser()]

class MonkeyUser():
    get_repo = lambda self, y: MonkeyRepo()

class MonkeyRepo():
    get_commits = lambda self: list(range(10))
    @property
    def created_at(self, *args):
         return ValueError # raising error to ensure override in actual tests
    get_license = lambda self: MonkeyContentFile()

class MonkeyContentFile():
    @property
    def license(self):
        return MonkeyLicense()

class MonkeyLicense():
    @property
    def spdx_id(self):
        return ValueError # raising error to ensure override in actual tests

