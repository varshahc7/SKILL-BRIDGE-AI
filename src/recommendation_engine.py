def recommend_skills(missing_skills, priority_order=None):
    """
    Recommend which missing skills the student should learn first.
    """

    if not missing_skills:
        return []

    if priority_order:
        priority_map = {
            skill.lower(): index
            for index, skill in enumerate(priority_order)
        }

        return sorted(
            missing_skills,
            key=lambda skill: priority_map.get(skill.lower(), 999)
        )

    return sorted(missing_skills)