from flask import Flask, render_template, request
from src.data_loader import load_job_roles, get_job_role
from src.skill_matcher import calculate_skill_match
from src.recommendation_engine import recommend_skills
from src.learning_roadmap import LEARNING_ROADMAP
from src.career_readiness import calculate_readiness
from src.career_analysis import generate_career_summary
app = Flask(__name__)

# Load job-role dataset once when the application starts
data = load_job_roles()


@app.route("/", methods=["GET", "POST"])
def home():

    # Default values
    result = None
    readiness = None
    recommended_skills = []
    roadmap = {}
    career_analysis = None
    error = None
    suggestions = []

    if request.method == "POST":

        # Get skills from the form
        student_input = request.form.get("skills", "")

        student_skills = [
            skill.strip()
            for skill in student_input.split(",")
            if skill.strip()
        ]

        # Get target role
        target_role = request.form.get("role", "").strip()

        # Find job role
        job = get_job_role(data, target_role)

        # Handle invalid job role
        if job is None:

            error = f"Job role '{target_role}' was not found."

            # Get available roles
            available_roles = data["role"].tolist()

            from difflib import get_close_matches

            suggestions = get_close_matches(
                target_role,
                available_roles,
                n=3,
                cutoff=0.5
            )

        else:

            # Convert required skills from dataset
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

            # Calculate career readiness
            readiness = calculate_readiness(
                result["match_percentage"]
            )

            # Generate recommendations
            recommended_skills = recommend_skills(
                result["missing_skills"]
            )

            # Generate learning roadmap
            for skill in recommended_skills:

                topics = LEARNING_ROADMAP.get(
                    skill.lower()
                )

                if topics:
                    roadmap[skill] = topics

            # Generate career analysis
            career_analysis = generate_career_summary(
                target_role,
                result["match_percentage"],
                readiness,
                result["missing_skills"]
            )

    return render_template(
        "index.html",
        result=result,
        readiness=readiness,
        recommended_skills=recommended_skills,
        roadmap=roadmap,
        career_analysis=career_analysis,
        error=error,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)