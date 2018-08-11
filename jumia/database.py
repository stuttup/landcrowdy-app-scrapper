from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, DateTime, INTEGER, String, text, create_engine


sql_host = 'host here'
sql_port = 'port here'
sql_user = 'user here'
sql_password = 'pw here'
sql_database = 'db here'

connection_string = f"mysql+pymysql://{sql_user}:{sql_password}@{sql_host}:{sql_port}/{sql_database}"

# SqlAlchemy engine setup
engine = create_engine(connection_string)
Base = declarative_base(engine)
metadata = Base.metadata

# database connection object
class DatabaseConnection:
    """Database connection object context manager

    """

    def __enter__(self):
        self.conn = engine.connect()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


class DatabaseSession:
    """Database session object with context manager

    """
    def __enter__(self):
        self.session = Session(engine)
        self.session.expire_on_commit = False
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None


## Models generated with Sqlacodegen : sqlacodegen mysql+pymysql://[USER]:[PASSWD]@[HOST]:[DB_PORT]/[DB] > jumia/models.py

class ListeJob(Base):
    __tablename__ = 'liste_jobs'

    id = Column(INTEGER, primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250))
    lien = Column(String(250), nullable=False)
    image = Column(String(250))
    pays = Column(String(2), nullable=False)
    ville = Column(String(20))
    domaines = Column(String(100))
    type = Column(String(20), server_default=text("'CDI'"))
    salaire = Column(String(50))
    date = Column(Date, nullable=False)


class ListeMaison(Base):
    __tablename__ = 'liste_maisons'

    id = Column(INTEGER, primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250))
    image = Column(String(250))
    lien = Column(String(250), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50))
    quartier = Column(String(50))
    superficie = Column(String(20))
    prix = Column(String(20))
    chambres = Column(String(20))
    type = Column(String(20), server_default=text("'location'"))
    date = Column(Date, nullable=False)


class ListeTerrain(Base):
    __tablename__ = 'liste_terrains'

    id = Column(INTEGER, primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250))
    image = Column(String(250))
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50))
    superficie = Column(String(50))
    prix = Column(String(50))
    type = Column(String(20), server_default=text("'vente'"))
    statut = Column(String(20), server_default=text("'titr�'"))
    date = Column(Date, nullable=False)
    lien = Column(String(250))


class Newsletter(Base):
    __tablename__ = 'newsletter'

    id = Column(INTEGER, primary_key=True)
    telephone = Column(String(20), nullable=False)
    mail = Column(String(100))
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    quartier = Column(String(50), nullable=False)
    last_send = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))