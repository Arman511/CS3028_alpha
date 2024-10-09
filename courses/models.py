"""
This module defines the Course class and provides methods to manage courses in the database.
Classes:
    Course: A class to represent and manage courses.
Methods:
    add_course(self):
        Adds a new course to the database.
        Updates the courses cache upon successful addition.
        Returns a JSON response with the added course or an error message.
    delete_course(self):
        Deletes a course from the database based on the course_id provided in the request.
        Updates the courses cache upon successful deletion.
        Returns a JSON response with the deleted course or an error message.
    get_course_by_id(self):
        Retrieves a course from the database based on the course_id provided in the request.
        Returns a JSON response with the course details or an error message.
    get_courses(self):
        Retrieves all courses from the database. Uses a cache to store courses for up to one week.
        Returns a JSON response with the list of courses or an error message.
"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, request
from core import database

# Cache to store courses and the last update time
courses_cache = {
    "data": None,
    "last_updated": None
}
class Course:
    """Course data model"""
    def add_course(self):
        """Adds a course to the database."""
        course = {
            "_id": uuid.uuid1().hex,
            "course_id": request.form.get('course_id'),
            "course_name": request.form.get('course_name'),
            "course_description": request.form.get('course_description')
        }
        overwrite = bool(request.form.get('overwrite'))

        if not overwrite and database.courses_collection.find_one({
            "course_id": request.form.get('course_id')
            }):
            return jsonify({"error": "Course already in database"}), 400

        database.courses_collection.insert_one(course)

        if course:
            # Update cache
            courses = list(database.courses_collection.find())
            courses_cache["data"] = courses
            courses_cache["last_updated"] = datetime.now()
            return jsonify(course), 200

        return jsonify({"error": "Course not added"}), 400

    def delete_course(self):
        """Deletes a course from the database."""
        course = database.courses_collection.find_one({"course_id": request.form.get('course_id')})

        if not course:
            return jsonify({"error": "Course not found"}), 404

        database.courses_collection.delete_one({"course_id": request.form.get('course_id')})

        # Update cache
        courses = list(database.courses_collection.find())
        courses_cache["data"] = courses
        courses_cache["last_updated"] = datetime.now()

        return jsonify(course), 200

    def get_course_by_id(self):
        """Retrieves a course by its ID."""
        course = database.courses_collection.find_one({"course_id": request.form.get('course_id')})

        if course:
            return jsonify(course), 200

        return jsonify({"error": "Course not found"}), 404

    def get_courses(self):
        """Retrieves all courses."""
        current_time = datetime.now()
        one_week_ago = current_time - timedelta(weeks=1)

        # Check if cache is valid
        if (courses_cache["data"] and courses_cache["last_updated"] and
            courses_cache["last_updated"] > one_week_ago):
            return jsonify(courses_cache["data"]), 200

        # Fetch courses from the database
        courses = list(database.courses_collection.find())

        if courses:
            # Update cache
            courses_cache["data"] = courses
            courses_cache["last_updated"] = current_time
            return jsonify(courses), 200

        return jsonify({"error": "No courses found"}), 404
