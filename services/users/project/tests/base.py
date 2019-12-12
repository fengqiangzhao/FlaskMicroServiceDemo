from flask_testing import TestCase
from project import create_app, db

app = create_app('project.config.TestingConfig')


class BaseTestCase(TestCase):
    def create_app(self):
        self.app = app
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
