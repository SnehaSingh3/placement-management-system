from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#1.Admin table
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    passhash = db.Column(db.String(256), nullable=False)


#Student Table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    passhash = db.Column(db.String(256), nullable=False)
    resume_link = db.Column(db.String(255))
    approval_status = db.Column(db.String(20), default='approved')

    applications = db.relationship('Application', backref='student', lazy=True)
    
#Company Table
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hr_contact = db.Column(db.String(150))
    website = db.Column(db.String(150))
    approval_status = db.Column(db.String(20), default='pending')
    passhash = db.Column(db.String(256), nullable=False)

    drives = db.relationship('PlacementDrive', backref='company', lazy=True)

#Placement Drive Table
class PlacementDrive(db.Model):
    drive_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    drive_date = db.Column(db.DateTime)
    job_title = db.Column(db.String(100))
    job_description = db.Column(db.String(500))
    eligibility_criteria = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending')

    applications = db.relationship('Application', backref='drive', lazy=True)

#Application Table
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.drive_id'), nullable=False)
    application_date = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(20), default='pending')

