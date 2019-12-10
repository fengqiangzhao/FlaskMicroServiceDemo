from flask_testing import TestCase

from project import create_app

app = create_app('project.config.DevelopmentConfig')


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'secret')
        self.assertTrue(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] ==
                        'mysql+pymysql://root:root321@users-db:3306/users_dev')


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'secret')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(
            self.app.config['SQLALCHEMY_DATABASE_URI'] ==
            'mysql+pymysql://root:root321@users-db:3306/users_test')


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('project.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'secret')
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
