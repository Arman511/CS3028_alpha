import pytest
import os
from dotenv import load_dotenv
load_dotenv() 
if os.getenv('IS_GITHUB_ACTIONS', "True") != 'True':
    from ..core import database
import uuid

def test_ping_success():
    if os.getenv('IS_GITHUB_ACTIONS', "True") != 'True':
        try:
            database.client.admin.command('ping')
            assert True, "Pinged your deployment. You successfully connected to MongoDB!"
        except Exception as e:
            pytest.fail(f"Unexpected error: {e}")
        
def test_find_dummy_login():
    if os.getenv('IS_GITHUB_ACTIONS', "True") != 'True':
        user = database.users_collection.find_one({"email": "dummy@dummy.com"})
        
        if user:
            assert user['email'] == "dummy@dummy.com"
            assert user['password'] == "dummy"
            assert user['name'] == "dummy"
        else:
            pytest.fail("User not found")
        
def test_add_and_remove_dummy_login():
    if os.getenv('IS_GITHUB_ACTIONS', "True") != 'True':
        user = {
            "_id": uuid.uuid4().hex,
            "name": "dummy2",
            "email": "dummy2@dummy.com",
            "password": "dummy2"
        }
        database.users_collection.insert_one(user)
        
        # Assert the user was added
        added_user = database.users_collection.find_one({"email": "dummy2@dummy.com"})
        assert added_user is not None, "User was not added"
        assert added_user['email'] == "dummy2@dummy.com"

        # Delete the user
        database.users_collection.delete_one({"email": "dummy2@dummy.com"})

        # Confirm the user was deleted
        deleted_user = database.users_collection.find_one({"email": "dummy2@dummy.com"})
        assert deleted_user is None, "User was not deleted"
