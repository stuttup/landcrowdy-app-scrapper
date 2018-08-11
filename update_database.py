# -*- coding: utf-8 -*-
from datetime import datetime
import json
from jumia.database import DatabaseSession, ListeMaison, ListeTerrain, ListeJob


def delete_records():
    with DatabaseSession() as session:
        print("Removing previous records")
        try:
            session.query(ListeMaison).delete()
            session.query(ListeTerrain).delete()
            session.query(ListeJob).delete()
            session.commit()
        except:
            session.rollback()

def insert_records():
    with DatabaseSession() as session:
        print("Inserting new records")
        with open('maisons.json') as f:
            maisons = json.load(f)
        with open('terrains.json') as f:
            terrains = json.load(f)
        with open('jobs.json') as f:
            jobs = json.load(f)

        for maison in maisons:
            m = ListeMaison(titre=maison.get('titre', 'Test'), description=maison.get('description', ''),
                            image=maison.get('image', ''), lien=maison.get('lien', ''), pays='SN',
                            ville=maison.get('lieu', ''), quartier=maison.get('lieu', ''), superficie=maison.get('superficie'),
                            prix=maison.get('prix', 0), chambres=maison.get('chambres', 1), type=maison.get('type', 'location'),
                            date=datetime.strptime(maison.get('date', "7-8-2018 11:30").replace('.', '-'), '%d-%m-%Y %H:%M').date())
            try:
                session.add(m)
            except Exception as e:
                print(e)
                session.rollback()

        for terrain in terrains:
            t = ListeTerrain(titre=terrain.get('titre', 'Annonce'), description=terrain.get('description', ''),
                            image=terrain.get('image', ''), pays='SN',
                            ville=terrain.get('lieu', ''), quartier=terrain.get('lieu', ''), superficie=terrain.get('superficie', '0'),
                            prix=terrain.get('prix', '0'), type=terrain.get('type', 'location'), statut=terrain.get('statut'),
                            date=datetime.strptime(terrain.get('date', "7-8-2018 11:30").replace('.', '-'), '%d-%m-%Y %H:%M').date(),
                             lien=terrain.get('lien', ''), )
            try:
                session.add(t)
            except Exception as e:
                print(e)
                session.rollback()

        for job in jobs:
            j = ListeJob(titre=job.get('titre', 'Annonce'), description=job.get('description', ''),
                            image=job.get('image', ''), lien=job.get('lien', ''), pays='SN',
                            ville=job.get('lieu', ''), domaines=job.get('lieu', ''),
                            salaire=job.get('prix', 0), type=job.get('type', 'location'),
                            date=datetime.strptime(job.get('date', "7-8-2018 11:30").replace('.', '-'), '%d-%m-%Y %H:%M').date())
            try:
                session.add(j)
            except Exception as e:
                print(e)
                session.rollback()

        session.commit()

if __name__ == '__main__':
    delete_records()
    insert_records()