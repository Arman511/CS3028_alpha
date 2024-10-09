
"""
This module defines the User class which handles user authentication and session management.
"""
import uuid
from flask import jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from core import database

class User:
    """A class used to represent a User and handle user-related operations 
    such as session management, registration, login, and signout."""
    def start_session(self, user):
        """Starts a session for the given user by removing the password from the 
        user dictionary, setting session variables, and returning a JSON response."""
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def register(self):
        """Registers a new user by creating a user dictionary with a unique ID, 
        name, email, and password, and returns a JSON response indicating failure."""
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match (if needed here for extra validation)
        if password != confirm_password:
            return jsonify({"error": "Passwords don't match"}), 400

        user = {
            "_id": uuid.uuid1().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": pbkdf2_sha256.hash(password)  # Hash only the password
        }

        if database.users_collection.find_one({"email": request.form.get('email')}):
            return jsonify({"error": "Email address already in use"}), 400

        # Insert the user into the database
        database.users_collection.insert_one(user)

        # Start session or return success response
        if user:
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        """Clears the current session and redirects to the home page."""
        session.clear()
        return redirect('/')

    def login(self):
        """Validates user credentials and returns a JSON response indicating 
        invalid login credentials."""
        session.clear()
        user = database.users_collection.find_one({"email": request.form.get("email")})

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401

    def change_password(self):
        """Change user password."""
        user = session.get('user')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not pbkdf2_sha256.verify(old_password, user['password']):
            return jsonify({"error": "Invalid old password"}), 400

        if new_password != confirm_password:
            return jsonify({"error": "Passwords don't match"}), 400

        database.users_collection.update_one(
            {"_id": user['_id']},
            {"$set": {"password": pbkdf2_sha256.hash(new_password)}}
        )

        return jsonify({"message": "Password updated successfully"}), 200
    