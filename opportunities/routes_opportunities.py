"""Routes for opportunites"""

import uuid
from flask import flash, redirect, render_template, request, session, url_for
from core import handlers
from course_modules.models import Module
from courses.models import Course
from employers.models import Employers
from .models import Opportunity


def add_opportunities_routes(app):
    """Add routes for opportunities"""

    @app.route("/opportunities/search", methods=["GET", "POST"])
    @handlers.admin_or_employers_required
    def search_opportunities():
        if request.method == "POST":
            return Opportunity().search_opportunities()

        user_type= ""
        if "user" in session:
            user_type = "admin"
        if "employer" in session:
            user_type = session["employer"]["_id"]

        opportunities = Opportunity().get_opportunities_by_company(user_type)

        return render_template(
            "opportunities/search.html",
            opportunities=opportunities,
            company_name=Employers().get_company_name,
            user_type=user_type,
        )

    @app.route(
        "/opportunities/employer_add_update_opportunity", methods=["GET", "POST"]
    )
    @handlers.admin_or_employers_required
    def employer_add_update_opportunity():
        if request.method == "POST":
            return Opportunity().add_update_opportunity()
        opportunity_id = request.args.get("opportunity_id")
        if opportunity_id is not None:
            opportunity = Opportunity().get_opportunity_by_id(opportunity_id)
        else:
            opportunity = {"_id": uuid.uuid1().hex}

        return render_template(
            "opportunities/employer_add_update_opportunity.html",
            opportunity=opportunity,
            courses=Course().get_courses(),
            modules=Module().get_modules(),
        )

    @app.route("/opportunities/employer_delete_opportunity", methods=["POST"])
    @handlers.admin_or_employers_required
    def employer_delete_opportunity():
        opportunity_id = request.args.get("opportunity_id")
        if not opportunity_id:
            flash("Opportunity ID is required", "error")
            return redirect(request.referrer)

        Opportunity().delete_opportunity_by_id(opportunity_id)
        flash("Opportunity deleted successfully", "success")
        return redirect(url_for("search_opportunities"))
