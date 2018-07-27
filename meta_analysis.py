import datetime as dt
from github import Github
from config import OAUTH_TOKEN

class Repository(object):
	
	osi_license_ids = ["MPL-2.0", "GPL-2.0", "MIT", "LGPL-3.0", "BSD-2-Clause",
			   "EPL-2.0", "Apache-2.0", "BSD-3-Clause", "GPL-3.0", "LGPL-2.1"]

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
		last_twenty_commits = self.commits[:19]
		extract_date = lambda text_date: dt.datetime.strptime(text_date.stats.last_modified[5:16], "%d %b %Y")
		in_past_year = lambda date: (dt.datetime.now() - date) < dt.timedelta(weeks=52)
		return any(map(in_past_year, map(extract_date, last_twenty_commits)))

	@property
	def contributor_count(self):
		"""
		Returns the number of contributors
		for this project.
		"""	
		return len([contributor for contributor in self.repo.get_stats_contributors()])
		
	def osi_license(self):
		"""
		Returns True if the license associated
		with this repository is a valid OSI license.
		"""
		license_name = self.repo.get_license().license.spdx_id
		return license_name in self.osi_license_ids

	def has_issues_or_prs(self):
		"""
		Returns True if the repository has Issues
		and Pull Requests from external people.
		"""
		if not self.repo.has_issues:
			return False

		issues = self.repo.get_issues()
		for issue in issues:
			if issue.user == self.repo.owner:
				continue
			# check if author of issue or PR is from the same company
			if issue.user.company is not None:
				if issue.user.company[1:-1] == self.user.login:
					print('same company')
		return True # dummy return

	def core_developers(self):
		"""
		Returns a list of names of core
		developers (>20% of code).
		"""
		pass

import bpython
bpython.embed(locals_=locals())
