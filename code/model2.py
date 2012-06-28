import sqlalchemy
from elixir import (Entity, Field, Unicode, Integer,
                    setup_entities, GlobalEntityCollection)

__session__ = sqlalchemy.orm.scoped_session(sqlalchemy.orm.sessionmaker())
__metadata__ = sqlalchemy.MetaData(bind="sqlite:///db.sqlite")
__collection__ = GlobalEntityCollection()


class User(Entity):
    name = Field(Unicode)
    age = Field(Integer)


if __name__ == '__main__':
    setup_entities(__collection__)
    __metadata__.create_all()

