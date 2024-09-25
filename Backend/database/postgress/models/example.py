from sqlmodel import Field, SQLModel

class Example(SQLModel, table=True):
    name: str
    username: str
    email: str
    password: str
    id: int | None = Field(default=None, primary_key=True)

    def __repr__(self):
        return f"User(name={self.name}, username={self.username}, email={self.email})"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def to_dict(self):
        return {
            "name": self.name,
            "username": self.username,
            "email": self.email
        }

    @staticmethod
    def from_dict(data):
        return Example(**data)