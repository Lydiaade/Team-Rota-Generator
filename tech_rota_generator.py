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
while not rota:
    try:
        for index, date in enumerate(shifts):
            team.assign_off_days(date)
            members_on_duty = []
            for i, role in enumerate(roles):
                previously_on_duty = rota[index - 1][i] if index != 0 else None
                qualified_members = team.get_available_qualified_members(role, members_on_duty, date, previously_on_duty)
                member_on_duty = random.choice(qualified_members)
                member_on_duty.log_role_count(role)
                members_on_duty.append(member_on_duty.name)
            rota.append([*members_on_duty, ""])
    except IndexError:
        rota = []
        team.reset_all_values()

# Generate csv table for all the possible roles
positions = ["Propresenter", "Livestream", "Camera 1", "Camera 2"]
array = np.array(rota)

df = pd.DataFrame(data=array, index=shifts, columns=positions)
print(df)
df.to_csv(f"generated_rotas/{start_month}to{end_month}{year}rota.csv")
