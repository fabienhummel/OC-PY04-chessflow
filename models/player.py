"""Player business model."""

import re
from dataclasses import dataclass
from datetime import date
from typing import ClassVar


@dataclass(frozen=True, slots=True)
class Player:
    """Represent a chess player independently from any tournament score."""

    last_name: str
    first_name: str
    birth_date: date
    national_id: str

    NATIONAL_ID_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"^[A-Z]{2}\d{5}$")

    def __post_init__(self) -> None:
        """Normalize and validate player data."""
        last_name = self.last_name.strip()
        first_name = self.first_name.strip()

        if not last_name or not first_name:
            raise ValueError("First name and last name are required.")
        if not isinstance(self.birth_date, date):
            raise TypeError("Birth date must be a date instance.")

        object.__setattr__(self, "last_name", last_name)
        object.__setattr__(self, "first_name", first_name)
        object.__setattr__(self, "national_id", self.validate_national_id(self.national_id))

    @classmethod
    def validate_national_id(cls, national_id: str) -> str:
        """Return a normalized national ID or raise when its format is invalid."""
        if not isinstance(national_id, str):
            raise TypeError("National ID must be a string.")

        normalized_id = national_id.strip().upper()
        if not cls.NATIONAL_ID_PATTERN.fullmatch(normalized_id):
            raise ValueError("National ID must contain two letters followed by five digits.")
        return normalized_id

    def to_dict(self) -> dict[str, str]:
        """Serialize the player to JSON-compatible data."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date.isoformat(),
            "national_id": self.national_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "Player":
        """Build a player from serialized data."""
        return cls(
            last_name=data["last_name"],
            first_name=data["first_name"],
            birth_date=date.fromisoformat(data["birth_date"]),
            national_id=data["national_id"],
        )
