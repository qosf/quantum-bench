"""
Monkey classes to patch the PyGithub functionality
with unittest.mock in the tests.
"""

class MonkeyGithub():
    search_users = lambda self, x: [MonkeyUser()]

class MonkeyRepo():
    get_commits = lambda self: list(range(10))
    created_at = property(lambda self, *args: 1/0)
    get_license = lambda self: MonkeyContentFile()
    get_stats_contributors = lambda self: 1/0
    get_stats_code_frequency = lambda self: 1/0

class MonkeyUser():
    get_repo = lambda self, y: MonkeyRepo()
    login = property(lambda self: 'Peter Shor')
    weeks = property(lambda self: StatsContributor())

class MonkeyContentFile():
    license = property(lambda self: MonkeyLicense())

class MonkeyLicense():
    spdx_id = property(lambda self: 1/0)

class MonkeyStatsContributor():
    author = property(lambda self: MonkeyUser())
    weeks = property(lambda self: [MonkeyWeeks() for i in range(5)])

class MonkeyWeeks(MonkeyStatsContributor):
    a = property(lambda self: 1/0)
    d = property(lambda self: 1/0)
    c = property(lambda self: 1/0)

class MonkeyStatsCodeFrequency():
    additions = property(lambda self: 1/0)
    deletions = property(lambda self: 1/0)
