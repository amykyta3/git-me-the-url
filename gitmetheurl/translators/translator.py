import re

class TranslatorSpec:
    #: list of regexes to match the git remote URL.
    #: This is typically two regexes - one for SSH and another for HTTPS
    #: Regexes are searched sequentially. The first successful match is used.
    #: If an expression uses named groups, the group names can be used later in URL recipes
    remote_regexes = []

    # TODO: Clean up these docstrings!
    #: List of URL recipies.
    #: a recipe entry can be either a format string or a tuple containing a
    #: format string and conditional expression.
    #:
    #: format strings are processed using str.format() using the keys available
    #: in the info dictionary.
    #:
    #: Conditional strings are evaluated. keys from the info dictionary are
    #: available as local variables
    #:
    #: The first recipe that matches its conditional (if any), and can be
    #: formatted successfully is used.
    #:
    #: [
    #:       ("https://github.com/{project_name}/{repo_name}/blob/{branch_name}/{path}", "is_folder == False"),
    #:       ("https://github.com/{project_name}/{repo_name}/tree/{branch_name}/{path}", "is_folder == True"),
    #: ]


    #: Formatting recipes for the URL prefix.
    #: This is usually for handling variations in the repository's base URL
    url_root_recipes = []

    #: Formatting recipes for the main contents of the URL
    #: This is a good place to define variations in file/folder paths, branch/commit references, etc.
    url_body_recipes = []

    #: Formatting recipes for the URL's suffix
    #: Use this to define line number highligting, etc.
    url_suffix_recipes = []

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
        for regex in cls.remote_regexes:
            if re.fullmatch(regex, remote):
                return True

        return False


    @classmethod
    def get_source_url(cls, remote: str, info: dict) -> str:

        # Get match object for remote url
        m = None
        for regex in cls.remote_regexes:
            m = re.fullmatch(regex, remote)
            if m:
                break
        assert m is not None

        # Extract any named match groups and stuff them to the info dictionary
        for k,v in m.groupdict().items():
            if v is not None:
                info[k] = v

        url_root = cls.process_recipe(info, cls.url_root_recipes)
        url_body = cls.process_recipe(info, cls.url_body_recipes)
        url_suffix = cls.process_recipe(info, cls.url_suffix_recipes)

        return url_root + url_body + url_suffix


    @classmethod
    def process_recipe(cls, info: dict, recipes: list) -> str:

        for recipe in recipes:
            if isinstance(recipe, tuple):
                format_string, conditional = recipe

                # Check conditional
                if not eval(conditional, {}, info):
                    continue
            else:
                # unconditional format string
                format_string = recipe
            assert isinstance(format_string, str)

            # Process format string
            try:
                return format_string.format(**info)
            except KeyError:
                # format string tried to use an info key that was unavailable
                # not a match
                pass

        raise RuntimeError
