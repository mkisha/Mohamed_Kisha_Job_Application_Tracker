# Mohamed Kisha - Job Application Tracker

## Project Overview
This is a full-stack web application built with Flask, MySQL, HTML, CSS, and Bootstrap.  
The purpose of the app is to help users track job applications, companies, contacts, and jobs.

## Features
- Dashboard with summary statistics
- Full CRUD for:
  - Companies
  - Jobs
  - Applications
  - Contacts
- Job Match feature that compares user-entered skills with job requirements
- JSON support for:
  - `requirements` in jobs
  - `interview_data` in applications

## Technologies Used
- Python 3
- Flask
- MySQL
- HTML
- CSS
- Bootstrap
- GitHub

## Project Structure
```text
Mohamed_Kisha_Job_Application_Tracker/
│
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── README.md
├── AI_USAGE.md
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── companies.html
    ├── company_form.html
    ├── jobs.html
    ├── job_form.html
    ├── applications.html
    ├── application_form.html
    ├── contacts.html
    ├── contact_form.html
    └── job_match.html