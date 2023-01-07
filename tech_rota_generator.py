import os
import random
import sys

import numpy as np
import pandas as pd

from shifts import generate_shifts
from team import TeamMembers, roles


def generate_rota(start_month_year: str, end_month_year: str, team_members_csv: str = "team_members.csv"):
    shifts = generate_shifts(start_month_year, end_month_year)
    team = TeamMembers(team_members_csv)

    # Randomly assign roles to members
    rota = []
    while not rota:
        try:
            for index, date in enumerate(shifts):
                team.assign_off_days(date)
                members_on_duty = []
                for i, role in enumerate(roles):
                    previously_on_duty = rota[index - 1][i] if index != 0 else None
                    qualified_members = team.get_available_qualified_members(role, members_on_duty, date,
                                                                             previously_on_duty)
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
    filename = f"{start_month_year.replace('/','_')}to{end_month_year.replace('/','_')}rota.csv"
    print(f"File name: {filename}")
    df.to_csv(f"generated_rotas/{filename}")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        generate_rota(start_month_year=sys.argv[1], end_month_year=sys.argv[2])
    elif len(sys.argv) == 4:
        generate_rota(start_month_year=sys.argv[1], end_month_year=sys.argv[2], team_members_csv=sys.argv[3])
    else:
        print(
            "To use this script you would need to input the following:")
        print("1: Start month and year")
        print("2: End month and year")
        print("3: Team members csv file, if not the default will be used.")
        print("Note: If used it must be placed in the team members folder")
        print(f"python {os.path.basename(__file__)} start_month_and_year end_month_and_year team_members_csv_file_name")
        print("Example:")
        print(f"python {os.path.basename(__file__)} 01/2023 07/2023 team_members.csv")
