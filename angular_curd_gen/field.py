import inflect
import inflection
from inflect import engine
from pydantic import BaseModel


class Image(BaseModel):
    pass


class Url(BaseModel):
    pass


class FieldUtil:
    @staticmethod
    def to_plural(name: str) -> str:
        local_engine = inflect.engine()
        return local_engine.plural(name) or name

    @staticmethod
    def to_singular(name: str) -> str:
        local_engine = inflect.engine()
        return local_engine.singular_noun(text=name) or name

    @staticmethod
    def camel_to_snake(name: str) -> str:
        return inflection.underscore(name)

    @staticmethod
    def snake_to_camel(name: str) -> str:
        return inflection.camelize(name)

    @staticmethod
    def snake_to_camel_lower(name: str) -> str:
        return inflection.camelize(name, False)
