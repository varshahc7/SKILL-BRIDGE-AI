from flask import Flask, render_template, request

from src.data_loader import load_job_roles, get_job_role
from src.skill_matcher import calculate_skill_match
from src.recommendation_engine import recommend_skills
from src.career_readiness import calculate_readiness
from src.career_analysis import generate_career_summary
from src.learning_roadmap import LEARNING_ROADMAP


app = Flask(__name__)

data = load_job_roles()


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        student_input = request.form["skills"]
        target_role = request.form["job_role"]

        student_skills = [
            skill.strip()
            for skill in student_input.split(",")
            if skill.strip()
        ]

        job = get_job_role(data, target_role)

        if job is not None:
            required_skills = [
                skill.strip()
                for skill in job["skills"].split(",")
                if skill.strip()
            ]

            result = calculate_skill_match(
                student_skills,
                required_skills
            )

            recommended_skills = recommend_skills(
                result["missing_skills"]
            )

            readiness_level = calculate_readiness(
                result["match_percentage"]
            )

            career_summary = generate_career_summary(
                target_role,
                result["match_percentage"],
                readiness_level,
                result["missing_skills"]
            )

            roadmap = {}

            for skill in recommended_skills:
                topics = LEARNING_ROADMAP.get(
                    skill.lower(),
                    []
                )

                if topics:
                    roadmap[skill] = topics

            result["recommended_skills"] = recommended_skills
            result["readiness_level"] = readiness_level
            result["career_summary"] = career_summary
            result["roadmap"] = roadmap
            result["target_role"] = target_role

        else:
            result = {
                "error": f"Job role '{target_role}' was not found."
            }

    roles = data["role"].tolist()

    return render_template(
        "index.html",
        roles=roles,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)