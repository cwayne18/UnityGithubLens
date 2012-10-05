import logging
import optparse
import urllib2
import simplejson

import gettext
from gettext import gettext as _
gettext.textdomain('unity-lens-github')

from singlet.lens import SingleScopeLens, IconViewCategory, ListViewCategory

from unity_lens_github import unity_lens_githubconfig

class GithubLens(SingleScopeLens):

    class Meta:
        name = 'github'
        description = 'Github Lens'
        search_hint = 'Search Github'
        icon = 'github.png'
        search_on_blank = False
        
    github_icon = '/usr/share/unity/lenses/github/github-logo.png'
    repo_category = ListViewCategory("Repos", github_icon)
    
    
    def search_repos(self, search):
        try:
            repo_url = 'https://api.github.com/legacy/repos/search/%s' % search
            repos = simplejson.loads(urllib2.urlopen(repo_url).read())['repositories']
            return repos
        except (IOError, KeyError, urllib2.URLError, urllib2.HTTPError, simplejson.JSONDecodeError):
            print "Error, unable to search github"
            return []

    def search(self, search, results):
        # TODO: Add your search results
        for repo in self.search_repos(search):
            desc = ''
            if repo['description']:
                desc = repo['description']
            results.append('http://github.com/%s/%s' % (repo['owner'], repo['name']),
                            self.github_icon,
                            self.repo_category,
                            "text/html",
                            '%s/%s' % (repo['owner'], repo['name']),
                            desc,
                            'http://github.com/%s/%s' % (repo['owner'], repo['name']))
        pass
