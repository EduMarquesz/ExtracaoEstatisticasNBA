from typing import Tuple, Any

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:

    def __init__(self) -> None:
        self.__connection_string = "postgresql+psycopg2://postgres:123@localhost:5432/nba_statistics"
        self.__engine = self.__create_database_engine()
        self.session = None


    def __create_database_engine(self) -> Tuple[Any]:
        engine = create_engine(self.__connection_string)
        return engine
    

    def get_engine(self) -> Tuple[Any]:
        return self.__engine
    

    def __enter__(self) -> Any:
        session_make = sessionmaker(bind = self.__engine)
        self.session = session_make()
        return self
    

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.session.close()