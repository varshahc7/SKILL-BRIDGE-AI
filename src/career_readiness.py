def calculate_readiness(match_percentage):
    """
    Determine the student's career readiness level
    based on their skill match percentage.
    """

    if match_percentage >= 80:
        return "Job Ready"

    if match_percentage >= 60:
        return "Nearly Ready"

    if match_percentage >= 40:
        return "Developing"

    return "Needs Improvement"