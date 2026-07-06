from flask import render_template, request, redirect, session
from app import app, db
from models import Admin, Student, Company, PlacementDrive, Application


# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # ADMIN LOGIN
        admin = Admin.query.filter_by(username=username, passhash=password).first()

        if admin:
            session["role"] = "admin"
            return redirect("/admin/dashboard")


        # STUDENT LOGIN
        student = Student.query.filter_by(name=username, passhash=password).first()

        if student:
            session["role"] = "student"
            session["student_id"] = student.id
            return redirect("/student/dashboard")


        # COMPANY LOGIN
        company = Company.query.filter_by(cname=username, passhash=password).first()

        if company:

            if company.approval_status != "approved":
                return "Company not approved yet. Wait for admin approval."

            session["role"] = "company"
            session["company_id"] = company.id

            return redirect("/company/dashboard")

    return render_template("login.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        role = request.form.get("role")
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # STUDENT REGISTRATION
        if role == "student":

            student = Student(
                name=name,
                email=email,
                passhash=password,
                approval_status="approved"
            )

            db.session.add(student)
            db.session.commit()

            return redirect("/login")


        # COMPANY REGISTRATION
        elif role == "company":

            company = Company(
                cname=name,
                email=email,
                passhash=password,
                approval_status="pending"
            )

            db.session.add(company)
            db.session.commit()

            return "Company registered. Please wait for admin approval."

    return render_template("register.html")


# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin/dashboard")
def admin_dashboard():

    if session.get("role") != "admin":
        return redirect("/login")

    students = Student.query.all()

    companies = Company.query.filter_by(approval_status="approved").all()

    pending_companies = Company.query.filter_by(approval_status="pending").all()

    drives = PlacementDrive.query.all()

    applications = Application.query.all()

    return render_template(
        "admin_dashboard.html",
        students=students,
        companies=companies,
        pending_companies=pending_companies,
        drives=drives,
        applications=applications
    )


# ---------------- APPROVE COMPANY ----------------

@app.route("/approve_company/<int:id>")
def approve_company(id):

    company = Company.query.get(id)

    company.approval_status = "approved"

    db.session.commit()

    return redirect("/admin/dashboard")


# ---------------- STUDENT DASHBOARD ----------------

@app.route("/student/dashboard")
def student_dashboard():

    if session.get("role") != "student":
        return redirect("/login")

    drives = PlacementDrive.query.all()

    applications = Application.query.filter_by(
        student_id=session.get("student_id")
    ).all()

    return render_template(
        "student_dashboard.html",
        drives=drives,
        applications=applications
    )


# ---------------- COMPANY DASHBOARD ----------------

@app.route("/company/dashboard")
def company_dashboard():

    if session.get("role") != "company":
        return redirect("/login")

    drives = PlacementDrive.query.filter_by(
        company_id=session.get("company_id")
    ).all()

    applications = Application.query.all()

    return render_template(
        "company_dashboard.html",
        drives=drives,
        applications=applications
    )


# ---------------- CREATE DRIVE ----------------

@app.route("/create_drive", methods=["GET", "POST"])
def create_drive():

    if session.get("role") != "company":
        return redirect("/login")

    if request.method == "POST":

        job_title = request.form.get("job_title")
        job_description = request.form.get("job_description")
        eligibility = request.form.get("eligibility")

        drive = PlacementDrive(
            company_id=session["company_id"],
            job_title=job_title,
            job_description=job_description,
            eligibility_criteria=eligibility
        )

        db.session.add(drive)
        db.session.commit()

        return redirect("/company/dashboard")

    return render_template("create_drive.html")


# ---------------- DRIVE DETAILS ----------------

@app.route("/drive/<int:drive_id>")
def drive_details(drive_id):

    drive = PlacementDrive.query.get(drive_id)

    applications = Application.query.filter_by(drive_id=drive_id).all()

    return render_template(
        "drive_details.html",
        drive=drive,
        applications=applications
    )


# ---------------- APPLY FOR DRIVE ----------------

@app.route("/apply/<int:drive_id>")
def apply(drive_id):

    if session.get("role") != "student":
        return redirect("/login")

    student_id = session.get("student_id")

    # check if already applied
    existing_application = Application.query.filter_by(
        student_id=student_id,
        drive_id=drive_id
    ).first()

    if existing_application:
        return "You have already applied for this drive."

    application = Application(
        student_id=student_id,
        drive_id=drive_id
    )

    db.session.add(application)
    db.session.commit()

    return redirect("/student/dashboard")


# ---------------- APPLICATION HISTORY ----------------

@app.route("/application_history")
def application_history():

    if session.get("role") != "student":
        return redirect("/login")

    applications = Application.query.filter_by(
        student_id=session.get("student_id")
    ).all()

    return render_template(
        "student_application_history.html",
        applications=applications
    )


# ---------------- COMPLETE DRIVE ----------------

@app.route("/complete_drive/<int:id>")
def complete_drive(id):

    drive = PlacementDrive.query.get(id)

    drive.status = "completed"

    db.session.commit()

    return redirect("/company/dashboard")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")