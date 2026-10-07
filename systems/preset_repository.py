"""
Shared flat-file preset registry plumbing, used by every `*_preset_repository`
module under /systems/ (task_preset_repository, site_preset_repository, ...).

Presets are stored as literal constructor calls in a plain Python module, so
they stay human-readable and diffable in git instead of living in JSON or a
DB table. Each concrete repository supplies its own PRESETS_PATH, the name
of the dict variable in that file, and a file header (docstring + whatever
imports its preset type's constructor call needs) -- everything else
(load/save/add/search) is generic and lives here.
"""

from __future__ import annotations
import importlib.util
from dataclasses import fields, is_dataclass
from enum import Enum
from pathlib import Path
from typing import Callable, TypeVar


T = TypeVar("T")


# What text a preset should be matched against in search_presets, given its
# dict key and the preset object itself. Defaults to just the key. Pass a
# different callable for preset types that carry their own searchable text
# (e.g. TaskPreset's `notes` field): lambda key, p: f"{key} {p.notes or ''}"
SearchKey = Callable[[str, T], str]


def _default_search_key(key: str, preset: T) -> str:
    return key


DEFAULT_SEARCH_KEY: SearchKey = _default_search_key


def load_presets(
    path: Path, dict_name: str
) -> dict[str, T]:
    """Import `path` fresh and return the dict stored under `dict_name`.

    Uses importlib directly (rather than a normal `import`) so repeated
    calls always reflect the current file contents on disk, rather than a
    cached module from an earlier import.
    """
    spec = importlib.util.spec_from_file_location(
        path.stem, path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return dict(getattr(module, dict_name))


def search_presets(
    presets: dict[str, T],
    query: str | None,
    search_key: SearchKey = DEFAULT_SEARCH_KEY,
) -> list[T]:
    """Case-insensitive substring match against search_key(key, preset)."""
    if not query:
        return list(presets.values())
    q = query.strip().lower()
    if not q:
        return list(presets.values())
    return [
        preset
        for key, preset in presets.items()
        if q in search_key(key, preset).lower()
    ]


def _format_value(value: object) -> str:
    if isinstance(value, Enum):
        return f"{type(value).__name__}.{value.name}"
    return repr(value)


def _format_instance(key: str, preset: T) -> str:
    """Render one `key: PresetType(field=value, ...)` entry, in
    declaration-field order, with Enum fields written as
    `EnumType.MEMBER_NAME` and everything else as repr()."""
    if not is_dataclass(preset):
        raise TypeError(
            f"preset_file formatting only supports dataclasses, got {type(preset)!r}"
        )
    lines = [f"    {key!r}: {type(preset).__name__}("]
    for f in fields(preset):
        value = getattr(preset, f.name)
        lines.append(
            f"        {f.name}={_format_value(value)},"
        )
    lines.append("    ),")
    return "\n".join(lines) + "\n"


def save_presets(
    path: Path,
    dict_name: str,
    header: str,
    presets: dict[str, T],
    value_type: str = "object",
) -> None:
    """Regenerate `path` wholesale from `presets`. `header` must include
    the file's module docstring plus any imports the preset type's
    constructor call and its enum fields (if any) need."""
    body = "".join(
        _format_instance(key, preset)
        for key, preset in presets.items()
    )
    text = f"{header}{dict_name}: dict[str, {value_type}] = {{\n{body}}}\n"
    path.write_text(text, encoding="utf-8")


def add_preset(
    path: Path,
    dict_name: str,
    header: str,
    key: str,
    preset: T,
    value_type: str = "object",
) -> dict[str, T]:
    """Add or overwrite one preset under `key` and persist the whole dict.
    Returns the new dict."""
    presets = load_presets(path, dict_name)
    presets[key] = preset
    save_presets(
        path,
        dict_name,
        header,
        presets,
        value_type=value_type,
    )
    return presets
