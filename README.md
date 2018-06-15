# The Dummy ORM

In general, an ORM or an object-relational mapping adds a level of abstraction on top of a relational database management system. It lets you query and manipulate data from a database using an object-oriented paradigm. The most popular ORMs libraries for Python are [SQLAlchemy](https://www.sqlalchemy.org "SQLAlchemy") and [Django ORM](https://docs.djangoproject.com/en/2.0/ref/models/ "Django ORM"). Here is an example of very basic ORM with limited functionality written to use with [SQLite](https://www.sqlite.org/index.html "SQLite"). As with the [Dummy WSGI framework](https://github.com/FilippSolovev/DummyWSGIFramework "Dummy WSGI framework"), my motivation to build this project was purely educational.

# How to use

Like SQLAlchemy this ORM allows three major its components: a table, a mapper, and a class object to be defined at once in one class definition. The following declarative definition specifies a table of users with just two columns ‘id’ and ‘name’:

~~~~
from DummyORM import Integer, String
from DummyORM import NotRequired, PrimaryKey
from DummyORM import create_engine, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = (Integer, PrimaryKey)
    user_name = (String, NotRequired)
~~~~

Below create an engine that stores data locally in a file or memory:

~~~~
    sqlite_file = ':memory:'
    engine = create_engine(sqlite_file)
~~~~

Further, create all tables in the engine (here in the example it will be the table ‘users’) which is an equivalent to SQL’s ‘CREATE TABLE’:

~~~~
    Base.create_all(engine)
~~~~

Let's write some code to insert and update records into the database:

~~~~
    User(user_id=1, user_name='Philip').insert(engine)
    User(user_id=2, user_name='Peter').insert(engine)
    User(user_name='Gary').insert(engine)
    User(user_name='John').insert(engine)

    User(user_id=3).update(engine, {'user_name': 'Mr. X'})
~~~~

Now we are ready to query the database using the defined class:

~~~~
    print(User(user_id='1', user_name='*').select_all(engine))
    print(User(user_id='1', user_name='*').select_first(engine))
    print(User(user_id='2', user_name='*').select_one(engine))
    print(User(user_id='3', user_name='*').select_scalar(engine))
    print(User(user_id='*', user_name='Philip').select_all(engine))
~~~~

According to our data, the result should be as follows:

~~~~
[(1, 'Philip')]
(1, 'Philip')
[(2, 'Peter')]
(3, 'Mr. X')
[(1, 'Philip')]
~~~~

To delete all the tables created use:

~~~~
    Base.drop_all(engine)
~~~~

Here we are. The only thing left is to close the database.

~~~~
    engine.close()
~~~~

The code above is enclosed in an application.py file.

# Installation and running

Clone the project and install the requirements:

~~~~
$ git clone https://github.com/FilippSolovev/DummyORM.git
$ pip install -r requirements.txt
~~~~

# Built With
* [Python 3](https://docs.python.org/3/ "Python 3")
* [sqlite3](https://github.com/ghaering/pysqlite "sqlite3")

# Authors
[FilippSolovev](https://github.com/FilippSolovev "FilippSolovev")

# License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/FilippSolovev/DummyORM/blob/master/LICENSE) file for details
