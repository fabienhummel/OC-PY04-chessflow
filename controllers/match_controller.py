from persistence.json_repository import save_tournament


class MatchController:
    """Manage match results."""

    @staticmethod
    def validate_result(score_one, score_two):
        """Validate and normalize a match result."""
        try:
            score_one = float(str(score_one).replace(",", "."))
            score_two = float(str(score_two).replace(",", "."))
        except ValueError:
            raise ValueError("Scores must be numbers.") from None

        if (score_one, score_two) not in ((1, 0), (0, 1), (0.5, 0.5)):
            raise ValueError("Valid results are 1-0, 0-1 or 0.5-0.5.")

        return score_one, score_two

    def record_result(self, tournament, match, score_one, score_two):
        """Validate and record a match result."""
        score_one, score_two = self.validate_result(score_one, score_two)
        match.set_result(score_one, score_two)
        save_tournament(tournament, f"{tournament.name}.json")
