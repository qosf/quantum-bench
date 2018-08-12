import datetime as dt
from functools import reduce
from difflib import SequenceMatcher as SM

from cached_property import cached_property
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

    @cached_property
    def commit_count(self):
        """
        Returns the total number of commits.
        """
        return len([commit for commit in self.commits])

    @cached_property
    def is_young(self):
        """
        Returns True if the repository
        is younger than one year.
        """
        return (dt.datetime.now() - self.repo.created_at) > dt.timedelta(weeks=52)

    @cached_property
    def has_recent_commits(self):
        """
        Returns True if the repository had at
        least 20 commits in the past year.
        """
        last_twenty_commits = self.commits[:19]
        extract_date = lambda text_date: dt.datetime.strptime(text_date.stats.last_modified[5:16], "%d %b %Y")
        in_past_year = lambda date: (dt.datetime.now() - date) < dt.timedelta(weeks=52)
        return any(map(in_past_year, map(extract_date, last_twenty_commits)))

    @cached_property
    def contributor_count(self):
        """
        Returns the number of contributors
        for this project.
        """    
        return len(self.get_contributors())
        
    @cached_property
    def osi_license(self):
        """
        Returns True if the license associated
        with this repository is a valid OSI license.
        """
        license_name = self.repo.get_license().license.spdx_id
        return license_name in self.osi_license_ids

    @cached_property
    def has_xtrnl_issues_or_prs(self):
        """
        Returns True if the repository has Issues
        and Pull Requests from external people.
        """
        if not self.repo.has_issues or len(self.get_xtrnl_issues_and_prs()) == 0:
            return False
        else:
            return True

    @cached_property
    def core_developers(self):
        """
        Returns a list of names of core
        developers (>10% of total additions OR deletions OR >15% of total commits).
        """
        adds_and_dels = self.get_total_adds_and_dels()

        is_core_dev = lambda contributor: (contributor['additions']/adds_and_dels['additions'] > 0.10) \
                        or (contributor['deletions']/adds_and_dels['deletions']*-1 > 0.10) \
                        or (contributor['commits']/self.commit_count > 0.15)

        return list(filter(is_core_dev, self.get_contributors()))

    @cached_property
    def has_ignored_issues_and_prs(self):
        """
        Returns True if more than 50% of external Issues and PRs
        were ignored within their first month of existence.
        """
        external_issues_and_prs = self.get_xtrnl_issues_and_prs()
        core_dev_names = [dev['name'] for dev in self.core_developers]
        ignorance_counter = 0

        for ext_issue in external_issues_and_prs:
            replied_on_time = False
            for comment in ext_issue.get_comments():
                if ext_issue.created_at - comment.created_at > dt.timedelta(weeks=4):
                    break # no one replied for one month
                if comment.user.login in core_dev_names or self.is_part_of_company(comment.user):
                    replied_on_time = True    
                    break

            if replied_on_time == False:
                ignorance_counter += 1

        # if more than 50% of Issues and PRs were ignored we consider the project abandoned
        if ignorance_counter/len(external_issues_and_prs) > 0.50:
            return True
        else:
            return False

    def get_contributors(self):
        """
        Returns a list of dictionaries. Each dictionary represents
        as single contributor and provides their name and their
        total number of additions and deletions.
        """
        extract = lambda list_of_weeks, param: sum([week.a if param == 'a' else
                                (week.d if param == 'd' else week.c)
                                for week in list_of_weeks]
        )
        return [{'name': contributor.author.login,
                'additions': extract(contributor.weeks, 'a'),
                'deletions': extract(contributor.weeks, 'd'),
                'commits': extract(contributor.weeks, 'c')}
                for contributor in self.repo.get_stats_contributors()
        ]
    
    def get_xtrnl_issues_and_prs(self):
        """
        Returns a list of Issues and PRs from external
        developers.
        """
        
        # get all issues and names of core developers
        issues = [issue for issue in self.repo.get_issues(state='all')]
        core_dev_names = [dev['name'] for dev in self.core_developers]    

        external_issues_and_prs = [] # initialize an empty list

        for issue in issues:

            if issue.user == self.repo.owner:
                continue

            # check if author of issue or PR is from the same company that owns the repo
            if self.is_part_of_company(issue.user):
                    continue

            # check if author of issue is a core developer
            if issue.user.login in core_dev_names:
                    continue
            else:
                external_issues_and_prs.append(issue)

        return external_issues_and_prs

    def is_part_of_company(self, user):
        """
        Returns True if user is part
        of the company that owns the repo.
        """

        # define lambda for fuzzy string comparison (yields true if >90% overlap)
        fuzzy_compare = lambda string1, string2: SM(None, string1, string2).ratio() > 0.9
            
        if user.company is None:
            return False
        elif fuzzy_compare(user.company, self.user.login):
            # we use fuzzy string comparison to account for spelling or punctuation diffs
            return True
        elif self.user.name is not None: # some users have only login and no name
            if fuzzy_compare(user.company, self.user.name):
                return True
        else:
            return False
    
    def get_total_adds_and_dels(self):
        """
        Returns a dictionary with the total
        number of additions and deletions
        in this repository.
        """
        stats = {}
        stats['additions'] = reduce(lambda x, y: (x + y.additions) if type(x) is int \
                     else (x.additions + y.additions), self.repo.get_stats_code_frequency()
        )
        stats['deletions'] = reduce(lambda x, y: (x + y.deletions) if type(x) is int \
                     else (x.deletions + y.deletions), self.repo.get_stats_code_frequency()
        )
        return stats
    
    def is_valid(self):
        """
        Executes the entire decision tree and yields True
        if the repo satisfies all conditions. Hence, the repo
        is a valid OSS repo that is valuable to other and also
        obeys good practices.    
        """

        if not self.osi_license: 
            print('license not okay')
            return False
        print('license okay')
        if self.contributor_count == 1:
              print('only 1 contributor')
              return False
        print('>1 contributor')
        if not self.is_young and self.commit_count < 100:
              print('project is old and has less than 100 commits.')
              return False
        print('project either old and has more than 100 commits or young.')
        if self.is_young and not self.has_recent_commits:
              print('project is young but has too little recent commits')
              return False
        print('project maybe young and enough recent commits')
        if not self.has_xtrnl_issues_or_prs:
              print('project has no xtrnl issues')
              return False
        print('project has xtrnl issues')
        if self.has_ignored_issues_and_prs:
            print('project is ignorant')
            return False
        print('project not ignorant')
        return True # since it has satisfied all previous conditions
