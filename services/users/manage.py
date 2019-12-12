import unittest
from flask_script import Manager
from project import create_app, db
from project.api.models import User
import coverage
import os

config = os.getenv('APP_SETTINGS')

app = create_app(config)
manager = Manager(app)

COV = coverage.coverage(branch=True,
                        include='project/*',
                        omit=['project/tests/*'])
COV.start()


@manager.command
def recreate_db():
    """重新创建数据表."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def test():
    tests = unittest.TestLoader().discover('project/tests',
                                           pattern='test_*.py')
    reesult = unittest.TextTestRunner(verbosity=2).run(tests)

    if reesult.wasSuccessful():
        return 0
    return 1


@manager.command
def insert_user():
    db.session.add(User(username='cnych', email="qikqiak@gmail.com"))
    db.session.add(User(username='chyang', email="icnych@gmail.com"))
    db.session.commit()


if __name__ == "__main__":
    manager.run()
