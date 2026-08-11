from data_loader import load_job_roles, get_job_role
from skill_matcher import calculate_skill_match
from recommendation_engine import recommend_skills


def main():
    # Load job-role dataset
    data = load_job_roles()

    # Get student's skills from user
    student_input = input(
        "Enter your skills (comma-separated): "
    )

    student_skills = [
        skill.strip()
        for skill in student_input.split(",")
        if skill.strip()
    ]

    # Get target job role from user
    target_role = input(
        "Enter your target job role: "
    ).strip()

    # Find the target role
    job = get_job_role(data, target_role)

    if job is None:
        print(f"\nJob role '{target_role}' was not found.")
        print("\nAvailable roles:")
        for role in data["role"]:
            print(f"  - {role}")
        return

    # Convert required skills from CSV text into a list
    required_skills = [
        skill.strip()
        for skill in job["skills"].split(",")
        if skill.strip()
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

    # Display results
    print("\n===== SkillBridge AI =====")
    print(f"Target Role: {target_role}")

    print("\nSkills You Have:")
    if result["matching_skills"]:
        for skill in result["matching_skills"]:
            print(f"  ✓ {skill}")
    else:
        print("  None")

    print("\nSkills You Need:")
    if result["missing_skills"]:
        for skill in result["missing_skills"]:
            print(f"  ✗ {skill}")
    else:
        print("  None")

    print(
        f"\nSkill Match: {result['match_percentage']}%"
    )

    print("\nRecommended Skills to Learn:")

    if recommended_skills:
        for index, skill in enumerate(
            recommended_skills,
            start=1
        ):
            print(f"  {index}. {skill}")
    else:
        print("  You already have all the required skills!")


if __name__ == "__main__":
    main()