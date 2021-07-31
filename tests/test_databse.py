import unittest
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from mytodo.database import User, Todo, Base, DbDriver
from datetime import date


class DbTestCase(unittest.TestCase):
    def test_get_todos_month(self):
        result = self.dbdriver.get_todos_month("test_user1", "2021-6-11", "2021-6-12")
        self.assertEqual(len(result), 0)
        result = self.dbdriver.get_todos_month("test_user1", "2021-07-15", "2021-07-15")
        self.assertEqual(len(result), 7)
        result = self.dbdriver.get_todos_month("test_user1", "2021-07-16", "2021-07-22")
        self.assertEqual(len(result), 6)
        result = self.dbdriver.get_todos_month("test_user2", "2021-07-15", "2021-07-15")
        self.assertEqual(len(result), 0)
        result = self.dbdriver.get_todos_month("test_user3", "2021-01-01", "2021-12-31")
        self.assertEqual(len(result), 0)

    def test_add_todo(self):
        self.dbdriver.add_todo(1, "add1", "add1", "2021-8-31")
        result = self.dbdriver.get_todos_month("test_user1", "2021-8-31", "2021-8-31")
        self.assertEqual(len(result), 1)
        result = result[0]
        self.assertEqual(result['date'], date(2021, 8, 31))
        self.assertEqual(result['title'], 'add1')
        self.assertEqual(result['description'], "add1")

    @classmethod
    def setUpClass(cls) -> None:
        cls.dbdriver = DbDriver()
        cls.dbdriver.connect_to_db()
        # clear database
        Base.metadata.drop_all(bind=cls.dbdriver.eng)
        Base.metadata.create_all(bind=cls.dbdriver.eng)

        users = [User(user_id=1, token="test_user1"),
                 User(user_id=2, token="test_user2"),
                 User(user_id=3, token="test_user3")]
        session = cls.dbdriver.get_session()
        session.add_all(users)
        session.commit()

        todos = [
            Todo(user_id=1, date="2021-07-15", start="", end="", title="title1", description="desc1"),
            Todo(user_id=1, date="2021-07-15", start="", end="", title="title2", description="desc2"),
            Todo(user_id=1, date="2021-07-15", start="", end="", title="title3", description="desc3"),
            Todo(user_id=1, date="2021-07-15", start="", end="", title="title4", description="desc4"),
            Todo(user_id=1, date="2021-07-15", start="", end="", title="title5", description="desc5"),
            Todo(user_id=1, date="2021-07-15", start="", end="", title="title6", description="desc6"),
            Todo(user_id=1, date="2021-07-15", start="", end="", title="title7", description="desc7"),

            Todo(user_id=2, date="2021-07-16", start="", end="", title="title1", description="desc1"),
            Todo(user_id=2, date="2021-07-16", start="", end="", title="title2", description="desc2"),
            Todo(user_id=2, date="2021-07-16", start="", end="", title="title3", description="desc3"),
            Todo(user_id=2, date="2021-07-16", start="", end="", title="title4", description="desc4"),
            Todo(user_id=2, date="2021-07-16", start="", end="", title="title5", description="desc5"),
            Todo(user_id=2, date="2021-07-16", start="", end="", title="title6", description="desc6"),
            Todo(user_id=2, date="2021-07-16", start="", end="", title="title7", description="desc7"),

            Todo(user_id=1, date="2021-07-16", start="", end="", title="title7", description="desc7"),
            Todo(user_id=1, date="2021-07-17", start="", end="", title="title7", description="desc7"),
            Todo(user_id=1, date="2021-07-18", start="", end="", title="title7", description="desc7"),
            Todo(user_id=1, date="2021-07-19", start="", end="", title="title7", description="desc7"),
            Todo(user_id=1, date="2021-07-20", start="", end="", title="title7", description="desc7"),
            Todo(user_id=1, date="2021-07-21", start="", end="", title="title7", description="desc7"),
            Todo(user_id=1, date="2021-08-15", start="", end="", title="title7", description="desc7"),
        ]
        session.add_all(todos)
        session.commit()


if __name__ == '__main__':
    unittest.main()
