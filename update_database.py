# -*- coding: utf-8 -*-
from datetime import datetime
import json
from jumia.database import DatabaseSession, ListeMaison


def delete_records():
    with DatabaseSession() as session:
        print("Removing previous records")
        try:
            session.query(ListeMaison).delete()
            session.commit()
        except:
            session.rollback()

def insert_records():
    with DatabaseSession() as session:
        print("Inserting new records")
        with open('scraper_output.json') as f:
            records = json.load(f)

        for record in records:
            m = ListeMaison(titre=record.get('titre', 'Test'), description=record.get('description', ''),
                            image=record.get('image', ''), lien=record.get('lien', ''), pays='SN',
                            ville=record.get('lieu', ''), quartier=record.get('lieu', ''), superficie=record.get('superficie', 0),
                            prix=record.get('prix', 0), chambres=record.get('type', 1), type=record.get('type', 'location'),
                            date=datetime.strptime(record.get('date', "7-8-2018 11:30"), '%d-%m-%Y %H:%M').date())
            try:
                session.add(m)
            except Exception as e:
                print(e)
                session.rollback()
        session.commit()
