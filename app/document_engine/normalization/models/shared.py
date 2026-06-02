from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class NormalizedMargins:
    top: int            # twips
    bottom: int         # twips
    left: int           # twips
    right: int          # twips