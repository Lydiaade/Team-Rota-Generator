from datetime import date, timedelta


def generate_shifts(start_month: int, end_month: int, year: int) -> list:
    shifts = []

    day = date(year=year, month=start_month, day=1)  # January 1st

    # Gets the first sunday
    day += timedelta(days=(6 - day.weekday()))

    # Get all other shifts in year
    while day < date(year=year, month=end_month, day=1):
        shifts.append(day.isoformat())
        day += timedelta(days=7)

    return shifts

