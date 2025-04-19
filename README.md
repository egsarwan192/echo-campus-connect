
# Campus Connect

Campus Connect is a web application that connects students and campuses, providing a platform for educational institutions to showcase their offerings and for students to discover opportunities.

## Features

- **Two User Roles:** Student and Campus
- **Authentication:** Email-based authentication with role selection
- **Profiles:** Create and manage profiles for both students and campuses
- **Dashboard:** Personalized dashboards for each user role
- **File Uploads:** Support for profile pictures and other documents
- **Responsive Design:** Works seamlessly on all devices

## Tech Stack

- **Frontend:** HTML, CSS (pure CSS, no frameworks), Vanilla JavaScript
- **Backend:** Flask
- **Database:** SQLite (for development)
- **Authentication:** Flask-Login with bcrypt for password hashing

## Project Structure

```
campus-connect/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Project dependencies
├── static/                # Static assets
│   ├── css/
│   │   └── styles.css     # Main stylesheet
│   ├── js/
│   │   └── script.js      # JavaScript functionality
│   └── uploads/           # User uploaded files
└── templates/             # HTML templates
    ├── index.html         # Landing page
    ├── login.html         # Login page
    ├── signup.html        # Signup page
    ├── student_dashboard.html  # Student dashboard
    └── campus_dashboard.html   # Campus dashboard
```

## Setup and Installation

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/campus-connect.git
   cd campus-connect
   ```

2. **Create a virtual environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```
   python app.py
   ```
   The database will be automatically created on first run.

5. **Run the application**
   ```
   python app.py
   ```
   The application will be available at http://localhost:5000

## Color Scheme

- Primary Orange: #F28C38
- White: #FFFFFF
- Text Gray: #4A4A4A
- Border/Background Gray: #E0E0E0

## Future Enhancements

- Resume builder functionality for students
- Event management system for campuses
- Messaging system between students and campuses
- Advanced search and filtering options
- Galleries for campus profiles
- Email notifications

## License

This project is open source and available under the [MIT License](LICENSE).
