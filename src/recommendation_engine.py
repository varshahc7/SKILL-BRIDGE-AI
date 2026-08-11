def recommend_skills(missing_skills, priority_order=None):
    """
    Recommend which missing skills the student should learn first.
    """

    if not missing_skills:
        return []

    # Default learning priority
    if priority_order is None:
        priority_order = [
            "Python",
            "SQL",
            "Git",
            "Data Structures",
            "APIs",
            "NumPy",
            "Pandas",
            "Statistics",
            "Data Visualization",
            "Machine Learning",
            "Scikit-learn",
            "Deep Learning",
            "NLP",
            "TensorFlow",
            "PyTorch",
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Databases",
            "Docker",
            "CI/CD",
            "Cloud",
            "Linux",
            "Networking",
        ]

    # Create a priority lookup
    priority_map = {
        skill.lower(): index
        for index, skill in enumerate(priority_order)
    }

    # Sort missing skills by learning priority
    return sorted(
        missing_skills,
        key=lambda skill: priority_map.get(
            skill.lower(),
            999
        )
    )