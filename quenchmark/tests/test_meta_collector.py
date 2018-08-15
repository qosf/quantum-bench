import mock
import datetime as dt
from unittest.mock import patch

import pytest
import github

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

@patch('monkeys.MonkeyStatsContributor')
@patch('monkeys.MonkeyRepo')
@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_get_contributors(repo_mock, stats_mock):
    """
    Getting the list of contributors for a project.
    """
    repo_mock.return_value.get_stats_contributors.return_value = [monkeys.MonkeyStatsContributor() for i in range(5)]
    stats_mock.return_value.weeks = [monkeys.MonkeyWeeks() for i in range(5)]
    stats_mock.return_value.author= monkeys.MonkeyUser()
    contributor_list = [{'additions': 500, 'commits': 250, 'deletions': 1000, 'name': 'Peter Shor'},
            {'additions': 500, 'commits': 250, 'deletions': 1000, 'name': 'Peter Shor'},
            {'additions': 500, 'commits': 250, 'deletions': 1000, 'name': 'Peter Shor'},
            {'additions': 500, 'commits': 250, 'deletions': 1000, 'name': 'Peter Shor'},
            {'additions': 500, 'commits': 250, 'deletions': 1000, 'name': 'Peter Shor'}]
    assert MetaCollector('TestRepoOwner', 'TestRepoName').get_contributors() == contributor_list
