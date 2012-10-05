import logging
import optparse

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
        icon = 'github.svg'
        search_on_blank=True

    # TODO: Add your categories
    example_category = ListViewCategory("Examples", 'help')

    def search(self, search, results):
        # TODO: Add your search results
        results.append('https://wiki.ubuntu.com/Unity/Lenses/Singlet',
                         'ubuntu-logo',
                         self.example_category,
                         "text/html",
                         'Learn More',
                         'Find out how to write your Unity Lens',
                         'https://wiki.ubuntu.com/Unity/Lenses/Singlet')
        pass
