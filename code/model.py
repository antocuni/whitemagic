from elixir import Entity, Field, Unicode, Integer, metadata, session, setup_all, create_all

metadata.bind = "sqlite:///db.sqlite"

class User(Entity):
    name = Field(Unicode)
    age = Field(Integer)


if __name__ == '__main__':
    setup_all()
    create_all()
    u = User(name=u'anto', age=30)
    session.commit()

