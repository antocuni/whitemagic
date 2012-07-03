from elixir import Entity, Field, Unicode, Integer

class User(Entity):
    name = Field(Unicode)
    age = Field(Integer)
