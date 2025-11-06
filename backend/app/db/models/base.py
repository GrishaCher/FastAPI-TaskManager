from sqlalchemy.orm import declarative_base


class SerializerMixin:
    def to_dict(self) -> dict:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


Base = declarative_base()
