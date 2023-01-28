import datetime
from datetime import date

from src.shifts import get_sundays_between_dates, ShiftService


class TestShiftService:
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

    def test_generate_shifts(self):
        start_date = "01/2023"
        end_date = "02/2023"
        shift_service = ShiftService(
            start_month_year=start_date, end_month_year=end_date
        )

        assert len(shift_service.shifts) == 5

    def test_get_full_shift_dates(self):
        start_date = "01/2023"
        end_date = "02/2023"
        shift_service = ShiftService(
            start_month_year=start_date, end_month_year=end_date
        )

        returned_full_shifts_dates = shift_service.get_full_shift_dates()
        assert len(returned_full_shifts_dates) == 5
        assert returned_full_shifts_dates == [
            "Sunday 01 January 2023",
            "Sunday 08 January 2023",
            "Sunday 15 January 2023",
            "Sunday 22 January 2023",
            "Sunday 29 January 2023",
        ]

    def test_get_iso_shift_dates(self):
        start_date = "01/2023"
        end_date = "02/2023"
        shift_service = ShiftService(
            start_month_year=start_date, end_month_year=end_date
        )

        returned_iso_shifts_dates = shift_service.get_iso_shift_dates()
        assert len(returned_iso_shifts_dates) == 5
        assert returned_iso_shifts_dates == [
            "2023-01-01",
            "2023-01-08",
            "2023-01-15",
            "2023-01-22",
            "2023-01-29",
        ]
