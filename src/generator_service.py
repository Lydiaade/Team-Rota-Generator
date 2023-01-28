import random

import numpy as np
import pandas as pd

from shifts import ShiftService
from team import TeamMembers, roles


class GeneratorService:
    def __init__(
        self,
        start_month_year: str,
        end_month_year: str,
        team_members_csv: str = "team_members.csv",
    ):
        self.start_month_year = start_month_year
        self.end_month_year = end_month_year
        self.team_members_csv = team_members_csv

    def generate_rota(self):
        shift_service = ShiftService(self.start_month_year, self.end_month_year)
        team = TeamMembers(self.team_members_csv)

        rota = self._assign_roles_to_members(shift_service, team)

        # Log number of shifts per person
        for member in team.team_members:
            print(f"{member.name} {member.total_role_count}")
            print(f"Total number of shifts: {sum(member.total_role_count.values())}")

        # Generate csv table for all the possible roles
        df = self._generate_rota_df(rota, shift_service)

        self._export_df(df)

    def _export_df(self, df: pd.DataFrame):
        filename = f"{self.start_month_year.replace('/', '_')}to{self.end_month_year.replace('/', '_')}rota.csv"
        print(f"File name: {filename}")
        df.to_csv(f"generated_rotas/{filename}")

    def _generate_rota_df(
        self, rota: list, shift_service: ShiftService
    ) -> pd.DataFrame:
        positions = ["Propresenter", "Livestream", "Camera 1", "Camera 2"]
        array = np.array(rota)
        df = pd.DataFrame(
            data=array, index=shift_service.get_full_shift_dates(), columns=positions
        )
        return df

    def _assign_roles_to_members(
        self, shift_service: ShiftService, team: TeamMembers
    ) -> list:
        # Randomly assign roles to members
        rota = []
        while not rota:
            try:
                for index, date in enumerate(shift_service.shifts):
                    team.assign_off_days(date)
                    members_on_duty = []
                    for i, role in enumerate(roles):
                        previously_on_duty = rota[index - 1][i] if index != 0 else None
                        qualified_members = team.get_available_qualified_members(
                            role, members_on_duty, date, previously_on_duty
                        )
                        member_on_duty = random.choice(qualified_members)
                        member_on_duty.log_role_count(role)
                        members_on_duty.append(member_on_duty.name)
                    rota.append([*members_on_duty, ""])
            except IndexError:
                rota = []
                team.reset_all_values()
        return rota
