### BEGIN LICENSE
# Copyright (C) 2012 Chris Wayne <cwayne@ubuntu.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE
import logging
import optparse
import urllib2
import simplejson

import locale
from locale import gettext as _
locale.textdomain('unity-lens-github')

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
    user_category = ListViewCategory("Users", github_icon)
    
    
    def search_github(self, search, search_type):
        try:
            repo_url = 'https://api.github.com/legacy/%s/search/%s' % (search_type, search)
            if search_type == 'repos':
                repos = simplejson.loads(urllib2.urlopen(repo_url).read())['repositories']
            elif search_type == 'user':
                repos = simplejson.loads(urllib2.urlopen(repo_url).read())['users']
            print repos
            return repos
        except (IOError, KeyError, urllib2.URLError, urllib2.HTTPError, simplejson.JSONDecodeError):
            print "Error, unable to search github"
            return []
            
    
    def search_user_repo(self, search):
        try:
            search_url = 'https://api.github.com/users/%s/repos' % search
            user_repos = simplejson.loads(urllib2.urlopen(search_url).read())
            print user_repos
            return user_repos
        except (IOError, KeyError, urllib2.URLError, urllib2.HTTPError, simplejson.JSONDecodeError):
            print "Error, unable to search github"
            return []

    def search(self, search, results):
        if len(search) > 2:
            if search[0] == "@":
                for user_repo in self.search_user_repo(search.strip('@')):
                    if user_repo['owner']['avatar_url']:
                        icon = user_repo['owner']['avatar_url']
                    else:
                        icon = self.github_icon
                    results.append(user_repo['html_url'],
                                   icon,
                                   self.repo_category,
                                   "text/html",
                                   '%s/%s' % (user_repo['owner']['login'], user_repo['name']),
                                   user_repo['description'],
                                   user_repo['html_url'])
            else:
                for repo in self.search_github(search, 'repos'):
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
                for user in self.search_github(search, 'user'):
                    name = ''
                    if user['name']:
                        name = user['name']
                    results.append('http://github.com/%s' % user['username'],
                                    self.github_icon,
                                    self.user_category,
                                    "text/html",
                                    user['username'],
                                    name,
                                    'http://github.com/%s' % user['username'])
        pass
