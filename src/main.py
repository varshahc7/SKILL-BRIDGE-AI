from data_loader import load_job_roles, get_job_role
from skill_matcher import calculate_skill_match
from recommendation_engine import recommend_skills


def main():
    # Load job-role dataset
    data = load_job_roles()

    # Example student profile
    student_skills = [
        "Python",
        "Pandas",
        "NumPy",
        "Git"
    ]

    # Target job role
    target_role = "Machine Learning Engineer"

    # Find the target role
    job = get_job_role(data, target_role)

    if job is None:
        print(f"Job role '{target_role}' was not found.")
        return

    # Convert required skills from CSV text into a list
    required_skills = [
        skill.strip()
        for skill in job["skills"].split(",")
    ]

    # Calculate skill match
    result = calculate_skill_match(
        student_skills,
        required_skills
    )

    # Generate skill recommendations
    recommended_skills = recommend_skills(
        result["missing_skills"]
    )

    print("\n===== SkillBridge AI =====")
    print(f"Target Role: {target_role}")

    print("\nSkills You Have:")
    for skill in result["matching_skills"]:
        print(f"  ✓ {skill}")

    print("\nSkills You Need:")
    for skill in result["missing_skills"]:
        print(f"  ✗ {skill}")

    print(
        f"\nSkill Match: {result['match_percentage']}%"
    )

    print("\nRecommended Skills to Learn:")

    if recommended_skills:
        for index, skill in enumerate(recommended_skills, start=1):
            print(f"  {index}. {skill}")
    else:
        print("  You already have all the required skills!")


if __name__ == "__main__":
    main()