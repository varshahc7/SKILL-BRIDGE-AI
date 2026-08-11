def calculate_skill_match(student_skills, required_skills):
    """
    Compare a student's skills with the skills required for a job role.

    Returns the matching skills, missing skills, and match percentage.
    """

    student_skills = {skill.strip().lower() for skill in student_skills}
    required_skills = {skill.strip().lower() for skill in required_skills}

    matching_skills = student_skills.intersection(required_skills)
    missing_skills = required_skills - student_skills

    if not required_skills:
        match_percentage = 0
    else:
        match_percentage = (len(matching_skills) / len(required_skills)) * 100

    return {
        "matching_skills": sorted(matching_skills),
        "missing_skills": sorted(missing_skills),
        "match_percentage": round(match_percentage, 2),
    }