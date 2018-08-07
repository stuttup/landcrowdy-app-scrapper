# coding: utf-8
from sqlalchemy import Column, Date, DateTime, INTEGER, String, text
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CmdJob(Base):
    __tablename__ = 'cmd_jobs'

    id = Column(INTEGER(10), primary_key=True)
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

    id = Column(INTEGER(10), primary_key=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    telephone = Column(String(20), nullable=False)
    mail = Column(String(100), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50), nullable=False)
    superficie = Column(INTEGER(10), nullable=False)
    prix = Column(INTEGER(10), nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'location'"))
    chambres = Column(INTEGER(2), nullable=False, server_default=text("'0'"))


class CmdTerrain(Base):
    __tablename__ = 'cmd_terrains'

    id = Column(INTEGER(10), primary_key=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    telephone = Column(String(20), nullable=False)
    mail = Column(String(100), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50), nullable=False)
    superficie = Column(String(50), nullable=False)
    prix_m2 = Column(String(50), nullable=False)
    frequence = Column(INTEGER(2), nullable=False, server_default=text("'1'"))
    statut = Column(INTEGER(1), nullable=False, server_default=text("'0'"))
    next_send = Column(DateTime, nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'vente'"))
    titre = Column(TINYINT(1), nullable=False, server_default=text("'1'"))


class ListeJob(Base):
    __tablename__ = 'liste_jobs'

    id = Column(INTEGER(10), primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    lien = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(20), nullable=False)
    domaines = Column(String(100), nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'CDI'"))
    salaire = Column(INTEGER(10), nullable=False, server_default=text("'75000'"))
    date = Column(Date, nullable=False)


class ListeMaison(Base):
    __tablename__ = 'liste_maisons'

    id = Column(INTEGER(10), primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    lien = Column(String(250), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50), nullable=False)
    superficie = Column(INTEGER(10), nullable=False)
    prix = Column(INTEGER(10), nullable=False)
    chambres = Column(INTEGER(2), nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'location'"))
    date = Column(Date, nullable=False)


class ListeTerrain(Base):
    __tablename__ = 'liste_terrains'

    id = Column(INTEGER(10), primary_key=True)
    titre = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    image = Column(String(250), nullable=False)
    pays = Column(String(2), nullable=False)
    ville = Column(String(50), nullable=False)
    quartier = Column(String(50), nullable=False)
    superficie = Column(INTEGER(10), nullable=False)
    prix_m2 = Column(INTEGER(10), nullable=False)
    type = Column(String(20), nullable=False, server_default=text("'vente'"))
    statut = Column(String(20), nullable=False, server_default=text("'titré'"))
    date = Column(Date, nullable=False)
