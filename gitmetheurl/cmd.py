import argparse
import re
import sys

import git

from . import GitMeTheURL, GMTUException

def main() -> None:
    #----------------------------------
    # Collect command line arguments
    #----------------------------------
    parser = argparse.ArgumentParser(
        description="Create a shareable URL to a Git repository"
    )
    parser.add_argument(
        '-e', '--exact', dest='exact_commit', action='store_true',default=False,
        help="If set, URL will point to the file at the exact commit."
    )
    parser.add_argument('target_path',
        nargs="?", default=".",
        help='Generate a public URL to this path.'
    )
    options = parser.parse_args()

    #----------------------------------
    # Parse target path
    m = re.fullmatch(r'(?P<path>.+?):(?P<line>\d+)(?:-(?P<to_line>\d+))?', options.target_path)
    if not m:
        path = options.target_path
        line = None
    else:
        path = m.group("path")
        line = int(m.group("line"))
        to_line = m.group("to_line")
        if to_line is not None:
            line = tuple(sorted([line, int(to_line)]))

    #----------------------------------
    gmtu = GitMeTheURL()

    #----------------------------------
    # Translate the path!
    #----------------------------------
    try:
        url = gmtu.get_source_url(path, line=line, exact_commit=options.exact_commit)
    except git.InvalidGitRepositoryError:
        print("error: Path does not point to a git repository: %s" % path, file=sys.stderr)
        sys.exit(1)
    except git.NoSuchPathError:
        print("error: Path does not exist: %s" % path, file=sys.stderr)
        sys.exit(1)
    except GMTUException as e:
        print("error:", e.args[0], file=sys.stderr)
        sys.exit(1)

    #----------------------------------
    # Output
    #----------------------------------
    print(url)
