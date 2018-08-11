# coding: utf-8
from sqlalchemy import Column, Date, DateTime, INTEGER, String, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ListeJob(Base):
    __tablename__ = 'liste_jobs'

    id = Column(INTEGER(10), primary_key=True)
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

    id = Column(INTEGER(10), primary_key=True)
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

    id = Column(INTEGER(10), primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250))
    image = Column(String(250))
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50))
    superficie = Column(String(50))
    prix = Column(String(50))
    type = Column(String(20), server_default=text("'vente'"))
    statut = Column(String(20), server_default=text("'titré'"))
    date = Column(Date, nullable=False)
    lien = Column(String(250))


class Newsletter(Base):
    __tablename__ = 'newsletter'

    id = Column(INTEGER(10), primary_key=True)
    telephone = Column(String(20), nullable=False)
    mail = Column(String(100))
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    type = Column(String(20), nullable=False)
    quartier = Column(String(50), nullable=False)
    last_send = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
