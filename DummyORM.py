import sqlite3


DATATYPE = {'Integer': 'INTEGER',
            'Boolean': 'INTEGER',
            'String': 'TEXT',
            'Blob': 'BLOB'
            }


class MetaType(type):
    def __new__(cls, name, parents, attrs):
        return DATATYPE[name]


class Integer(metaclass=MetaType):
    pass


class String(metaclass=MetaType):
    pass


class Boolean(metaclass=MetaType):
    pass


class Blob(metaclass=MetaType):
    pass


CONSTRAINTS = {'Required': 'NOT NULL',
               'NotRequired': '',
               'Unique': 'UNIQUE',
               'PrimaryKey': 'PRIMARY KEY'
               }


class MetaConstraints(type):
    def __new__(cls, name, parents, attrs):
        return CONSTRAINTS[name]


class Required(metaclass=MetaConstraints):
    pass


class NotRequired(metaclass=MetaConstraints):
    pass


class Unique(metaclass=MetaConstraints):
    pass


class PrimaryKey(metaclass=MetaConstraints):
    pass


def select(table, fields, limit=None):
    query = 'SELECT ' + ', '.join(fields.keys())
    query += f' FROM {table}'
    where_clause = [f'{key}="{value}"' for key,
                    value in fields.items() if value is not '*']
    if where_clause:
        query += ' WHERE ' + ' AND '.join(where_clause)
    if limit:
        query += f' LIMIT {limit}'
    return query


def create_engine(sqlite_file):
    return sqlite3.connect(sqlite_file)


def declarative_base():
    class Base:
        def __init__(self, **kwargs):
            self.table = self.__tablename__
            if kwargs is not None:
                fields = {}
                for key, value in kwargs.items():
                    if key in self.__dir__():
                        fields[key] = value
                    else:
                        print(f"A column '{key}' in the table '{self.table}' "
                              "is not defined!")
                        raise AttributeError
                self.fields = fields

        @property
        def __tablename__(self):
            print("a __tablename__ attribute in the table "
                  f"'{self.__class__.__name__}' is not defined!")
            raise NotImplementedError

        @classmethod
        def create_all(cls, engine):
            cursor = engine.cursor()
            query = ''
            for table in cls.__subclasses__():
                query = f'CREATE TABLE {table.__tablename__} ('
                fields = []
                for key, value in table.__dict__.items():
                    if not key.startswith('__'):
                        fields.append(f'{key} {value[0]} {value[1]}')
                query += ', '.join(fields)
                query += ')'
                try:
                    cursor.execute(query)
                    engine.commit()
                except sqlite3.OperationalError:
                    print(f"Couldn't create a {table.__name__} table!")

        def insert(self, engine):
            cursor = engine.cursor()
            query = f'INSERT INTO {self.table} ('
            query += ', '.join(self.fields.keys()) + ') '
            query += ('VALUES ('
                      + ', '.join(['?' for _ in self.fields.values()])
                      + ')')
            try:
                cursor.execute(query, tuple(self.fields.values()))
                engine.commit()
            except sqlite3.IntegrityError as error:
                print(error)

        def select_all(self, engine):
            cursor = engine.cursor()
            query = select(self.table, self.fields)
            cursor.execute(query)
            return cursor.fetchall()

        def select_one(self, engine):
            cursor = engine.cursor()
            query = select(self.table, self.fields)
            cursor.execute(query)
            output = cursor.fetchall()
            if len(output) > 1:
                print('Result consisted of more than one row!')
                raise sqlite3.OperationalError
            return output

        def select_scalar(self, engine):
            output = self.select_one(engine)
            return output[0]

        def select_first(self, engine):
            cursor = engine.cursor()
            query = select(self.table, self.fields, limit=1)
            cursor.execute(query)
            return cursor.fetchone()

        def update(self, engine, new_vals=None):
            if new_vals:
                cursor = engine.cursor()
                query = f'UPDATE {self.table} SET '
                query += ', '.join([f'{key}="{value}"'
                                    for key, value in new_vals.items()])
                if self.fields:
                    query += ' WHERE ' + \
                        ' AND '.join([f'{key}="{value}"'
                                      for key, value in self.fields.items()])
                cursor.execute(query)
                engine.commit()

        def drop(self, engine):
            cursor = engine.cursor()
            query = f'DROP TABLE IF EXISTS {self.table}'
            cursor.execute(query)
            engine.commit()

        @classmethod
        def drop_all(cls, engine):
            cursor = engine.cursor()
            tables = [table.__tablename__ for table in cls.__subclasses__()]
            for table in tables:
                query = f'DROP TABLE IF EXISTS {table}'
                cursor.execute(query)
            engine.commit()

    return Base
