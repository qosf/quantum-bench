"""
Monkey classes to patch the PyGithub functionality
with unittest.mock in the tests.
"""

import datetime as dt

class MonkeyGithub():
    search_users = lambda self, x: [MonkeyUser()]

class MonkeyUser():
    get_repo = lambda self, y: YoungMonkeyRepo() # just passing the young repo as default

class YoungMonkeyRepo():
    get_commits = lambda self: list(range(10))
    @property
    def created_at(self, *args):
        return dt.datetime.now() - dt.timedelta(weeks=30)

class OldMonkeyRepo():
    get_commits = lambda self: list(range(10))
    @property
    def created_at(self, *args):
        return dt.datetime.now() - dt.timedelta(weeks=180)


