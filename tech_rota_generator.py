import csv
import random

import numpy as np
import pandas as pd

from members import Role, Member, TeamMembers
from shifts import generate_shifts

start_month = 1
end_month = 7
year = 2023
roles = ["Propresenter", "Livestream", "Camera"]


def extract_members_from_csv(filename: str) -> TeamMembers:
    members = []
    with open(f'team_members/{filename}', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            member_roles = [Role(role) for role in roles if eval(row[role])]
            members.append(Member(row["Name"], member_roles))

    return TeamMembers(members)


team = extract_members_from_csv("team_members.csv")

shifts = generate_shifts(start_month, end_month, year)

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
            options_for_role = [member for member in team.available_members() if
                                member != rota[index - 1][i] and member not in people_on_duty]
            people_on_duty.append(random.choice(options_for_role))
    rota.append([*people_on_duty, ""])

# Generate csv table for all the possible roles
positions = ["Propresenter", "Livestream", "Camera 1", "Camera 2"]
array = np.array(rota)

df = pd.DataFrame(data=array, index=shifts, columns=positions)
print(df)
df.to_csv(f"generated_rotas/{start_month}to{end_month}{year}rota.csv")
