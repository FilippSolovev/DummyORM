from DummyORM import Integer, String
from DummyORM import NotRequired, PrimaryKey
from DummyORM import create_engine, declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = (Integer, PrimaryKey)
    user_name = (String, NotRequired)


if __name__ == '__main__':

    sqlite_file = ':memory:'
    engine = create_engine(sqlite_file)
    Base.create_all(engine)

    # Insert and update
    User(user_id=1, user_name='Philip').insert(engine)
    User(user_id=2, user_name='Peter').insert(engine)
    User(user_name='Gary').insert(engine)
    User(user_name='John').insert(engine)

    User(user_id=3).update(engine, {'user_name': 'Mr. X'})

    # Select
    print(User(user_id='1', user_name='*').select_all(engine))
    print(User(user_id='1', user_name='*').select_first(engine))
    print(User(user_id='2', user_name='*').select_one(engine))
    print(User(user_id='3', user_name='*').select_scalar(engine))

    print(User(user_id='*', user_name='Philip').select_all(engine))

    # Delete tables
    Base.drop_all(engine)

    engine.close()
