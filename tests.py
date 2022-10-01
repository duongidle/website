from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='duong')
        u.set_password('password1')
        self.assertFalse(u.check_password('password2'))
        self.assertTrue(u.check_password('password1'))

    def test_avatar(self):
        u = User(username='duong', email='duong@duong.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         '49064dffd110ec1826f2ef79df8574c0'
                                         '?d=identicon&s=128'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
