import os

from pydantic import BaseModel
import re
from dotenv import load_dotenv

load_dotenv()


class ConfigModel(BaseModel):
    def __init__(self) -> None:
        class_name = self._camelcase_to_snakecase(self.__class__.__name__)
        data = dict()
        for key, field in self.__fields__.items():
            data[key] = field.type_(
                os.environ.get(f"{class_name}__{key.upper()}", field.default)
            )
        super().__init__(**data)

    @staticmethod
    def _camelcase_to_snakecase(string):
        return re.sub(r"(?<!^)(?=[A-Z])", "_", string).upper()

    @classmethod
    def get_fields_defaults(cls):
        class_name = cls._camelcase_to_snakecase(cls.__name__)
        return {
            f"{class_name}__{key.upper()}": os.environ.get(
                f"{class_name}__{key.upper()}"
            )
            or str(field.default or "")
            for key, field in cls.__fields__.items()
        }


# postgres://postgres:123456@127.0.0.1:5432/dummy


class PostgresConfig(ConfigModel):
    user: str
    pwd: str
    host: str
    port: int = 5432
    db_name: str = ""

    def get_connection_url(self):
        return f"postgres://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.db_name}"


POSTGRES_CONFIG = PostgresConfig()
TORTOISE_ORM = {
    "connections": {"default": POSTGRES_CONFIG.get_connection_url()},
    "apps": {
        "models": {
            "models": ["qmunity.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


class MongoConfig(ConfigModel):
    user: str
    pwd: str
    host: str
    port: int = 27017
    db_name: str

    def get_connection_url(self):
        return f"mongodb://{self.user}:{self.pwd}@{self.host}:{self.port}/{self.db_name}?authSource=admin"


MONGO_CONFIG = MongoConfig()

if __name__ == "__main__":
    configs = [
        PostgresConfig.get_fields_defaults(),
        MongoConfig.get_fields_defaults(),
    ]

    if os.path.exists("../.env"):
        os.remove("../.env")
    with open("../.env", "w") as file:
        for config in configs:
            file.writelines([f"{k}={v}\n" for k, v in config.items()])
            file.write("\n")
