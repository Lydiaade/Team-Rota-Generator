from datetime import date, timedelta
from typing import List


def get_sundays_between_dates(start_date: date, end_date: date) -> List[date]:
    shifts = []
    day = start_date

    day += timedelta(days=(6 - start_date.weekday()))

    # Get all other shifts in year
    while day < end_date:
        if day == day.today():
            day += timedelta(days=7)
        shifts.append(day)
        day += timedelta(days=7)

    return shifts


class ShiftService:
    _shifts: [date]

    def __init__(self, start_month_year: str, end_month_year: str):
        self._shifts = self._generate_shifts(start_month_year, end_month_year)

    def get_iso_shift_dates(self) -> List[str]:
        return [shift.isoformat() for shift in self._shifts]

    def get_full_shift_dates(self) -> List[str]:
        return [shift.strftime("%A %d %B %Y") for shift in self._shifts]

    def _generate_shifts(
        self, start_month_year: str, end_month_year: str
    ) -> List[date]:

        start_date = self._get_date_from_month_year(
            start_month_year
        )  # 1st Day of Month

        start_date = date.today() if start_date < date.today() else start_date

        end_date = self._get_date_from_month_year(end_month_year)

        return get_sundays_between_dates(start_date=start_date, end_date=end_date)

    def _get_date_from_month_year(self, month_year_date: str) -> date:
        return date(
            year=int(month_year_date.split("/")[1]),
            month=int(month_year_date.split("/")[0]),
            day=1,
        )
