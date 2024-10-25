from flask import Flask, render_template
from ..app import app


def test_create_app():
    client = app.test_client()
    url = "/"

    response = client.get(url)
    assert response.status_code == 302


def test_get_login_page():
    client = app.test_client()
    url = "/user/login"

    response = client.get(url)
    expected = b'<!DOCTYPE html>\n<html lang="en">\n    <head>\n        <meta charset="UTF-8" />\n        <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n        <title>SkillPilot</title>\n        <link rel="icon"\n              href="/static/favicon.ico"\n              type="image/x-icon" />\n        <meta name="description"\n              content="SkillPilot - Enhance your learning with our platform." />\n        <meta name="keywords"\n              content="skills, learning, education, SkillPilot, platform, career" />\n        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"\n              rel="stylesheet"\n              integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"\n              crossorigin="anonymous" />\n        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"\n                integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"\n                crossorigin="anonymous"></script>\n        <link rel="stylesheet" href="/static/style.css" />\n        <script src="/static/script.js"></script>\n    </head>\n    <body>\n        <header>\n            <a href="/">\n                <h1>SkillPilot</h1>\n            </a>\n        </header>\n        <main>\n            \n<div class="card-wrapper">\n    <div class="card">\n        <h1 class="center">Log In</h1>\n\n        <form class="login_form" name="login_form">\n            <input\n                type="email"\n                name="email"\n                class="field"\n                placeholder="Email"\n                required\n            />\n\n            <div class="password-container">\n                <input\n                    type="password"\n                    name="password"\n                    class="field"\n                    placeholder="Password"\n                    required\n                />\n            </div>\n            <p class="error error--hidden"></p>\n\n            <input type="submit" value="Log In" class="btn" />\n        </form>\n        <p class="center">\n            Don\'t have an account? <a href="/user/register">Register</a>\n        </p>\n        <p class="center">\n            Are you a student?\n            <a href="/student/login">Student Login</a>\n        </p>\n    </div>\n    <script src="/static/login/script.js"></script>\n</div>\n\n        </main>\n        <footer>\n            <p>\xc2\xa9 2024 SkillPilot. All rights reserved.</p>\n            <p>\n                This website uses cookies to ensure you get the best experience.\n                By logging in, you agree to our\n                <a href="/privacy_policy">Privacy Policy</a>.\n            </p>\n        </footer>\n    </body>\n</html>'
    assert response.status_code == 200
    assert response.get_data() == expected

