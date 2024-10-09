"""
This module defines the routes for user-related actions in the Flask application.

Routes:
    /user/register (POST): Registers a new user.
    /user/signout: Signs out the current user.
    /user/login: Renders the login page.
    /user/login_attempt (POST): Attempts to log in a user.
"""
from flask import redirect, render_template, session, request
from .models import User

def add_user_routes(app):
    """Add user routes."""
    @app.route('/user/register', methods=['GET', 'POST'])
    def register():
        """Give page to register a new user."""
        if request.method == 'POST':
            return User().register()
        return render_template('register.html')

    @app.route('/user/signout')
    def signout():
        """Signs out the current user."""
        return User().signout()

    @app.route('/user/login', methods=['GET', 'POST'])
    def login():
        """Gives login form to user."""
        if request.method == 'POST':
            return User().login()
        if "logged_in" in session:
            return redirect('/')
        return render_template('login.html')
    
    @app.route('/user/change_password', methods=['GET', 'POST'])
    def change_password():
        """Change user password."""
        if request.method == 'POST':
            return User().change_password()
        return render_template('change_password.html')
