import csv
from datetime import date
from enum import Enum
from typing import List

from dateutil.parser import parse

roles = ["Propresenter", "Livestream", "Camera"]


class Role(Enum):
    PROPRESENTER = "Propresenter"
    LIVESTREAM = "Livestream"
    CAMERA = "Camera"


class Member:
    name: str
    unavailable_days: List[str]
    roles: List[Role]

    def __init__(self, row: dict) -> None:
        self.name = row["Name"]
        self._extract_roles(row)
        self._extract_unavailable_days(row)

    def _extract_roles(self, row: dict):
        self.roles = [Role(role) for role in roles if eval(row[role])]

    def _extract_unavailable_days(self, row: dict):
        self.unavailable_days = [parse(day).date().isoformat() for day in row["Unavailability"].split()]


class TeamMembers:
    team_members: List[Member]

    def __init__(self, filename: str):
        self._extract_members_from_csv(filename)

    def get_available_qualified_members(self, role: str, members_already_on_duty: List[str], date: str) -> List[str]:
        available_members = []
        for member in self.team_members:
            if member.name in members_already_on_duty:
                pass
            elif date in member.unavailable_days:
                pass
            elif Role(role) in member.roles:
                available_members.append(member.name)
        return available_members

    def _extract_members_from_csv(self, filename: str):
        members = []
        with open(f'team_members/{filename}', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                members.append(Member(row))

        self.team_members = members
