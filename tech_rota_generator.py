import random

import numpy as np
import pandas as pd

from team import TeamMembers, roles
from shifts import generate_shifts

start_month = 1
end_month = 7
year = 2023

team = TeamMembers("team_members.csv")

shifts = generate_shifts(start_month, end_month, year)

# Randomly assign roles to members
rota = []
for index, date in enumerate(shifts):
    members_on_duty = []
    for i, role in enumerate(roles):
        options_for_role = []
        qualified_members = team.get_available_qualified_members(role, members_on_duty, date)
        for member in qualified_members:
            if index == 0:
                options_for_role.append(member)
            elif member != rota[index - 1][i]:
                options_for_role.append(member)
        members_on_duty.append(random.choice(options_for_role))
    rota.append([*members_on_duty, ""])

# Generate csv table for all the possible roles
positions = ["Propresenter", "Livestream", "Camera 1", "Camera 2"]
array = np.array(rota)

df = pd.DataFrame(data=array, index=shifts, columns=positions)
print(df)
df.to_csv(f"generated_rotas/{start_month}to{end_month}{year}rota.csv")
