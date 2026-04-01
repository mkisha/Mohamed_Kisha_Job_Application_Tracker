from flask import Flask, render_template, request, redirect, url_for, flash
from database import (
    get_dashboard_stats,
    get_all_companies, get_company, add_company, update_company, delete_company,
    get_all_jobs, get_job, add_job, update_job, delete_job,
    get_all_applications, get_application, add_application, update_application, delete_application,
    get_all_contacts, get_contact, add_contact, update_contact, delete_contact,
    get_job_match_results
)

app = Flask(__name__)
app.secret_key = "job_tracker_secret_key"


@app.route("/")
def dashboard():
    stats = get_dashboard_stats()
    return render_template("dashboard.html", stats=stats)


# ---------------- Companies ----------------
@app.route("/companies")
def companies():
    companies_list = get_all_companies()
    return render_template("companies.html", companies=companies_list)


@app.route("/companies/add", methods=["GET", "POST"])
def company_add():
    if request.method == "POST":
        add_company(request.form)
        flash("Company added successfully.")
        return redirect(url_for("companies"))
    return render_template("company_form.html", company=None)


@app.route("/companies/edit/<int:company_id>", methods=["GET", "POST"])
def company_edit(company_id):
    company = get_company(company_id)
    if not company:
        flash("Company not found.")
        return redirect(url_for("companies"))

    if request.method == "POST":
        update_company(company_id, request.form)
        flash("Company updated successfully.")
        return redirect(url_for("companies"))

    return render_template("company_form.html", company=company)


@app.route("/companies/delete/<int:company_id>", methods=["POST"])
def company_delete(company_id):
    delete_company(company_id)
    flash("Company deleted successfully.")
    return redirect(url_for("companies"))


# ---------------- Jobs ----------------
@app.route("/jobs")
def jobs():
    jobs_list = get_all_jobs()
    return render_template("jobs.html", jobs=jobs_list)


@app.route("/jobs/add", methods=["GET", "POST"])
def job_add():
    companies_list = get_all_companies()

    if request.method == "POST":
        add_job(request.form)
        flash("Job added successfully.")
        return redirect(url_for("jobs"))

    return render_template("job_form.html", job=None, companies=companies_list)


@app.route("/jobs/edit/<int:job_id>", methods=["GET", "POST"])
def job_edit(job_id):
    job = get_job(job_id)
    companies_list = get_all_companies()

    if not job:
        flash("Job not found.")
        return redirect(url_for("jobs"))

    if request.method == "POST":
        add_requirements_string = request.form.get("requirements", "")
        request.form = request.form.copy()
        request.form["requirements"] = add_requirements_string
        update_job(job_id, request.form)
        flash("Job updated successfully.")
        return redirect(url_for("jobs"))

    return render_template("job_form.html", job=job, companies=companies_list)


@app.route("/jobs/delete/<int:job_id>", methods=["POST"])
def job_delete(job_id):
    delete_job(job_id)
    flash("Job deleted successfully.")
    return redirect(url_for("jobs"))


# ---------------- Applications ----------------
@app.route("/applications")
def applications():
    applications_list = get_all_applications()
    return render_template("applications.html", applications=applications_list)


@app.route("/applications/add", methods=["GET", "POST"])
def application_add():
    jobs_list = get_all_jobs()

    if request.method == "POST":
        add_application(request.form)
        flash("Application added successfully.")
        return redirect(url_for("applications"))

    return render_template("application_form.html", application=None, jobs=jobs_list)


@app.route("/applications/edit/<int:application_id>", methods=["GET", "POST"])
def application_edit(application_id):
    application = get_application(application_id)
    jobs_list = get_all_jobs()

    if not application:
        flash("Application not found.")
        return redirect(url_for("applications"))

    if request.method == "POST":
        update_application(application_id, request.form)
        flash("Application updated successfully.")
        return redirect(url_for("applications"))

    return render_template(
        "application_form.html",
        application=application,
        jobs=jobs_list
    )


@app.route("/applications/delete/<int:application_id>", methods=["POST"])
def application_delete(application_id):
    delete_application(application_id)
    flash("Application deleted successfully.")
    return redirect(url_for("applications"))


# ---------------- Contacts ----------------
@app.route("/contacts")
def contacts():
    contacts_list = get_all_contacts()
    return render_template("contacts.html", contacts=contacts_list)


@app.route("/contacts/add", methods=["GET", "POST"])
def contact_add():
    companies_list = get_all_companies()

    if request.method == "POST":
        add_contact(request.form)
        flash("Contact added successfully.")
        return redirect(url_for("contacts"))

    return render_template("contact_form.html", contact=None, companies=companies_list)


@app.route("/contacts/edit/<int:contact_id>", methods=["GET", "POST"])
def contact_edit(contact_id):
    contact = get_contact(contact_id)
    companies_list = get_all_companies()

    if not contact:
        flash("Contact not found.")
        return redirect(url_for("contacts"))

    if request.method == "POST":
        update_contact(contact_id, request.form)
        flash("Contact updated successfully.")
        return redirect(url_for("contacts"))

    return render_template("contact_form.html", contact=contact, companies=companies_list)


@app.route("/contacts/delete/<int:contact_id>", methods=["POST"])
def contact_delete(contact_id):
    delete_contact(contact_id)
    flash("Contact deleted successfully.")
    return redirect(url_for("contacts"))


# ---------------- Job Match ----------------
@app.route("/job-match", methods=["GET", "POST"])
def job_match():
    results = []
    user_skills = ""

    if request.method == "POST":
        user_skills = request.form.get("skills", "")
        skill_list = [skill.strip() for skill in user_skills.split(",") if skill.strip()]
        results = get_job_match_results(skill_list)

    return render_template("job_match.html", results=results, user_skills=user_skills)


if __name__ == "__main__":
    app.run(debug=True)