import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.database import Base, init_db
from app.schemas import (
    ActivitePhysiqueCreate, AlimentCreate, RepasCreate,
    UtilisateurCreate, UtilisateurOut
)
from app.models import (
    ActivitePhysique, Aliment, Repas,
    RepasAliment, Utilisateur, Poids
)


engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        populate_db(db)
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def utilisateurs(db_session: Session):
    user_data = [
        Utilisateur(
            nom="test1",
            email="email1@domain.com",
            mot_de_passe="testxyz",
            age=31,
            poids_initial=78
        ),
        Utilisateur(
            nom="test2",
            email="email2@domain.com",
            mot_de_passe="testxyz",
            age=13,
            poids_initial=87
        )
    ]
    db_session.add_all(user_data)
    db_session.commit()
    return user_data

@pytest.fixture(scope="function")
def aliments(db_session: Session):
    aliments_data = [
        Aliment(
            nom="aliment1",
            calories=1,
            unite="g",
            categorie="categorie1"
        ),
        Aliment(
            nom="aliment2",
            calories=2,
            unite="g",
            categorie="categorie2"
        ),
        Aliment(
            nom="aliment3",
            calories=3,
            unite="g",
            categorie="categorie3"
        )
    ]
    db_session.add_all(aliments_data)
    db_session.commit()
    return aliments_data

@pytest.fixture(scope="function")
def repas(db_session: Session, utilisateurs):
    repas_data = [
        Repas(
            type_repas=f"repas{key}",
            date=datetime.date(2023, 1, 1),
            heure=datetime.time(12, 0),
            utilisateur_id=utilisateur.id
        ) for key, utilisateur in enumerate(utilisateurs)
    ]
    db_session.add_all(repas_data)
    db_session.commit()
    return repas_data

@pytest.fixture(scope="function")
def repas_aliments(db_session: Session, aliments, repas):
    repas_aliments_data = []
    for repa in repas:
        for aliment in aliments:
            repas_aliments_data.append(RepasAliment(
                repas=repa,
                aliment=aliment,
                quantite=100,
                calories_totales=aliment.calories * 100
            ))

    db_session.add_all(repas_aliments_data)
    db_session.commit()
    return repas_aliments_data

def populate_db(db: Session):
    # Utilisateurs
    users = [
        UtilisateurCreate(
            nom="test",
            email="email@domain.com",
            mot_de_passe="testxyz",
            age=31,
            poids_initial=78
        ),
        UtilisateurCreate(
            nom="test2",
            email="email@domain.com",
            mot_de_passe="testzyx",
            age=32,
            poids_initial=78
        )
    ]
    for user in users:
        db_user = Utilisateur(
            nom=user.nom,
            email=user.email,
            mot_de_passe=user.mot_de_passe,
            age=user.age,
            poids_initial=user.poids_initial
        )
        db.add(db_user)
    
    # Aliments
    aliments = [
        AlimentCreate(
            nom="banane",
            calories=100,
            unite="unité",
            categorie="fruits"
        ),
        AlimentCreate(
            nom="pomme",
            calories=100,
            unite="unité",
            categorie="fruits"
        ),
        AlimentCreate(
            nom="carotte",
            calories=100,
            unite="unité",
            categorie="Légumes"
        )
    ]
    for aliment in aliments:
        db_aliment = Aliment(
            nom=aliment.nom,
            calories=aliment.calories,
            unite=aliment.unite,
            categorie=aliment.categorie
        )
        db.add(db_aliment)

    db.commit()
    