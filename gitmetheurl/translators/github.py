
import re

from .translator import Translator

class GitHub(Translator):
    """
    Remote formats:
        git@github.com:PROJECT/REPO.git
        https://github.com/PROJECT/REPO.git

    Views:
        File:       https://github.com/PROJECT/REPO/blob/master/test.txt
        Folder:     https://github.com/PROJECT/REPO/tree/master/subfolder
        At Branch:  https://github.com/PROJECT/REPO/blob/whitespace/test.txt
        At commit:  https://github.com/PROJECT/REPO/blob/5e80224ebc8b7324e085af68d3071739ff8f1b02/test.txt
                    https://github.com/PROJECT/REPO/tree/5e80224ebc8b7324e085af68d3071739ff8f1b02
        
        Single line:    https://github.com/PROJECT/REPO/blob/master/test.txt#L4
        Line Span:      https://github.com/PROJECT/REPO/blob/master/test.txt#L8-L12
    """
    SSH_REGEX = r'git@github\.com:(?P<project>[\w\-]+)/(?P<repo>[\w\-]+)\.git'
    HTTPS_REGEX = r'https://github\.com/(?P<project>[\w\-]+)/(?P<repo>[\w\-]+)\.git'


    def construct_source_url(self, remote: str, relpath: str, is_folder: bool, line = None, commit: str = None, branch: str = None):
        
        # Parse remote
        m = re.fullmatch(self.SSH_REGEX, remote) or re.fullmatch(self.HTTPS_REGEX, remote)
        project_name, repo_name = m.group("project", "repo")

        if is_folder:
            urltype = "tree"
            line_suffix = ""
        else:
            urltype = "blob"
            if isinstance(line, int):
                line_suffix = "#L%d" % line
            elif isinstance(line, tuple) and len(line) == 2:
                line_suffix = "#L%d-L%d" % line
            else:
                line_suffix = ""

        if branch is not None:
            ref = branch
        elif commit is not None:
            ref = commit
        else:
            # uuh panic!!
            ref = "master"
        
        return "https://github.com/%s/%s/%s/%s/%s%s" % (
            project_name, repo_name,
            urltype, ref,
            relpath, line_suffix
        )
