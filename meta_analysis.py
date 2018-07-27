import datetime as dt
from github import Github
from config import OAUTH_TOKEN

class Repository(object):
	
	def __init__(self, user_name, repo_name):
		"""
		Gets the repo with repo_name from user_name's profile
		and already retrieves a list of all commits.
		"""
		
		# create a Github instance with OAuth token
		self.github = Github(OAUTH_TOKEN)
		
		# adding @ ensures finding users exactly
		self.user = self.github.search_users('@'+user_name)[0]
		self.repo = self.user.get_repo(repo_name)
		self.commits = [commit for commit in self.repo.get_commits()]

	@property	
	def commit_count(self):
		"""
		Returns the total number of commits.
		"""
		return len([commit for commit in self.commits])

	@property
	def is_young(self):
		"""
		Returns True if the repository
		is younger than one year.
		"""
		return (dt.datetime.now() - self.repo.created_at) > dt.timedelta(weeks=52)

	@property
	def has_recent_commits(self):
		"""
		Returns True if the repository had at
		least 20 commits in the past year.
		"""
		commits = self.commits()[:19]
		for commit in commits:
			commit_date_str = commit.stats.last_modified
			commit_date = dt.datetime.strptime(commit_date_str[5:16], "%d %b %Y")
			if (dt.datetime.now() - commit_date) > dt.timedelta(weeks=52):
				return False
			else:
				return True

	@property
	def contributor_count(self):
		"""
		Returns the number of contributors
		for this project.
		"""	
		return len([contributor for contributor in self.repo.get_stats_contributors()])
		
	def get_license(self):
		"""
		Returns the license file
		associated with the project.
		"""
		pass

import bpython
bpython.embed(locals_=locals())
