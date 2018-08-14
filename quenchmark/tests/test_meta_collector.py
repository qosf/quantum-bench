import mock
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

@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_commit_count():
    """
    Testing if >100 commits really results in True.
    """
    assert MetaCollector('TestRepoOwner', 'TestRepoName').commit_count == 10

@patch('monkeys.MonkeyUser.get_repo')
@patch('github.Github.search_users', mock.MagicMock(return_value=[monkeys.MonkeyUser()]))
@patch('github.Github.__init__', mock.MagicMock(return_value=None))
def test_is_young(repo_mock):
    """
    Testing if a project is young (< 1 year).
    """
    repo_mock.return_value = monkeys.YoungMonkeyRepo()
    assert MetaCollector('TestRepoOwner', 'TestRepoName').is_young == True
    repo_mock.return_value = monkeys.OldMonkeyRepo()
    assert MetaCollector('TestRepoOwner', 'TestRepoName').is_young == False


@patch('github.Github', mock.MagicMock(return_value=monkeys.MonkeyGithub()))
def test_has_recent_commits():
    """
    Testing if a project had at least 20 commits in the past year.
    """
    assert MetaCollector('TestRepoOwner', 'TestRepoName').is_young == True
