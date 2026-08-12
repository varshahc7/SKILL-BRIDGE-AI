from flask import Flask, render_template, request

from src.data_loader import load_job_roles, get_job_role
from src.skill_matcher import calculate_skill_match
from src.recommendation_engine import recommend_skills
from src.learning_roadmap import LEARNING_ROADMAP
from src.career_readiness import calculate_readiness
from src.career_analysis import generate_career_summary


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        # Load job-role dataset
        data = load_job_roles()

        # Get skills from user
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

        if job is None:

            result = {
                "error": f"Job role '{target_role}' was not found."
            }

            return render_template(
                "index.html",
                result=result
            )

        # Convert required skills into a list
        required_skills = [
            skill.strip()
            for skill in job["skills"].split(",")
            if skill.strip()
        ]

        # Calculate skill match
        match_result = calculate_skill_match(
            student_skills,
            required_skills
        )

        # Get missing skills
        missing_skills = match_result["missing_skills"]

        # Recommend skills
        recommended_skills = recommend_skills(
            missing_skills
        )

        # Calculate career readiness
        readiness = calculate_readiness(
            match_result["match_percentage"]
        )

        # Generate career analysis
        career_analysis = generate_career_summary(
            target_role,
            match_result["match_percentage"],
            readiness,
            missing_skills
        )

        # Create learning roadmap
        roadmap = {}

        for skill in recommended_skills:

            topics = LEARNING_ROADMAP.get(
                skill.lower()
            )

            if topics:
                roadmap[skill] = topics

        # Final result sent to website
        result = {

            "target_role": target_role,

            "match_percentage":
                match_result["match_percentage"],

            "matching_skills":
                match_result["matching_skills"],

            "missing_skills":
                missing_skills,

            "recommended_skills":
                recommended_skills,

            "readiness":
                readiness,

            "roadmap":
                roadmap,

            "career_analysis":
                career_analysis
        }

    return render_template(
        "index.html",
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)