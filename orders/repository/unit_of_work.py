from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PARENTS_FOLDER = Path(__file__).parent.parent
DATABASE_PATH = PARENTS_FOLDER / Path("orders.db")
SQLITE_CONNECTION_STRING = "sqlite:///" + DATABASE_PATH.as_posix()


class UnitOfWork:
    def __init__(self):
        self.session_maker = sessionmaker(
            bind=create_engine(SQLITE_CONNECTION_STRING)
        )

    def __enter__(self):
        self.session = self.session_maker()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):  
        if exc_type is not None:
            self.rollback()
            self.session.close()
        self.session.close()
    
    def commit(self):
        """Wrapper of SQLAlchemy commit
        """
        self.session.commit()
    
    def rollback(self):
        """Wrapper of SQLAlchemy rollback
        """
        self.session.rollback()
