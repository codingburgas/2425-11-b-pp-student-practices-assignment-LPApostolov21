import unittest
from flask import url_for
from app import create_app  # adjust if your app factory is elsewhere
from models import db, User, Admin

class TestingConfig:
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestingConfig')  # Use your testing config
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.client.post('/', data={
            'username': 'testuser',
            'password': 'testpass',
            'role': 'user'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User account created successfully!', response.data)

    def test_register_admin(self):
        response = self.client.post('/', data={
            'username': 'adminuser',
            'password': 'adminpass',
            'role': 'admin'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin account created successfully!', response.data)

    def test_login_user(self):
        # First register a user
        hashed_password = 'pbkdf2:sha256:...'  # Or use generate_password_hash
        user = User(username='loginuser', password_hash=hashed_password, role='user')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', data={
            'username': 'loginuser',
            'password': 'wrongpass'  # should fail
        }, follow_redirects=True)

        self.assertIn(b'Invalid username or password', response.data)

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out.', response.data)

