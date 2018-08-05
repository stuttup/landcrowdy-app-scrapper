from sqlalchemy.orm import Session, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, DateTime, INTEGER, String, text, create_engine, BOOLEAN,ForeignKey
from sqlalchemy.dialects.mysql.types import TINYINT


sql_host = 'host name here'
sql_port = 'Mysql port here'
sql_user = 'database user here'
sql_password = 'database pw here'
sql_database = 'database name here'

connection_string = f"mysql+pymysql://{sql_user}:{sql_password}@{sql_host}:{sql_port}/{sql_database}"

# SqlAlchemy engine setup
engine = create_engine(connection_string)
Base = declarative_base(engine)
metadata = Base.metadata

# database connection object
class DatabaseConnection:

    def __enter__(self):
        # make a database connection and return it
        self.conn = engine.connect()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        # make sure the dbconnection gets closed
        self.conn.close()

# Database session object (needed for tasks like querying)
class DatabaseSession:

    def __enter__(self):
        self.session = Session(engine)

        self.session.expire_on_commit = False

        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None


class CmdJob(Base):
    __tablename__ = 'cmd_jobs'

    id = Column(INTEGER, primary_key=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    mail = Column(String(100), nullable=False)
    secteur = Column(String(50), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    telephone = Column(String(20), nullable=False)
    salaire = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'CDI'"))
    date = Column(Date, nullable=False)


class CmdMaison(Base):
    __tablename__ = 'cmd_maisons'

    id = Column(INTEGER, primary_key=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    telephone = Column(String(20), nullable=False)
    mail = Column(String(100), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50), nullable=False)
    superficie = Column(INTEGER, nullable=False)
    prix = Column(INTEGER, nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'location'"))
    chambres = Column(INTEGER, nullable=False, server_default=text("'0'"))


class CmdTerrain(Base):
    __tablename__ = 'cmd_terrains'

    id = Column(INTEGER, primary_key=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    telephone = Column(String(20), nullable=False)
    mail = Column(String(100), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50), nullable=False)
    superficie = Column(String(50), nullable=False)
    prix_m2 = Column(String(50), nullable=False)
    frequence = Column(INTEGER, nullable=False, server_default=text("'1'"))
    statut = Column(INTEGER, nullable=False, server_default=text("'0'"))
    next_send = Column(DateTime, nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'vente'"))
    titre = Column(TINYINT(1), nullable=False, server_default=text("'1'"))


class ListeJob(Base):
    __tablename__ = 'liste_jobs'

    id = Column(INTEGER, primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    lien = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(20), nullable=False)
    domaines = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'CDI'"))
    salaire = Column(INTEGER, nullable=False, server_default=text("'75000'"))
    date = Column(Date, nullable=False)


class ListeMaison(Base):
    __tablename__ = 'liste_maisons'

    id = Column(INTEGER, primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    lien = Column(String(250), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50), nullable=False)
    superficie = Column(INTEGER, nullable=False)
    prix = Column(INTEGER, nullable=False)
    chambres = Column(INTEGER, nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'location'"))
    date = Column(Date, nullable=False)


class ListeTerrain(Base):
    __tablename__ = 'liste_terrains'

    id = Column(INTEGER, primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50), nullable=False)
    superficie = Column(INTEGER, nullable=False)
    prix_m2 = Column(INTEGER, nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'vente'"))
    statut = Column(String(20), nullable=False, server_default=text("'titr�'"))
    date = Column(Date, nullable=False)
