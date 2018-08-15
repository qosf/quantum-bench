import mock
import datetime as dt
from unittest.mock import patch

import pytest
import github
import numpy as np

from quenchmark.collectors.meta import MetaCollector
import monkeys

@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_init():
    """
    Tests the instantiation of a Repository object.
    """
    repo = MetaCollector('TestRepoOwner', 'TestRepoName')

@patch('monkeys.MonkeyRepo')
@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_commit_count(repo_mock):
    """
    Testing if number of commits is accurately retrieved.
    """
    repo_mock.return_value.get_commits.return_value = list(range(10))
    assert MetaCollector('TestRepoOwner', 'TestRepoName').commit_count == 10

    repo_mock.return_value.get_commits.return_value = list(range(20))
    assert MetaCollector('TestRepoOwner', 'TestRepoName').commit_count == 20


@patch('monkeys.MonkeyRepo')
@patch('github.Github.search_users', mock.MagicMock(return_value=[monkeys.MonkeyUser()]))
@patch('github.Github.__init__', mock.MagicMock(return_value=None))
def test_is_young(repo_mock):
    """
    Testing if a project is young (< 1 year).
    """
    repo_mock.return_value.created_at = dt.datetime.now() - dt.timedelta(weeks=30)
    assert MetaCollector('TestRepoOwner', 'TestRepoName').is_young == True

    repo_mock.return_value.created_at = dt.datetime.now() - dt.timedelta(weeks=180)
    assert MetaCollector('TestRepoOwner', 'TestRepoName').is_young == False


@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_has_recent_commits():
    """
    Testing if a project had at least 20 commits in the past year.
    """
    pass # TODO: needs to be tested

@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_contributor_count():
    """
    Testing how many contributor a project has.
    """
    pass # TODO: needs to be tested

@patch('monkeys.MonkeyLicense')
@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_osi_license(license_mock):
    """
    Testing if the repo's license is OSI-approved.
    """
    license_mock.return_value.spdx_id = 'MPL-2.0'
    assert MetaCollector('TestRepoOwner', 'TestRepoName').osi_license == True
    license_mock.return_value.spdx_id = 'Proprietary'
    assert MetaCollector('TestRepoOwner', 'TestRepoName').osi_license == False
    license_mock.return_value.spdx_id = 'GPL-2.0'
    assert MetaCollector('TestRepoOwner', 'TestRepoName').osi_license == True

@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_has_xtrnl_issues_or_prs():
    """
    Testing if the repo has external Issues or PRs.
    """
    pass #TODO

@patch('monkeys.MonkeyWeeks')
@patch('monkeys.MonkeyStatsContributor')
@patch('monkeys.MonkeyRepo')
@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_get_contributors(repo_mock, stats_mock, weeks_mock):
    """
    Getting the list of contributors for a project.
    """
    repo_mock.return_value.get_stats_contributors.return_value = [monkeys.MonkeyStatsContributor() for i in range(5)]
    stats_mock.return_value.weeks = [monkeys.MonkeyWeeks() for i in range(5)]
    stats_mock.return_value.author= monkeys.MonkeyUser()
    weeks_mock.return_value.a = 100
    weeks_mock.return_value.d = -100
    weeks_mock.return_value.c = 20
    contributor_list = [{'additions': 500, 'commits': 100, 'deletions': -500, 'name': 'Peter Shor'},
            {'additions': 500, 'commits': 100, 'deletions': -500, 'name': 'Peter Shor'},
            {'additions': 500, 'commits': 100, 'deletions': -500, 'name': 'Peter Shor'},
            {'additions': 500, 'commits': 100, 'deletions': -500, 'name': 'Peter Shor'},
            {'additions': 500, 'commits': 100, 'deletions': -500, 'name': 'Peter Shor'}]
    assert MetaCollector('TestRepoOwner', 'TestRepoName').get_contributors() == contributor_list

@patch('monkeys.MonkeyStatsCodeFrequency')
@patch('monkeys.MonkeyRepo')
@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_get_total_adds_and_dels(repo_mock, stats_mock):
    """
    Getting the total number of additions and deletions.
    """
    repo_mock.return_value.get_stats_code_frequency.return_value = [monkeys.MonkeyStatsCodeFrequency() for i in range(10)]
    stats_mock.return_value.additions = 10000
    stats_mock.return_value.deletions = -10000
    assert MetaCollector('TestRepoOwner', 'TestRepoName').get_total_adds_and_dels() == {'additions': 100000, 'deletions': -100000}

    repo_mock.return_value.get_stats_code_frequency.return_value = [monkeys.MonkeyStatsCodeFrequency() for i in range(100)]
    stats_mock.return_value.additions = 20
    stats_mock.return_value.deletions = -200
    assert MetaCollector('TestRepoOwner', 'TestRepoName').get_total_adds_and_dels() == {'additions': 2000, 'deletions': -20000}

@patch('monkeys.MonkeyWeeks')
@patch('monkeys.MonkeyStatsCodeFrequency')
@patch('monkeys.MonkeyRepo')
@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_core_developers(repo_mock, stats_mock, weeks_mock):
    """
    Getting a list of core developers.
    """

    repo_mock.return_value.get_stats_contributors.return_value = [monkeys.MonkeyStatsContributor() for i in range(5)]
    stats_mock.return_value.weeks = [monkeys.MonkeyWeeks() for i in range(5)]
    stats_mock.return_value.author= monkeys.MonkeyUser()

    repo_mock.return_value.get_stats_code_frequency.return_value = [monkeys.MonkeyStatsCodeFrequency() for i in range(100)]
    stats_mock.return_value.additions = 10
    stats_mock.return_value.deletions = -10

    weeks_mock.return_value.a = 100
    weeks_mock.return_value.d = -100
    weeks_mock.return_value.c = 20

    assert MetaCollector('TestRepoOwner', 'TestRepoName').core_developers == [{'name': 'Peter Shor', 'additions': 500, 'deletions': -500, 'commits': 100}, {'name': 'Peter Shor', 'additions': 500, 'deletions': -500, 'commits': 100}, {'name': 'Peter Shor', 'additions': 500, 'deletions': -500, 'commits': 100}, {'name': 'Peter Shor', 'additions': 500, 'deletions': -500, 'commits': 100}, {'name': 'Peter Shor', 'additions': 500, 'deletions': -500, 'commits': 100}] 

    repo_mock.return_value.get_stats_contributors.return_value = [monkeys.MonkeyStatsContributor() for i in range(5)]
    repo_mock.return_value.get_commits.return_value = list(range(10))
    stats_mock.return_value.weeks = [monkeys.MonkeyWeeks() for i in range(5)]
    stats_mock.return_value.author= monkeys.MonkeyUser()

    repo_mock.return_value.get_stats_code_frequency.return_value = [monkeys.MonkeyStatsCodeFrequency() for i in range(100)]
    stats_mock.return_value.additions = 10
    stats_mock.return_value.deletions = -10

    weeks_mock.return_value.a = 1
    weeks_mock.return_value.d = -1
    weeks_mock.return_value.c = 0

    assert len(MetaCollector('TestRepoOwner', 'TestRepoName').core_developers) == 0
