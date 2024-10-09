"""
This module defines the Opportunity class, which gives methods for managing jobs in the database.

Classes:
    Opportunity: A class to represent and manage job opportunities.

Methods:
    add_opportunity(self):
        Adds a new opportunity to the database.
        Returns a JSON response indicating success or failure.

    search_opportunities(self):
        Searches for opportunities in the database based on provided criteria.
        Returns a JSON response with the search results or an error message.

    get_opportunity_by_id(self):
        Retrieves an opportunity from the database by its ID.
        Returns a JSON response with the opportunity data or an error message.

    get_opportunities(self):
        Retrieves all opportunities from the database.
        Returns a JSON response with the list of opportunities or an error message.

    update_opportunity(self):
        Updates an existing opportunity in the database.
        Returns a JSON response indicating success or failure.

    delete_opportunity_by_id(self, opportunity_id):
        Deletes an opportunity from the database by its ID.
        Returns a JSON response indicating success or failure.

    delete_opportunities(self):
        Deletes all opportunities from the database.
        Returns a JSON response indicating success or failure.

    import_opportunities_from_csv(self):
        Imports opportunities from a CSV file into the database.
        Returns a JSON response indicating success or failure.

    import_opportunities_from_xlsx(self):
        Imports opportunities from an Excel file into the database.
        Returns a JSON response indicating success or failure.
"""
import uuid
from flask import jsonify, request
import pandas as pd
from core import database, handlers

class Opportunity:
    """Opportunity class."""

    def add_opportunity(self):
        """Adding new opportunity."""
        opportunity = {
            "_id": uuid.uuid1().hex,
            "title": request.form.get('title'),
            "description": request.form.get('description'),
            "url": request.form.get('url'),
            "company": request.form.get('company'),
            "location": request.form.get('location'),
            "skills_required": request.form.get('skills_required'),
            "course_required": request.form.get('course_required'),
            "spots_available": request.form.get('spots_available')
        }

        database.opportunities_collection.insert_one(opportunity)

        if opportunity:
            return jsonify(opportunity), 200

        return jsonify({"error": "Opportunity not added"}), 400

    def search_opportunities(self):
        """Searching opportunities."""
        title = request.form.get('title')
        company = request.form.get('company')
        location = request.form.get('location')
        skills_required = request.form.get('skills_required')

        query = {}
        if title:
            query["title"] = title
        if company:
            query["company"] = company
        if location:
            query["location"] = location
        if skills_required:
            query["skills_required"] = skills_required

        opportunities = list(database.opportunities_collection.find(query))

        if opportunities:
            return jsonify(opportunities), 200

        return jsonify({"error": "No opportunities found"}), 404

    def get_opportunity_by_id(self):
        """Getting opportunity."""
        opportunity = database.opportunities_collection.find_one({
            "_id": request.form.get('_id')
            })

        if opportunity:
            return jsonify(opportunity), 200

        return jsonify({"error": "Opportunity not found"}), 404

    def get_opportunities(self):
        """Getting all opportunities."""
        opportunities = list(database.opportunities_collection.find())

        if opportunities:
            return jsonify(opportunities), 200

        return jsonify({"error": "No opportunities found"}), 404

    def update_opportunity(self):
        """Updating opportunity."""
        opportunity = database.opportunities_collection.find_one({
            "_id": request.form.get('_id')
            })

        if opportunity:
            database.opportunities_collection.update_one({
                "_id": request.form.get('_id')}, {
                    "$set": request.form
                    })
            return jsonify({"message": "Opportunity updated"}), 200

        return jsonify({"error": "Opportunity not found"}), 404

    def delete_opportunity_by_id(self, opportunity_id):
        """Deleting opportunity."""
        opportunity = database.opportunities_collection.find_one({"_id": opportunity_id})

        if opportunity:
            database.opportunities_collection.delete_one({"_id": opportunity_id})
            return jsonify({"message": "Opportunity deleted"}), 200

        return jsonify({"error": "Opportunity not found"}), 404

    def delete_opportunities(self):
        """Deleting all opportunities."""
        opportunities = list(database.opportunities_collection.find())

        if opportunities:
            database.opportunities_collection.delete_many({})
            return jsonify({"message": "All opportunities deleted"}), 200

        return jsonify({"error": "No opportunities found"}), 404

    def import_opportunities_from_csv(self):
        """Importing opportunities from CSV file."""

        if not 'file' in request.files:
            return jsonify({"error": "No file part"}), 400

        if not handlers.allowed_file(request.files['file'].filename, ['csv']):
            return jsonify({"error": "Invalid file type"}), 400

        try:
            file = request.files['file']
            df = pd.read_csv(file)

            opportunities = df.to_dict(orient='records')
            for opportunity in opportunities:
                opportunity["_id"] = uuid.uuid1().hex
                database.opportunities_collection.delete_one({"title": opportunity["title"]})

            database.opportunities_collection.insert_many(opportunities)
            return jsonify({"message": "Opportunities imported"}), 200
        except (pd.errors.EmptyDataError, pd.errors.ParserError, FileNotFoundError) as e:
            return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    def import_opportunities_from_xlsx(self):
        """Importing opportunities from Excel file."""

        if not 'file' in request.files:
            return jsonify({"error": "No file part"}), 400

        if not handlers.allowed_file(request.files['file'].filename, ['xlsx', 'xls']):
            return jsonify({"error": "Invalid file type"}), 400

        try:
            file = request.files['file']
            df = pd.read_excel(file)

            opportunities = df.to_dict(orient='records')
            for opportunity in opportunities:
                opportunity["_id"] = uuid.uuid1().hex
            database.opportunities_collection.insert_many(opportunities)

            return jsonify({"message": "Opportunities imported"}), 200
        except (pd.errors.EmptyDataError, pd.errors.ParserError, FileNotFoundError) as e:
            return jsonify({"error": f"Failed to read file: {str(e)}"}), 400
