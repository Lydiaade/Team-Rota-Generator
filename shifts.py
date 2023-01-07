from datetime import date, timedelta


def generate_shifts(start_month_year: str, end_month_year: str) -> list:
    shifts = []

    day = date(year=int(start_month_year.split('/')[1]), month=int(start_month_year.split('/')[0]), day=1) # 1st Day of Month

    day = date.today() if day <= date.today() else day

    # Gets the first sunday
    day += timedelta(days=(6 - day.weekday()))

    # Get all other shifts in year
    while day < date(year=int(end_month_year.split('/')[1]), month=int(end_month_year.split('/')[0]), day=1):
        shifts.append(day.isoformat())
        day += timedelta(days=7)

    return shifts
