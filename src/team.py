import csv
import re
from datetime import datetime, date
from enum import Enum
from typing import List, Dict

from src.shifts import get_sundays_between_dates

roles = ["Propresenter", "Livestream", "Camera"]


class Role(Enum):
    PROPRESENTER = "Propresenter"
    LIVESTREAM = "Livestream"
    CAMERA = "Camera"


class Member:
    name: str
    unavailable_days: List[date]
    roles: List[Role]
    at_risk_of_overworking = bool
    repeated_shift_count = 0
    monitored_role_count: Dict[str, int]
    total_role_count: Dict[str, int]
    off_days: [str]

    def __init__(self, row: dict) -> None:
        self.name = row["Name"]
        self._extract_roles(row)
        self._extract_unavailable_days(row)
        self.at_risk_of_overworking = len(self.roles) == len(roles)
        self.reset_values()

    def log_role_count(self, role: str) -> None:
        self.monitored_role_count[role] += 1
        self.total_role_count[role] += 1
        self.repeated_shift_count += 1

    def reset_values(self):
        self.monitored_role_count = {role.value: 0 for role in self.roles}
        self.total_role_count = {role.value: 0 for role in self.roles}
        self.repeated_shift_count = 0
        self.off_days = []

    def _extract_roles(self, row: dict) -> None:
        self.roles = [Role(role) for role in roles if eval(row[role])]

    def _extract_unavailable_days(self, row: dict) -> None:
        unavailable = []
        for dates in row["Unavailability"].split():
            if re.match(r"[0-9]*\/[0-9]*\/[0-9]{4}-[0-9]*\/[0-9]*\/[0-9]{4}", dates):
                start_end_dates = [
                    datetime.strptime(day, "%d/%m/%Y").date()
                    for day in dates.split("-")
                ]
                unavailable_dates = get_sundays_between_dates(*start_end_dates)
                unavailable.extend(unavailable_dates)
            else:
                unavailable.append(datetime.strptime(dates, "%d/%m/%Y").date())

        # unavailable = [day for day in unavailable if day > date.today()]
        self.unavailable_days = unavailable


class TeamMembers:
    team_members: List[Member]

    def __init__(self, filename: str) -> None:
        self._extract_members_from_csv(filename)

    def get_available_qualified_members(
        self,
        role: str,
        members_already_on_duty: List[str],
        shift_date: date,
        previously_on_duty: str,
    ) -> List[Member]:

        available_members = self.generate_available_members(
            members_already_on_duty, previously_on_duty, role, shift_date
        )

        if len(available_members) <= len(self._get_specific_members_for_role(role)):
            self._reset_role_count(role)
            available_members = self.generate_available_members(
                members_already_on_duty, previously_on_duty, role, shift_date
            )
        return available_members

    def generate_available_members(
        self, members_already_on_duty, previously_on_duty, role, shift_date
    ):
        available_members = []
        for member in self._get_members_for_role(role):
            if (
                member.name in members_already_on_duty
                or shift_date in member.unavailable_days
                or member.name == previously_on_duty
                or shift_date in member.off_days
            ):
                pass
            elif member.at_risk_of_overworking:
                if member.monitored_role_count[role] < 3:
                    available_members.append(member)
            else:
                available_members.append(member)
        return available_members

    def assign_off_days(self, shift_date: date):
        for member in self.team_members:
            if member.repeated_shift_count > 3:
                member.off_days.append(shift_date)
                member.repeated_shift_count = 0

    def reset_all_values(self):
        for member in self.team_members:
            member.reset_values()

    def _get_members_for_role(self, role: str) -> List[Member]:
        return [member for member in self.team_members if Role(role) in member.roles]

    def _get_specific_members_for_role(self, role: str) -> List[Member]:
        return [
            member
            for member in self.team_members
            if Role(role) in member.roles and len(member.roles) == 1
        ]

    def _reset_role_count(self, role: str) -> None:
        for member in self._get_members_for_role(role):
            member.monitored_role_count[role] = 0

    def _extract_members_from_csv(self, filename: str) -> None:
        members = []
        with open(f"resources/team_members/{filename}", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                members.append(Member(row))

        self.team_members = members
