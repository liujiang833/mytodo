from datetime import datetime
from random import seed
from typing import Mapping
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.sqltypes import Date

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
# user table


class User(Base):
    __tablename__ = "users"
    user_id = Column("user_id", Integer, primary_key=True, autoincrement=True)
    token = Column('token', String)

# todo table


class Todo(Base):
    __tablename__ = "todos"
    todo_number = Column("todo_number", Integer,
                         primary_key=True, autoincrement=True)
    user_id = Column("user_id", Integer)
    time = Column("time", DateTime)
    title = Column("title", String)
    description = Column("description", String)


# global variables
eng = sqlalchemy.create_engine(
    "mysql+mysqldb://mytodo:123456@localhost/mytodo", echo=True, future=True)
Session = sessionmaker(bind=eng)
session = Session()


def add_user(token):
    session.add(User(token=token))
    session.commit()

def get_user(token):
    query = session.query(User.token).filter(User.token == token)
    result = list(session.execute(query))
    return result[0][0] if result else None

def add_todo(user_id,time,title,description):
    session.add(Todo(user_id=user_id,time=time,title=title,description=description))
    session.commit()

def get_todos_month_default():
    month_todos = []
    for i in range(5):
        row = []
        for j in range(7):
            row.append(("",[("","","")] * 4))
        month_todos.append(row)
    return month_todos

def get_todos_month(token):
    '''
       :returns: list[tuple(date,list[tuple(time, title, description)])] 
    '''
    # query = session.query(User.token).filter(User.token == token)
    return get_todos_month_mock()

def get_todos_month_mock():
    month_todos = []
    for i in range(5):
        row = []
        for j in range(7):
            row.append((7 * j +i,[]))
        month_todos.append(row)
    month_todos[0][3] = (3, [(datetime.now(),"title1","desc1")])
    month_todos[0][5] = (5, [  (datetime.now(),"title1","desc1"),
                            (datetime.now(),"title2","desc2"),])
    return month_todos 


if __name__ == "__main__":
    print(get_user('hello_world2'))