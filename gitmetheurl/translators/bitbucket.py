
import re

from .translator import Translator

class Bitbucket(Translator):
    """
    Remote formats:
        git@bitbucket.org:PROJECT/REPO.git
        https://USER@bitbucket.org/PROJECT/REPO.git

    Views:
        File:       https://bitbucket.org/PROJECT/REPO/src/master/README.txt
        Folder:     https://bitbucket.org/PROJECT/REPO/src/master/folder
        At Branch:  https://bitbucket.org/PROJECT/REPO/src/mybranch/README.txt
        At commit:  https://bitbucket.org/PROJECT/REPO/src/c08065253fb89a071b84e3f27bdcb94853f0004c/README.txt

        Single line:    https://bitbucket.org/PROJECT/REPO/src/master/README.txt#lines-13
        Line Span:      https://bitbucket.org/PROJECT/REPO/src/master/README.txt#lines-13:18
    """
    SSH_REGEX = r'git@bitbucket\.org:(?P<project>[\w\-]+)/(?P<repo>[\w\-]+)\.git'
    HTTPS_REGEX = r'https://[\w\-]+@bitbucket\.org/(?P<project>[\w\-]+)/(?P<repo>[\w\-]+)\.git'

    def construct_source_url(self, remote: str, relpath: str, is_folder: bool, line = None, commit: str = None, branch: str = None) -> str:

        # Parse remote
        m = re.fullmatch(self.SSH_REGEX, remote) or re.fullmatch(self.HTTPS_REGEX, remote)
        assert m is not None
        project_name, repo_name = m.group("project", "repo")

        if is_folder:
            line_suffix = ""
        else:
            if isinstance(line, int):
                line_suffix = "#lines-%d" % line
            elif isinstance(line, tuple) and len(line) == 2:
                line_suffix = "#lines-%d:%d" % line
            else:
                line_suffix = ""

        if branch is not None:
            ref = branch
        elif commit is not None:
            ref = commit
        else:
            # uuh panic!!
            ref = "master"

        return "https://bitbucket.org/%s/%s/src/%s/%s%s" % (
            project_name, repo_name,
            ref,
            relpath, line_suffix
        )
