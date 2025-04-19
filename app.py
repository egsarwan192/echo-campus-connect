from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'campus-connect-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_connect.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models
from models import User, StudentProfile, CampusProfile

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('signup'))
        
        # Create new user
        new_user = User(
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            role=role
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}')
            return redirect(url_for('signup'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            
            # Check if profile exists
            if user.role == 'Student':
                profile = StudentProfile.query.filter_by(user_id=user.id).first()
                if not profile:
                    return redirect(url_for('setup_student_profile'))
                return redirect(url_for('student_dashboard'))
            else:
                profile = CampusProfile.query.filter_by(user_id=user.id).first()
                if not profile:
                    return redirect(url_for('setup_campus_profile'))
                return redirect(url_for('campus_dashboard'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/setup/student-profile', methods=['GET', 'POST'])
@login_required
def setup_student_profile():
    if current_user.role != 'Student':
        flash('Access denied')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        profile = StudentProfile(
            user_id=current_user.id,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            bio=request.form.get('bio'),
            location=request.form.get('location'),
            course=request.form.get('course'),
            graduation_start=request.form.get('graduation_start'),
            graduation_end=request.form.get('graduation_end')
        )
        
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename:
                filename = secure_filename(f"{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                profile.profile_picture = filename
        
        try:
            db.session.add(profile)
            db.session.commit()
            flash('Profile created successfully!')
            return redirect(url_for('student_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating profile: {str(e)}')
    
    return render_template('setup_student_profile.html')

@app.route('/setup/campus-profile', methods=['GET', 'POST'])
@login_required
def setup_campus_profile():
    if current_user.role != 'Campus':
        flash('Access denied')
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        profile = CampusProfile(
            user_id=current_user.id,
            campus_name=request.form.get('campus_name'),
            about=request.form.get('about'),
            established_year=request.form.get('established_year'),
            courses_offered=request.form.get('courses_offered')
        )
        
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename:
                filename = secure_filename(f"{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                profile.profile_picture = filename
        
        try:
            db.session.add(profile)
            db.session.commit()
            flash('Profile created successfully!')
            return redirect(url_for('campus_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating profile: {str(e)}')
    
    return render_template('setup_campus_profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    if current_user.role != 'Student':
        flash('Access denied')
        return redirect(url_for('index'))
    
    # Get student profile
    profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
    
    # Get recommended campuses (placeholder for now)
    recommended_campuses = CampusProfile.query.limit(3).all()
    
    return render_template('student_dashboard.html', 
                          profile=profile,
                          recommended_campuses=recommended_campuses)

@app.route('/campus/dashboard')
@login_required
def campus_dashboard():
    if current_user.role != 'Campus':
        flash('Access denied')
        return redirect(url_for('index'))
    
    # Get campus profile
    profile = CampusProfile.query.filter_by(user_id=current_user.id).first()
    
    # Get registered students (placeholder)
    students = StudentProfile.query.limit(5).all()
    
    return render_template('campus_dashboard.html', 
                          profile=profile,
                          students=students)

@app.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_picture' not in request.files:
        flash('No file part')
        return redirect(request.referrer)
    
    file = request.files['profile_picture']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.referrer)
    
    if file:
        filename = secure_filename(f"{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Update profile picture path in database
        if current_user.role == 'Student':
            profile = StudentProfile.query.filter_by(user_id=current_user.id).first()
            if not profile:
                profile = StudentProfile(user_id=current_user.id)
                db.session.add(profile)
            profile.profile_picture = filename
        else:
            profile = CampusProfile.query.filter_by(user_id=current_user.id).first()
            if not profile:
                profile = CampusProfile(user_id=current_user.id)
                db.session.add(profile)
            profile.profile_picture = filename
        
        db.session.commit()
        flash('Profile picture updated successfully')
    
    return redirect(request.referrer)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
