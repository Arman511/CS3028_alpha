"""
This module defines the Skill class and manages the caching and database operations for skills.
Classes:
    Skill: A class used to represent and manage skills in the database.
Functions:
    add_skill():
        Adds a new skill to the database. If the skill already exists and 
        overwrite is not allowed, returns an error.
        Updates the cache after adding the skill.
    delete_skill():
        Deletes a skill from the database based on the skill ID. If the 
        skill is not found, returns an error.
        Updates the cache after deleting the skill.
    get_skill_by_id():
        Retrieves a skill from the database based on the skill ID. If the 
        skill is not found, returns an error.
    get_skills():
        Retrieves all skills from the database. If the cache is valid 
        (updated within the last week), returns the cached data.
        Updates the cache if the data is fetched from the database.
"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, request
from core import database

# Cache to store skills and the last update time
skills_cache = {
    "data": None,
    "last_updated": None
}

class Skill:
    """
    A class used to represent and manage skills in the database."""
    def add_skill(self):
        """Add Skill to database"""
        skill = {
            "_id": uuid.uuid1().hex,
            "skill_name": request.form.get('skill_name'),
            "skill_description": request.form.get('skill_description')
        }
        overwrite = bool(request.form.get('overwrite'))

        if not overwrite and database.skills_collection.find_one({
            "skill_name": request.form.get('skill_name')
            }):
            return jsonify({"error": "Skill already in database"}), 400

        database.skills_collection.insert_one(skill)

        if skill:
            # Update cache
            skills = list(database.skills_collection.find())
            skills_cache["data"] = skills
            skills_cache["last_updated"] = datetime.now()
            return jsonify(skill), 200

        return jsonify({"error": "Skill not added"}), 400

    def delete_skill(self, skill_id):
        """Delete kill from database"""
        skill = database.skills_collection.find_one({"skill_id": skill_id})

        if not skill:
            return jsonify({"error": "Skill not found"}), 404

        database.skills_collection.delete_one({"skill_id": request.form.get('skill_id')})

        # Update cache
        skills = list(database.skills_collection.find())
        skills_cache["data"] = skills
        skills_cache["last_updated"] = datetime.now()

        return jsonify(skill), 200

    def get_skill_by_id(self):
        """Get skill by ID tag"""
        skill = database.skills_collection.find_one({"skill_id": request.form.get('skill_id')})

        if skill:
            return jsonify(skill), 200

        return jsonify({"error": "Skill not found"}), 404

    def get_skills(self):
        """Get full list of skills if chached get that instead"""
        current_time = datetime.now()
        one_week_ago = current_time - timedelta(weeks=1)

        # Check if cache is valid
        if (skills_cache["data"] and skills_cache["last_updated"]
            and skills_cache["last_updated"] > one_week_ago):
            return jsonify(skills_cache["data"]), 200

        # Fetch skills from the database
        skills = list(database.skills_collection.find())

        if skills:
            # Update cache
            skills_cache["data"] = skills
            skills_cache["last_updated"] = current_time
            return jsonify(skills), 200

        return jsonify({"error": "No skills found"}), 404
