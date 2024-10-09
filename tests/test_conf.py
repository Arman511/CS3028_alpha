from flask import Flask, render_template
from ..app import app


def test_create_app():
    client = app.test_client()
    url = "/"
    
    response = client.get(url)
    expected = b'<!doctype html>\n<html lang=en>\n<title>Redirecting...</title>\n<h1>Redirecting...</h1>\n<p>You should be redirected automatically to the target URL: <a href="/student/login">/student/login</a>. If not, click the link.\n'
    assert response.get_data() == expected
    assert response.status_code == 302
    
