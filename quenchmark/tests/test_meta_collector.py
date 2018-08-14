import mock
from unittest.mock import patch

import pytest
import github

from quenchmark.collectors.meta import MetaCollector

class MonkeyGithub(object):
    @classmethod
    def get_repo(cls, *args, **kwargs):
        return cls
    def get_commits(*args, **kwargs):
        return ['Commit #1', 'Commit #2', 3, 4, 5, 6, 7, 8, 9, 10]

@patch('github.Github.search_users', mock.MagicMock(return_value=[MonkeyGithub()]))
@patch('github.Github.__init__', mock.MagicMock(return_value=None))
def test_init():
    """
    Tests the instantiation of a Repository object.
    """
    #github_mock.return_value = None
    #github_mock.search_users.return_value = 'TestUser'
    #user_mock.get_repo.return_value = 'TestRepo'
    #github_mock.commits.return_value = 'TestCommits'
    
    repo = MetaCollector('RepoOwner', 'RepoName')

@patch('github.Github.search_users', mock.MagicMock(return_value=[MonkeyGithub()]))
@patch('github.Github.__init__', mock.MagicMock(return_value=None))
def test_commit_count():
    """
    Testing if >100 commits really results in True.
    """
    #init_mock.commits.return_value = list(range(10))
    assert MetaCollector('RepoOwner', 'RepoName').commit_count == 10
