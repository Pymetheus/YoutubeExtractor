from sqlalchemy_dbtoolkit.engine.factory import AlchemyEngineFactory
from sqlalchemy_dbtoolkit.orm.base import ORMBaseManager
from sqlalchemy_dbtoolkit.query.create import InsertManager
from src.database_models import Song, Video


class DatabaseOperations:
    """
    Handles database engine creation, table definitions, and data insertion.
    """

    def __init__(self, dbms="sqlite", db_name="youtube_archive"):
        """
        Initialize database connection and ORM base manager.

        Args:
            dbms (str): Database management system ('sqlite', 'mysql', 'postgresql').
            db_name (str): Name of the target database.
        """

        self.db_name = db_name
        self.dbms = dbms
        self.engine = self.get_engine()

        self.TableManager = ORMBaseManager(self.engine)
        self.Base = self.TableManager.Base

        self.music_table = Song
        self.video_table = Video

    def get_engine(self):
        """
        Create SQLAlchemy engine using provided DBMS and config.

        Returns:
            sqlalchemy.engine.Engine: SQLAlchemy engine object.

        Raises:
            ConnectionError: If engine creation fails.
        """

        try:
            DBEngine = AlchemyEngineFactory(dbms=self.dbms, db_name=self.db_name, config_path='../.config/config.ini')
            return DBEngine.engine
        except Exception as e:
            raise ConnectionError(f"Failed to create SQLAlchemy engine: {e}")

    def create_tables_if_not_exists(self):
        """
        Create database tables if they do not already exist.
        """

        try:
            self.TableManager.create_tables_if_not_exists()
        except Exception as e:
            raise RuntimeError(f"Failed to create database tables: {e}")

    def insert_data_in_table(self, Table, data):
        """
        Insert a row of metadata into the specified table.

        Args:
            Table (SQLAlchemy Table): SQLAlchemy model class.
            data (tuple): A 7-element tuple of metadata (title, artists, track, album, duration, filename, original_url).

        Raises:
            ValueError: If insertion fails or data is malformed.
        """

        try:
            if len(data) != 7:
                raise ValueError("Expected 7 elements in metadata tuple.")

            insert_query = InsertManager(self.engine)
            data = {"title": data[0],
                    "artists": data[1],
                    "track": data[2],
                    "album": data[3],
                    "duration": data[4],
                    "filename": data[5],
                    "original_url": data[6],
                    }
            insert_query.add_row(Table, data)
        except Exception as e:
            raise ValueError(f"Failed to insert metadata: {e}")
