import json

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Time, Date, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Date
from datetime import date, time

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

    def get_todos_month_json(self, token: str, start_date: date, end_date: date):
        result = self.get_todos_month(token, start_date, end_date)
        return json.dumps(result, default=json_serialize)

    def get_todos_month(self, token: str, start_date: date, end_date: date):
        """
            :return: todos of a specific user between [start, end]
        """
        session = self.get_session()
        query = session.query(Todo.date, Todo.title, Todo.description) \
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
    pass
