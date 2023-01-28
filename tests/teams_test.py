import datetime

from src.team import Member, Role


class TestMember:
    def test_generate_member_info(self):
        member_info = {
            "Name": "Example Person",
            "Propresenter": "True",
            "Livestream": "True",
            "Camera": "False",
            "Unavailability": "22/01/2023",
        }

        new_member = Member(member_info)

        assert new_member.name == "Example Person"
        assert len(new_member.roles) == 2
        assert Role.LIVESTREAM in new_member.roles
        assert Role.PROPRESENTER in new_member.roles
        assert new_member.unavailable_days == [datetime.date(2023, 1, 22)]
