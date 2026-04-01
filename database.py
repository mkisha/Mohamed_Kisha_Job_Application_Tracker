import json
import mysql.connector


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mohamedk.94",
        database="job_tracker"
    )


def execute_query(query, params=None, fetchone=False, fetchall=False):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())

    result = None
    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return result


def bool_from_form(value):
    return 1 if value in ("on", "true", "1", 1, True) else 0


def parse_skills_to_json(skills_text):
    if not skills_text:
        return json.dumps([])
    skills_list = [skill.strip() for skill in skills_text.split(",") if skill.strip()]
    return json.dumps(skills_list)


def parse_json_input(text):
    if not text or not text.strip():
        return None
    try:
        parsed = json.loads(text)
        return json.dumps(parsed)
    except json.JSONDecodeError:
        return json.dumps({"notes": text})


def json_to_display_string(value):
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            loaded = json.loads(value)
        except json.JSONDecodeError:
            return value
    else:
        loaded = value

    if isinstance(loaded, list):
        return ", ".join(str(item) for item in loaded)
    return json.dumps(loaded, indent=2)


# ---------------- Dashboard ----------------
def get_dashboard_stats():
    total_companies = execute_query(
        "SELECT COUNT(*) AS total FROM companies",
        fetchone=True
    )["total"]

    total_jobs = execute_query(
        "SELECT COUNT(*) AS total FROM jobs",
        fetchone=True
    )["total"]

    total_applications = execute_query(
        "SELECT COUNT(*) AS total FROM applications",
        fetchone=True
    )["total"]

    total_contacts = execute_query(
        "SELECT COUNT(*) AS total FROM contacts",
        fetchone=True
    )["total"]

    status_breakdown = execute_query(
        """
        SELECT status, COUNT(*) AS total
        FROM applications
        GROUP BY status
        ORDER BY total DESC
        """,
        fetchall=True
    )

    return {
        "total_companies": total_companies,
        "total_jobs": total_jobs,
        "total_applications": total_applications,
        "total_contacts": total_contacts,
        "status_breakdown": status_breakdown
    }


# ---------------- Companies ----------------
def get_all_companies():
    return execute_query(
        "SELECT * FROM companies ORDER BY company_name ASC",
        fetchall=True
    )


def get_company(company_id):
    return execute_query(
        "SELECT * FROM companies WHERE company_id = %s",
        (company_id,),
        fetchone=True
    )


def add_company(form_data):
    query = """
        INSERT INTO companies (
            company_name, industry, website, city, state, notes
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        form_data.get("company_name"),
        form_data.get("industry"),
        form_data.get("website"),
        form_data.get("city"),
        form_data.get("state"),
        form_data.get("notes")
    )
    execute_query(query, params)


def update_company(company_id, form_data):
    query = """
        UPDATE companies
        SET company_name = %s,
            industry = %s,
            website = %s,
            city = %s,
            state = %s,
            notes = %s
        WHERE company_id = %s
    """
    params = (
        form_data.get("company_name"),
        form_data.get("industry"),
        form_data.get("website"),
        form_data.get("city"),
        form_data.get("state"),
        form_data.get("notes"),
        company_id
    )
    execute_query(query, params)


def delete_company(company_id):
    execute_query(
        "DELETE FROM companies WHERE company_id = %s",
        (company_id,)
    )


# ---------------- Jobs ----------------
def get_all_jobs():
    jobs = execute_query(
        """
        SELECT j.*, c.company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY j.date_posted DESC, j.job_id DESC
        """,
        fetchall=True
    )

    for job in jobs:
        job["requirements_display"] = json_to_display_string(job.get("requirements"))

    return jobs


def get_job(job_id):
    job = execute_query(
        "SELECT * FROM jobs WHERE job_id = %s",
        (job_id,),
        fetchone=True
    )
    if job:
        job["requirements_display"] = json_to_display_string(job.get("requirements"))
    return job


def add_job(form_data):
    query = """
        INSERT INTO jobs (
            company_id, job_title, job_type, salary_min, salary_max,
            job_url, date_posted, requirements
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        form_data.get("company_id"),
        form_data.get("job_title"),
        form_data.get("job_type"),
        form_data.get("salary_min") or None,
        form_data.get("salary_max") or None,
        form_data.get("job_url"),
        form_data.get("date_posted") or None,
        parse_skills_to_json(form_data.get("requirements"))
    )
    execute_query(query, params)


def update_job(job_id, form_data):
    query = """
        UPDATE jobs
        SET company_id = %s,
            job_title = %s,
            job_type = %s,
            salary_min = %s,
            salary_max = %s,
            job_url = %s,
            date_posted = %s,
            requirements = %s
        WHERE job_id = %s
    """
    params = (
        form_data.get("company_id"),
        form_data.get("job_title"),
        form_data.get("job_type"),
        form_data.get("salary_min") or None,
        form_data.get("salary_max") or None,
        form_data.get("job_url"),
        form_data.get("date_posted") or None,
        parse_skills_to_json(form_data.get("requirements")),
        job_id
    )
    execute_query(query, params)


def delete_job(job_id):
    execute_query(
        "DELETE FROM jobs WHERE job_id = %s",
        (job_id,)
    )


# ---------------- Applications ----------------
def get_all_applications():
    applications = execute_query(
        """
        SELECT a.*, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC, a.application_id DESC
        """,
        fetchall=True
    )

    for application in applications:
        application["interview_data_display"] = json_to_display_string(application.get("interview_data"))
        application["cover_letter_text"] = "Yes" if application.get("cover_letter_sent") else "No"

    return applications


def get_application(application_id):
    application = execute_query(
        "SELECT * FROM applications WHERE application_id = %s",
        (application_id,),
        fetchone=True
    )
    if application:
        application["interview_data_display"] = json_to_display_string(application.get("interview_data"))
    return application


def add_application(form_data):
    query = """
        INSERT INTO applications (
            job_id, application_date, status, resume_version,
            cover_letter_sent, interview_data
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        form_data.get("job_id"),
        form_data.get("application_date"),
        form_data.get("status"),
        form_data.get("resume_version"),
        bool_from_form(form_data.get("cover_letter_sent")),
        parse_json_input(form_data.get("interview_data"))
    )
    execute_query(query, params)


def update_application(application_id, form_data):
    query = """
        UPDATE applications
        SET job_id = %s,
            application_date = %s,
            status = %s,
            resume_version = %s,
            cover_letter_sent = %s,
            interview_data = %s
        WHERE application_id = %s
    """
    params = (
        form_data.get("job_id"),
        form_data.get("application_date"),
        form_data.get("status"),
        form_data.get("resume_version"),
        bool_from_form(form_data.get("cover_letter_sent")),
        parse_json_input(form_data.get("interview_data")),
        application_id
    )
    execute_query(query, params)


def delete_application(application_id):
    execute_query(
        "DELETE FROM applications WHERE application_id = %s",
        (application_id,)
    )


# ---------------- Contacts ----------------
def get_all_contacts():
    return execute_query(
        """
        SELECT ct.*, c.company_name
        FROM contacts ct
        JOIN companies c ON ct.company_id = c.company_id
        ORDER BY ct.contact_name ASC
        """,
        fetchall=True
    )


def get_contact(contact_id):
    return execute_query(
        "SELECT * FROM contacts WHERE contact_id = %s",
        (contact_id,),
        fetchone=True
    )


def add_contact(form_data):
    query = """
        INSERT INTO contacts (
            company_id, contact_name, title, email,
            phone, linkedin_url, notes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        form_data.get("company_id"),
        form_data.get("contact_name"),
        form_data.get("title"),
        form_data.get("email"),
        form_data.get("phone"),
        form_data.get("linkedin_url"),
        form_data.get("notes")
    )
    execute_query(query, params)


def update_contact(contact_id, form_data):
    query = """
        UPDATE contacts
        SET company_id = %s,
            contact_name = %s,
            title = %s,
            email = %s,
            phone = %s,
            linkedin_url = %s,
            notes = %s
        WHERE contact_id = %s
    """
    params = (
        form_data.get("company_id"),
        form_data.get("contact_name"),
        form_data.get("title"),
        form_data.get("email"),
        form_data.get("phone"),
        form_data.get("linkedin_url"),
        form_data.get("notes"),
        contact_id
    )
    execute_query(query, params)


def delete_contact(contact_id):
    execute_query(
        "DELETE FROM contacts WHERE contact_id = %s",
        (contact_id,)
    )


# ---------------- Job Match ----------------
def get_job_match_results(user_skills):
    jobs = execute_query(
        """
        SELECT j.job_title, j.requirements, c.company_name
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY j.job_title ASC
        """,
        fetchall=True
    )

    normalized_user_skills = {skill.strip().lower() for skill in user_skills if skill.strip()}
    results = []

    for job in jobs:
        raw_requirements = job.get("requirements")
        if raw_requirements:
            if isinstance(raw_requirements, str):
                try:
                    requirements_list = json.loads(raw_requirements)
                except json.JSONDecodeError:
                    requirements_list = []
            else:
                requirements_list = raw_requirements
        else:
            requirements_list = []

        normalized_requirements = [skill.strip().lower() for skill in requirements_list if str(skill).strip()]
        matched_skills = [skill for skill in normalized_requirements if skill in normalized_user_skills]
        missing_skills = [skill for skill in normalized_requirements if skill not in normalized_user_skills]

        total_required = len(normalized_requirements)
        matched_count = len(matched_skills)
        match_percentage = round((matched_count / total_required) * 100) if total_required > 0 else 0

        results.append({
            "job_title": job["job_title"],
            "company_name": job["company_name"],
            "match_percentage": match_percentage,
            "matched_count": matched_count,
            "total_required": total_required,
            "missing_skills": ", ".join(missing_skills) if missing_skills else "None"
        })

    results.sort(key=lambda item: item["match_percentage"], reverse=True)
    return results