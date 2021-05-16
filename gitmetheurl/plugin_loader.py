def iter_entry_points(group_name):
    try:
        import pkg_resources
    except ImportError:
        return []

    return pkg_resources.iter_entry_points(group_name)

def get_translator_plugins():
    return [ep.load() for ep in iter_entry_points("gitmetheurl.translators")]
