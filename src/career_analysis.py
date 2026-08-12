def generate_career_summary(
    target_role,
    match_percentage,
    readiness_level,
    missing_skills
):
    """
    Generate a concise career analysis summary.
    """

    missing_count = len(missing_skills)

    if missing_count == 0:
        return (
            f"You are well aligned with the {target_role} role. "
            f"Your skill match is {match_percentage}%, "
            f"and your career readiness level is {readiness_level}."
        )

    if missing_count == 1:
        skill_text = "skill"
    else:
        skill_text = "skills"

    return (
        f"You currently match {match_percentage}% of the "
        f"skills required for the {target_role} role. "
        f"You need to develop {missing_count} additional "
        f"{skill_text}. Your current career readiness level "
        f"is {readiness_level}."
    )