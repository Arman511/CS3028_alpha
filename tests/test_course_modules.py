"""Contains tests for the course_modules model"""

import pymongo
import pytest
from ..core import database
from course_modules.models import Module

'''Testing Module.add_module class method'''
def test_add_module_can_add_a_module():
    assert(True)

def test_add_module_can_return_error_for_existing_module():
    assert(True)

def test_add_module_can_fail_to_make_a_module():
    assert(True)

'''Testing Module.delete_module class method'''
def test_delete_module_fails_to_find_module():
    assert(True)

def test_delete_module_returns_200_ok():
    assert(True)

def test_delete_module_actually_deletes_module_from_db():
    assert(True)

'''Testing Module.get_module_by_id class method'''
def test_get_module_by_id_returns_module_with_default_module_id():
    assert(True)

def test_get_module_by_id_returns_module_with_supplied_module_id():
    assert(True)

'''Testing Module.get_module_name_by_id class method'''
def test_get_module_name_by_id_returns_None_if_None_supplied():
    assert(True)

def test_get_module_name_by_id_returns_name_associated_with_module_id():
    assert(True)

'''Testing Module.get_modules class method'''
def test_get_modules_returns_cache_when_no_updates():
    assert(True)

def test_get_modules_returns_list_of_all_modules_from_db():
    assert(True)