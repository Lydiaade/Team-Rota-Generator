from datetime import date
from enum import Enum
from typing import List


class Role(Enum):
    PROPRESENTER = "Propresenter"
    LIVESTREAM = "Livestream"
    CAMERA = "Camera"


class Member:
    def __init__(self, name: str, roles: List[Role], unavailable_days: List[date] = []) -> None:
        self.name = name
        self.unavailable_days = unavailable_days
        self.roles = roles


class TeamMembers:
    def __init__(self, team_members: List[Member]):
        self.team_members = team_members

    def available_members(self) -> List[str]:
        return [member.name for member in self.team_members]
