from pydantic import BaseModel, constr

default_str = constr(max_length=255)


def snake_to_camel(string: str) -> str:
    """ Convert snake case string into camel case string. """
    return "".join([word.capitalize() if index > 0 else word for index, word in enumerate(string.split("_"))])


class Mapping(BaseModel):
    class Config:
        alias_generator = snake_to_camel
        allow_population_by_field_name = True


class ORMMapping(Mapping):
    class Config:
        orm_mode = True
        alias_generator = snake_to_camel
        allow_population_by_field_name = True
