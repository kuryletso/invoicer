from typing import TypeVar

from dataclasses import fields, is_dataclass

T = TypeVar("T")


class OverlayDataclassError(Exception):
    """Basic dataclass overlay utility error."""


def overlay_dataclass(base: T | None, override: T | None) -> T | None:
    if base is None:
        return override
    
    if override is None:
        return base
    
    if not is_dataclass(base):
        raise OverlayDataclassError(
            f"Must be a dataclass instance, got {type(base).__name__}"
        )
    
    if not is_dataclass(override):
        raise OverlayDataclassError(
            f"Must be a dataclass instance, got {type(override).__name__}"
        )
    
    values = {}

    for field in fields(base):
        try:
            override_value = getattr(override, field.name)
        except AttributeError as e:
            raise OverlayDataclassError(
                f"Missing field '{field.name}' in override {type(override).__name__}"
            ) from e
        
        if override_value is not None:
            values[field.name] = override_value
        else:
            values[field.name] = getattr(base, field.name)

    return type(base)(**values)


def overlay_dataclass_strict(base: T, override: T) -> T:
    if not is_dataclass(base):
        raise OverlayDataclassError(
            f"Must be a dataclass instance, got {type(base).__name__}"
        )
    
    if not is_dataclass(override):
        raise OverlayDataclassError(
            f"Must be a dataclass instance, got {type(override).__name__}"
        )
    
    values = {}

    for field in fields(base):
        try:
            override_value = getattr(override, field.name)
        except AttributeError as e:
            raise OverlayDataclassError(
                f"Missing field '{field.name}' in override {type(override).__name__}"
            ) from e

        if override_value is not None:
            values[field.name] = override_value
        else:
            values[field.name] = getattr(base, field.name)

    return type(base)(**values)