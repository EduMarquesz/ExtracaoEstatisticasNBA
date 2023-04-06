import logging
from typing import Dict, List, Any, Tuple

import sqlalchemy as sa

from infra.configs.dbconnect import DBConnectionHandler
from infra.model.schema import nba_statistics
from infra.configs.base import Base


class nbaRepository:
    def select_all(self) -> List[Tuple[Any]]:
        with DBConnectionHandler() as db:
            data = db.session.query(nba_statistics).all()
            return data
    

    def create_table(self) -> None:
        with DBConnectionHandler() as db:
            engine = db.get_engine()
            check_table = engine.dialect.has_table(engine.connect(), "nba_statistics")
            
            if not check_table:
                Base.metadata.create_all(engine)
                logging.info('Table created')


    def insert_db(self, info: List[Dict[str, Any]]) -> None:
        with DBConnectionHandler() as db:
            db.session.bulk_insert_mappings(
                nba_statistics, info
            )
            # Pega as linhas duplicadas e as deleta
            group_query = db.session.query(sa.func.min(nba_statistics.id)).group_by(nba_statistics.name)
            duplicate_query = db.session.query(nba_statistics).filter(~nba_statistics.id.in_(group_query))
            for name in duplicate_query:
                db.session.delete(name)
            db.session.commit()
            logging.info('Data entered into the table')