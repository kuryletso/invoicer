from typing import Optional

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class NormalizedSectionStyle:
    page_width: Optional[int]
    page_height: Optional[int]
    orientation: Optional[int]
    margin_header: Optional[int]
    margin_footer: Optional[int]
    margin_top: Optional[int]
    margin_bottom: Optional[int]
    margin_left: Optional[int]
    margin_right: Optional[int]