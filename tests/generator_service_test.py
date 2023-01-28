from src.generator_service import GeneratorService


class TestGeneratorService:
    def test_generator_service(self):
        start_date = "01/2023"
        end_date = "04/2023"

        new_member = GeneratorService(
            start_date, end_date, "resources/team_members.csv"
        )

        assert new_member
