import datetime
from datetime import date

from src.shifts import get_sundays_between_dates


class TestShifts:
    def test_get_sundays_between_dates(self):
        start_date = date(day=1, month=1, year=2023)
        end_date = date(day=31, month=1, year=2023)

        returned_dates = get_sundays_between_dates(start_date, end_date)

        assert len(returned_dates) == 5
        assert returned_dates == [
            datetime.date(2023, 1, 1),
            datetime.date(2023, 1, 8),
            datetime.date(2023, 1, 15),
            datetime.date(2023, 1, 22),
            datetime.date(2023, 1, 29),
        ]
