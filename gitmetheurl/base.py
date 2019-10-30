import os

import git

from .translators import GitHub
from .translators import GitLab
from .translators import Bitbucket

class GitMeTheURL:

    def __init__(self):
        self.translators = [
            GitHub,
            GitLab,
            Bitbucket
        ]


    def get_source_url(self, path: str, line = None, exact_commit: bool = False) -> str:
        """
        Convert a path to a file into a URL to the file in the service's source
        browser.

        Parameters
        ----------
        path: str
            Path to file.
        line: int or tuple
            Line(s) to highlight if the service supports it.
            If integer, selects a single line.
            If 2-tuple, selects the line range.
        exact_commit: bool
            If overridden to ``True``, will attempt to generate a URL that
            points to the source file at the same commit as it is currently.
        """
        repo = git.Repo(path, search_parent_directories=True)

        root_path = repo.git.rev_parse("--show-toplevel")

        try:
            urls = repo.remote().urls # raises ValueError if there is no origin
        except ValueError:
            raise GMTUException("Repository does not have any remotes")

        for url in urls:
            remote = url
            break
        else:
            raise ValueError("Repository does not have a remote URL set")

        is_folder = os.path.isdir(path)
        relpath = os.path.relpath(path, root_path)

        # Eliminate corner case
        if relpath == ".":
            relpath = ""

        # Lookup translator
        for t in self.translators:
            if t.is_match(remote):
                translator = t
                break
        else:
            raise GMTUException("Unable to convert remote: %s" % remote)

        # Get branch/commit reference as appropriate
        commit = None
        branch = None
        if exact_commit:
            # Unconditionally pointing to exact commit.
            commit = repo.head.object.hexsha
        else:
            # Attempt to determine current branch
            branch = self.get_branch(repo)

            if branch is None:
                # failed to get remote branch. Fall back to commit
                commit = repo.head.object.hexsha

        # Construct the URL!
        return translator().construct_source_url(
            remote, relpath, is_folder, line, commit, branch
        )


    @staticmethod
    def get_branch(repo):
        try:
            return repo.active_branch.name
        except TypeError:
            # Likely detached head
            pass

        # Find remote branch that contains this commit
        for ref in repo.remotes.origin.refs:
            if repo.is_ancestor(repo.head.object, ref.object):
                # Return branch name but strip "origin/" prefix
                return ref.name[len("origin/"):]
        return None

class GMTUException(Exception):
    pass
