from flask import Flask, render_template, request

from src.data_loader import (
    load_job_roles,
    get_job_role
)

from src.skill_matcher import (
    calculate_skill_match
)

from src.recommendation_engine import (
    recommend_skills
)

from src.learning_roadmap import (
    LEARNING_ROADMAP
)

from src.career_readiness import (
    calculate_readiness
)

from src.career_analysis import (
    generate_career_summary
)


app = Flask(__name__)


# =========================================================
# LOAD JOB DATA
# =========================================================

data = load_job_roles()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    result = None


    # =====================================================
    # WHEN USER SUBMITS FORM
    # =====================================================

    if request.method == "POST":


        # -------------------------------------------------
        # GET SKILLS FROM FORM
        # -------------------------------------------------

        student_input = request.form.get(
            "skills",
            ""
        )


        # Convert comma-separated skills
        # into a Python list

        student_skills = [
            skill.strip()
            for skill in student_input.split(",")
            if skill.strip()
        ]


        # -------------------------------------------------
        # GET TARGET ROLE
        # -------------------------------------------------

        target_role = request.form.get(
            "role",
            ""
        ).strip()


        # -------------------------------------------------
        # FIND JOB ROLE
        # -------------------------------------------------

        job = get_job_role(
            data,
            target_role
        )


        # -------------------------------------------------
        # INVALID ROLE
        # -------------------------------------------------

        if job is None:

            return render_template(
                "index.html",
                result=None,
                error=(
                    f"Job role '{target_role}' "
                    "was not found."
                )
            )


        # -------------------------------------------------
        # REQUIRED SKILLS
        # -------------------------------------------------

        required_skills = [

            skill.strip()

            for skill in job["skills"].split(",")

            if skill.strip()

        ]


        # -------------------------------------------------
        # CALCULATE SKILL MATCH
        # -------------------------------------------------

        match_result = calculate_skill_match(

            student_skills,

            required_skills

        )


        # -------------------------------------------------
        # RECOMMEND SKILLS
        # -------------------------------------------------

        recommended_skills = recommend_skills(

            match_result[
                "missing_skills"
            ]

        )


        # -------------------------------------------------
        # CAREER READINESS
        # -------------------------------------------------

        readiness = calculate_readiness(

            match_result[
                "match_percentage"
            ]

        )


        # -------------------------------------------------
        # LEARNING ROADMAP
        # -------------------------------------------------

        roadmap = {}


        for skill in recommended_skills:

            topics = LEARNING_ROADMAP.get(
                skill.lower()
            )


            if topics:

                roadmap[skill] = topics


        # -------------------------------------------------
        # CAREER ANALYSIS
        # -------------------------------------------------

        career_analysis = generate_career_summary(

            target_role,

            match_result[
                "match_percentage"
            ],

            readiness,

            match_result[
                "missing_skills"
            ]

        )


        # -------------------------------------------------
        # COMBINE EVERYTHING
        # -------------------------------------------------

        result = {

            "match_percentage":
                match_result[
                    "match_percentage"
                ],

            "readiness":
                readiness,

            "matching_skills":
                match_result[
                    "matching_skills"
                ],

            "missing_skills":
                match_result[
                    "missing_skills"
                ],

            "recommended_skills":
                recommended_skills,

            "roadmap":
                roadmap,

            "career_analysis":
                career_analysis,
            "target_role": target_role,
            

        }


    # =====================================================
    # DISPLAY PAGE
    # =====================================================

    return render_template(

        "index.html",

        result=result

    )


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )