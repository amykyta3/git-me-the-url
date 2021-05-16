import re

class Translator:
    SSH_REGEX = None # type: str
    HTTPS_REGEX = None # type: str

    @classmethod
    def is_match(cls, remote: str) -> bool:
        """
        Checks if remote URL is a match for this translator's service.
        Returning True guarantees that this translator can generate a link.

        Parameters
        ----------
        remote: str
            remote git URL.
        """
        # SSH remote
        if re.fullmatch(cls.SSH_REGEX, remote):
            return True

        # HTTPS remote
        if re.fullmatch(cls.HTTPS_REGEX, remote):
            return True

        return False


    def construct_source_url(self, remote: str, relpath: str, is_folder: bool, line = None, commit: str = None, branch: str = None) -> str:
        """
        Constructs the file browser URL given the available information.

        Caller will attempt to provide the branch name. Otherwise, the commit
        hash is provided.

        Parameters
        ----------
        remote: str
            remote git URL.
        relpath: str
            Path to file relative to repository root.
        is_folder: bool
            True if relpath points to a directory rather than a file.
        commit: str
            Commit hash.
            If present, URL should to point to the file's source at this exact commit.
        branch: str
            Branch name.
            If present, URL should point to the given branch.
        line: int or tuple
            Line(s) to highlight if the service supports it.
            If integer, selects a single line.
            If 2-tuple, selects the line range.
        """
        raise NotImplementedError
