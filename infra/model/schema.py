from sqlalchemy import (
    Column, String,
    Integer, NUMERIC
)

from infra.configs.base import Base


class nba_statistics(Base):
    __tablename__ = 'nba_statistics'

    id = Column(
        Integer, nullable=False,
        primary_key=True, autoincrement=True
    )
    name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    height = Column(NUMERIC, nullable=True)
    team_name = Column(String, nullable=True)
    team_city = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f'nba_statistics(ID: {self.id}, NAME: {self.name})'