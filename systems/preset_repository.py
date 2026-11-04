"""
Shared flat-file preset registry plumbing, used by every `*_preset_repository`
module under /systems/ (task_preset_repository, site_preset_repository, ...).

Presets are stored as literal constructor calls in a plain Python module, so
they stay human-readable and diffable in git instead of living in JSON or a
DB table. Each concrete repository supplies its own PRESETS_PATH, the name
of the dict variable in that file, and a file header (docstring + whatever
imports its preset type's constructor call needs) -- everything else
(load/save/add/search) is generic and lives here.

Saving is verified: the new file is written next to the real one, loaded
back, and compared with the presets it was generated from. Only if they are
equal does it replace the registry file, so a formatting or missing-import
problem raises an error instead of leaving an unloadable file behind.
"""

from __future__ import annotations
import importlib.util
import os
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
    if spec is None:
        raise ValueError(
            f"Path {path} for presets location is wrong!"
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


_INDENT = "    "


def _format_value(value: object, level: int = 0) -> str:
    """Render `value` as Python source that evaluates back to an equal value.

    Recursive, so enums and dataclasses nested inside dicts, tuples or other
    dataclasses are written as `EnumType.MEMBER` / `Type(field=...)`, never
    as their repr() (which for an enum is `<Type.MEMBER: 'x'>` -- not valid
    source). Anything else (str, int, float, bool, None, ...) uses repr().
    The names it writes must be imported by the repository's header.
    """
    pad = _INDENT * level
    if isinstance(value, Enum):
        return f"{type(value).__name__}.{value.name}"
    if is_dataclass(value) and not isinstance(value, type):
        lines = [f"{type(value).__name__}("]
        for f in fields(value):
            if not f.init:
                continue
            rendered = _format_value(
                getattr(value, f.name), level + 1
            )
            lines.append(
                f"{pad}{_INDENT}{f.name}={rendered},"
            )
        lines.append(f"{pad})")
        return "\n".join(lines)
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = ["{"]
        for k, v in value.items():
            lines.append(
                f"{pad}{_INDENT}{_format_value(k, level + 1)}: "
                f"{_format_value(v, level + 1)},"
            )
        lines.append(f"{pad}}}")
        return "\n".join(lines)
    if isinstance(value, (list, tuple)):
        items = [_format_value(v, level + 1) for v in value]
        if isinstance(value, list):
            return "[" + ", ".join(items) + "]"
        trailing = "," if len(items) == 1 else ""
        return "(" + ", ".join(items) + trailing + ")"
    return repr(value)


def _format_instance(key: str, preset: T) -> str:
    """Render one `key: PresetType(field=value, ...)` entry, in
    declaration-field order."""
    if not is_dataclass(preset):
        raise TypeError(
            f"preset_file formatting only supports dataclasses, got {type(preset)!r}"
        )
    return (
        f"{_INDENT}{key!r}: {_format_value(preset, 1)},\n"
    )


def save_presets(
    path: Path,
    dict_name: str,
    header: str,
    presets: dict[str, T],
    value_type: str = "object",
) -> None:
    """Regenerate `path` wholesale from `presets`. `header` must include
    the file's module docstring plus every name the generated constructor
    calls use (the preset type, its enums, nested dataclasses).

    The text is checked before it replaces `path`: it must compile, import,
    and load back equal to `presets`. On any failure `path` is untouched.
    """
    body = "".join(
        _format_instance(key, preset)
        for key, preset in presets.items()
    )
    text = f"{header}{dict_name}: dict[str, {value_type}] = {{\n{body}}}\n"
    compile(text, str(path), "exec")

    pending = path.with_name(f"_{path.stem}_pending.py")
    try:
        pending.write_text(text, encoding="utf-8")
        loaded = load_presets(pending, dict_name)
        bad = [
            key
            for key in presets
            if loaded.get(key) != presets[key]
        ]
        if bad or loaded.keys() != presets.keys():
            raise ValueError(
                f"generated {path.name} does not load back equal to the "
                f"presets it was written from (differs: {bad or 'keys'})"
            )
        os.replace(pending, path)
    finally:
        pending.unlink(missing_ok=True)


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
