import os
import sys

from generator_service import GeneratorService

if __name__ == "__main__":
    if len(sys.argv) == 3:
        GeneratorService(
            start_month_year=sys.argv[1], end_month_year=sys.argv[2]
        ).generate_rota()
    elif len(sys.argv) == 4:
        GeneratorService(
            start_month_year=sys.argv[1],
            end_month_year=sys.argv[2],
            team_members_csv=sys.argv[3],
        ).generate_rota()
    else:
        print("\nTo use this script you would need to input the following:")
        print("1: Start month and year")
        print("2: End month and year")
        print("3: Team members csv file, if not the default will be used.")
        print("Note: If used it must be placed in the team members folder\n")
        print("Example:")
        print(
            f"python {os.path.basename(__file__)} start_month_and_year end_month_and_year team_members_csv_file_name"
        )
        print(f"python {os.path.basename(__file__)} 01/2023 07/2023 team_members.csv")
