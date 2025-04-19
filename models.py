
from flask_login import UserMixin
from app import db

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'Student' or 'Campus'
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationships
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False)
    campus_profile = db.relationship('CampusProfile', backref='user', uselist=False)
    
    def __repr__(self):
        return f'<User {self.email}>'

class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)
    college_id = db.Column(db.Integer)  # Foreign key to a College table (to be created)
    location = db.Column(db.String(100))
    course = db.Column(db.String(100))
    graduation_start = db.Column(db.Integer)
    graduation_end = db.Column(db.Integer)
    profile_picture = db.Column(db.String(255))  # File path
    
    def __repr__(self):
        return f'<StudentProfile {self.first_name} {self.last_name}>'

class CampusProfile(db.Model):
    __tablename__ = 'campus_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    campus_name = db.Column(db.String(100))
    about = db.Column(db.Text)
    established_year = db.Column(db.Integer)
    courses_offered = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))  # File path
    
    def __repr__(self):
        return f'<CampusProfile {self.campus_name}>'

# We'll add Event model for future implementation
class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    campus_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Campus user_id
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    def __repr__(self):
        return f'<Event {self.title}>'
