from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List, Type, Iterable
    import pkg_resources
    from .translators.translator import TranslatorSpec

def iter_entry_points(group_name: str) -> 'Iterable[pkg_resources.EntryPoint]':
    try:
        import pkg_resources
    except ImportError:
        return []

    return pkg_resources.iter_entry_points(group_name)

def get_translator_plugins() -> 'List[Type[TranslatorSpec]]':
    return [ep.load() for ep in iter_entry_points("gitmetheurl.translators")]
