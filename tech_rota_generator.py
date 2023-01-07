from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
from typing import List
from enum import Enum
import random
import csv

start_month = 1
end_month = 7
year = 2023
roles = ["Propresenter", "Livestream", "Camera"]

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

team_members = []
with open('team_members/team_members.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        member_roles = [Role(role) for role in roles if eval(row[role])]
        team_members.append(Member(row["Name"], member_roles))

team = TeamMembers(team_members)

roles = ["Propresenter", "Livestream", "Camera 1", "Camera 2"]

# Create a table Sunday dates between certain time period
def allsundays(start_month: int, end_month: int, year: int) -> list:
    sundays = []

    day = date(year=year, month=start_month, day=1)  # January 1st

    # Gets the first sunday
    day += timedelta(days=(6 - day.weekday()))

    # Get all other sundays in year
    while day < date(year=year, month=end_month, day=1):
        sundays.append(day.isoformat())
        day += timedelta(days=7)

    return sundays


shifts = allsundays(start_month, end_month, year)

# Randomly assign roles to members
rota = []
for index, shift in enumerate(shifts):
    people_on_duty = []
    if index == 0:
        people_on_duty = random.sample(team.available_members(), 3)
    else:
        # Randomly select a person for the role that hasn't done it last week
        options = team.available_members()
        for i in range(3):
            options_for_role = [member for member in team.available_members() if member != rota[index-1][i] and member not in people_on_duty]
            people_on_duty.append(random.choice(options_for_role))
    rota.append([*people_on_duty, ""])

for item in rota:
    print(item)

# # Generate csv table for all the possible roles
# array = np.array(rota)

# df = pd.DataFrame(data=array, index=shifts, columns=roles)
# print(df)
# df.to_csv(f"generated_rotas/{start_month}to{end_month}{year}rota.csv")
