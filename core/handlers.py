"""
This module contains utility functions and route configurations for a Flask application.
Functions:
    allowed_file(filename, types):
        Check if file type is allowed.
    login_required(f):
        Decorator to ensure that a user is logged in before accessing certain routes.
    configure_routes(app):
        Configure the routes for the Flask application, including user and student routes, 
        and define the home and privacy policy routes.
Routes:
    /:
        The home route which requires the user to be logged in and renders the 'home.html' template.
    /privacy-policy:
        The privacy policy route which renders the 'privacy_policy.html' template.
"""
from functools import wraps
from flask import render_template, session, redirect
from user import routes_user
from students import routes_student
from opportunities import routes_opportunites

def allowed_file(filename, types):
    """Check if file type is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in types

# Decorators
def login_required(f):
    """This decorator ensures that a user is logged in before accessing certain routes.
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)

        return redirect('/student/login')

    return wrap

def student_login_required(f):
    """This decorator ensures that a user is logged in before accessing certain routes.
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'student_logged_in' in session:
            return f(*args, **kwargs)
        return redirect('/student/login')

    return wrap

def configure_routes(app):
    """Configures the routes for the given Flask application.
    This function sets up the routes for user and student modules by calling their respective
    route configuration functions. It also defines the home route and the privacy policy route.
    Args:
        app (Flask): The Flask application instance.
    Routes:
        /: The home route which needs the user to be logged in and renders the 'home.html' template.
        /privacy-policy: The privacy policy route which renders the 'privacy_policy.html' template.
    """

    routes_user.add_user_routes(app)
    routes_student.add_student_routes(app)
    routes_opportunites.add_opportunities_routes(app)

    @app.route('/')
    @login_required
    def index():
        """The home route which needs the user to be logged in and renders the 'home.html' template.

        Returns:
            str: Rendered HTML template for the home page.
        """
        return render_template('home.html')

    @app.route('/privacy-policy')
    def privacy_policy():
        """The privacy policy route which renders the 'privacy_policy.html' template.

        Returns:
            str: Rendered HTML template for the privacy policy page.
        """
        return render_template('privacy_policy.html')
 