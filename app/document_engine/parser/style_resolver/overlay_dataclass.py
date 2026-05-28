from typing import TypeVar

from dataclasses import fields, is_dataclass

T = TypeVar("T")

def overlay_dataclass(base: T | None, override: T | None) -> T | None:
    if base is None:
        return override
    
    if override is None:
        return base
    
    if not is_dataclass(base):
        raise TypeError(
            "Must be a dataclass instance."
        )
    
    if not is_dataclass(override):
        raise TypeError(
            "Must be a dataclass instance."
        )
    
    values = {}

    for field in fields(base):
        override_value = getattr(override, field.name)

        if override_value is not None:
            values[field.name] = override_value
        else:
            values[field.name] = getattr(base, field.name)

    return type(base)(**values)