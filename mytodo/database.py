import json

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Time, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Date
from datetime import date, time, timedelta

# How to connect to mysql
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqldb
# engine = sqlalchemy.create_engine("mysql+mysqldb://mytodo:123456@localhost/mytodo", echo=True, future=True)
# with engine.connect() as con:
#     con.execute(sqlalchemy.text("INSERT INTO users (user_id) VALUES (1)"))
#     results = con.execute(sqlalchemy.text("SELECT * FROM users"))
#     for row in results:
#         print(row)

# sqlalchemy orm tutorial:  https://zetcode.com/db/sqlalchemy/orm/
Base = declarative_base()


class User(Base):
    """
    user table
    """
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(32))


class Todo(Base):
    """
    todo table
    """
    __tablename__ = "todos"
    todo_number = Column(Integer,
                         primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    date = Column(Date)
    start = Column(Time)
    end = Column(Time)
    title = Column(String(256))
    description = Column(String(256))


def json_serialize(obj):
    if isinstance(obj, (date, time)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def organize_and_pad(result, start_date: date, end_date: date):
    days = (end_date - start_date).days + 1
    padded = [[start_date + timedelta(days=i), []] for i in range(days)]
    for todo in result:
        padded[(todo['date'] - start_date).days][1].append(todo)
    return padded


class DbDriver:
    def __init__(self):
        self.eng = None

    def add_user(self, token: str):
        session = self.get_session()
        session.add(User(token=token))
        session.commit()
        session.close()

    def get_user(self, token: str):
        session = self.get_session()
        query = session.query(User.token, User.user_id).filter(User.token == token).all()
        session.close()
        return query[0] if len(query) == 1 else None

    def add_todo(self, user_id: int, title: str, description: str, todo_date: date, start: time, end: time):
        session = self.get_session()
        session.add(Todo(user_id=user_id, date=todo_date, start=start, end=end,
                         title=title, description=description))
        session.commit()
        session.close()

    def get_todos_json(self, token: str, start_date: date, end_date: date):
        result = self.get_todos(token, start_date, end_date)
        result = organize_and_pad(result, start_date, end_date)
        return json.dumps(result, default=json_serialize)

    def get_todos(self, token: str, start_date: date, end_date: date):
        """
            :return: todos of a specific user between [start, end]
            sample result:
            [{'date': datetime.date(2021, 7, 15), 'start': datetime.time(0, 0), 'end': datetime.time(0, 0), 'title': 'title1', 'description': 'desc1'},
            {'date': datetime.date(2021, 7, 15), 'start': datetime.time(0, 0), 'end': datetime.time(0, 0), 'title': 'title2', 'description': 'desc2'},
            {'date': datetime.date(2021, 7, 15), 'start': datetime.time(0, 0), 'end': datetime.time(0, 0), 'title': 'title3', 'description': 'desc3'},
            {'date': datetime.date(2021, 7, 15), 'start': datetime.time(0, 0), 'end': datetime.time(0, 0), 'title': 'title4', 'description': 'desc4'},
            {'date': datetime.date(2021, 7, 15), 'start': datetime.time(0, 0), 'end': datetime.time(0, 0), 'title': 'title5', 'description': 'desc5'},
            {'date': datetime.date(2021, 7, 15), 'start': datetime.time(0, 0), 'end': datetime.time(0, 0), 'title': 'title6', 'description': 'desc6'},
            {'date': datetime.date(2021, 7, 15), 'start': datetime.time(0, 0), 'end': datetime.time(0, 0), 'title': 'title7', 'description': 'desc7'}]

        """
        session = self.get_session()
        query = session.query(Todo.date,Todo.start, Todo.end, Todo.title, Todo.description) \
            .select_from(User).join(Todo) \
            .filter(User.token == token).filter(Todo.date >= start_date).filter(Todo.date <= end_date).all()
        result = [row._asdict() for row in query]
        session.close()
        return result

    def connect_to_db(self):
        eng = sqlalchemy.create_engine(
            "mysql+mysqldb://mytodo:123456@localhost/mytodo", echo=False, future=True)
        self.eng = eng

    def get_session(self):
        Session = sessionmaker(bind=self.eng)
        session = Session()
        return session


dbdriver = DbDriver()
dbdriver.connect_to_db()
if __name__ == "__main__":
    print(dbdriver.get_todos_json("test_user1",date(2021,7,1),date(2021,7,15)))
