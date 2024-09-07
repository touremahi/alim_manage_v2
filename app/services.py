import datetime

from sqlalchemy import func

from sqlalchemy.orm import Session
from .models import (
    Aliment, Repas, RepasAliment,
    Utilisateur, ActivitePhysique, Poids
)
from .schemas import (
    UtilisateurCreate, UtilisateurOut,
    AlimentCreate, AlimentOut,
    RepasAlimentOut, RepasCreate, RepasAlimentOutOne,
    RepasOut, ListeRepasOut,
    ActivitePhysiqueCreate, ActivitePhysiqueOut,
    PoidsOut, PoidsBase
    
)

# utilisateur CRUD
# Create
def create_utilisateur(db: Session, utilisateur: UtilisateurCreate):
    db_utilisateur = Utilisateur(
        nom=utilisateur.nom,
        email=utilisateur.email,
        mot_de_passe=utilisateur.mot_de_passe,
        age=utilisateur.age,
        poids_initial=utilisateur.poids_initial
    )
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur

# Read
def get_utilisateur(db: Session, id: int):
    db_utilisateur = db.query(Utilisateur).filter(Utilisateur.id == id).first()
    if db_utilisateur:
        selected_utilisateur = UtilisateurOut(
            id=db_utilisateur.id,
            nom=db_utilisateur.nom,
            email=db_utilisateur.email,
            age=db_utilisateur.age,
            poids_initial=db_utilisateur.poids_initial
        )
        return selected_utilisateur
    return None

def get_utilisateurs(db: Session):
    users = db.query(Utilisateur).all()
    selected_utilisateurs = [
        UtilisateurOut(
            id=user.id,
            nom=user.nom,
            email=user.email,
            age=user.age,
            poids_initial=user.poids_initial
        ) for user in users
    ]
    return selected_utilisateurs

# Update except email and password
def update_utilisateur(db: Session, utilisateur: UtilisateurOut):
    db_utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur.id).first()
    if db_utilisateur:
        db_utilisateur.nom = utilisateur.nom
        db_utilisateur.age = utilisateur.age
        db_utilisateur.poids_initial = utilisateur.poids_initial
        db.commit()
        db.refresh(db_utilisateur)
        selected_utilisateur = UtilisateurOut(
            id=db_utilisateur.id,
            nom=db_utilisateur.nom,
            email=db_utilisateur.email,
            age=db_utilisateur.age,
            poids_initial=db_utilisateur.poids_initial
        )
        return selected_utilisateur
    return None

# TODO Update password
def update_utilisateur_password(db: Session, utilisateur: UtilisateurOut, new_password: str):
    pass

# Delete
def delete_utilisateur(db: Session, utilisateur: UtilisateurOut):
    db_utilisateur = db.query(Utilisateur).filter(Utilisateur.id == utilisateur.id).first()
    if db_utilisateur:
        db.delete(db_utilisateur)
        db.commit()
        return True
    return False

# aliment CRUD
def create_aliment(db: Session, aliment: AlimentCreate):
    db_aliment = Aliment(
        nom=aliment.nom,
        calories=aliment.calories,
        unite=aliment.unite,
        categorie=aliment.categorie
    )
    db.add(db_aliment)
    db.commit()
    db.refresh(db_aliment)
    return db_aliment

# Read
def get_aliment(db: Session, id: int):
    db_aliment = db.query(Aliment).filter(Aliment.id == id).first()
    if db_aliment:
        selected_aliment = AlimentOut(
            id=db_aliment.id,
            nom=db_aliment.nom,
            calories=db_aliment.calories,
            unite=db_aliment.unite,
            categorie=db_aliment.categorie
        )
        return selected_aliment
    return None

def get_aliments(db: Session):
    aliments = db.query(Aliment).all()
    selected_aliments = [
        AlimentOut(
            id=aliment.id,
            nom=aliment.nom,
            calories=aliment.calories,
            unite=aliment.unite,
            categorie=aliment.categorie
        ) for aliment in aliments
    ]
    return selected_aliments

def get_aliments_by_categorie(db: Session, categorie: str):
    aliments = db.query(Aliment).filter(Aliment.categorie == categorie).all()
    selected_aliments = [
        AlimentOut(
            id=aliment.id,
            nom=aliment.nom,
            calories=aliment.calories,
            unite=aliment.unite,
            categorie=aliment.categorie
        ) for aliment in aliments 
    ]
    return selected_aliments

#  Update
def update_aliment(db: Session, aliment: AlimentOut):
    db_aliment = db.query(Aliment).filter(Aliment.id == aliment.id).first()
    if db_aliment:
        db_aliment.nom = aliment.nom
        db_aliment.calories = aliment.calories
        db_aliment.unite = aliment.unite
        db_aliment.categorie = aliment.categorie
        db.commit()
        db.refresh(db_aliment)
        selected_aliment = AlimentOut(
            id=db_aliment.id,
            nom=db_aliment.nom,
            calories=db_aliment.calories,
            unite=db_aliment.unite,
            categorie=db_aliment.categorie
        )
        return selected_aliment
    return None

# Delete
def delete_aliment(db: Session, aliment: AlimentOut):
    db_aliment = db.query(Aliment).filter(Aliment.id == aliment.id).first()
    if db_aliment:
        db.delete(db_aliment)
        db.commit()
        return True
    return False

# repas CRUD
# Create
def create_repas(db: Session, repas: RepasCreate):
    db_repas = Repas(
        type_repas=repas.type_repas,
        date=repas.date,
        heure=repas.heure,
        utilisateur_id=repas.utilisateur.id
    )
    db.add(db_repas)
    db.commit()
    db.refresh(db_repas)
    return db_repas

# Read
# Utils
def query_repas(db: Session, db_repas: list):
    repas_data = []
    for repas in db_repas:
        aliments_r = db.query(RepasAliment).filter(RepasAliment.repas_id == repas.id).all()
        aliments_r_list = [
            RepasAlimentOut(
                aliment = get_aliment(db, aliment.aliment_id),
                quantite = aliment.quantite,
                calories_totales = aliment.calories_totales,
            ) for aliment in aliments_r
        ]
        selected_repas = ListeRepasOut(
            id=repas.id,
            type_repas=repas.type_repas,
            date=repas.date,
            heure=repas.heure,
            aliments=aliments_r_list
        )
        repas_data.append(selected_repas)
    return repas_data

# Read
def get_repas(db: Session, utilisateur: UtilisateurOut):
    db_repas = db.query(Repas).filter(Repas.utilisateur_id == utilisateur.id).all()
    if db_repas:
        return query_repas(db, db_repas)
    return None

def get_repas_by_id(db: Session, id: int):
    db_repas = db.query(Repas).filter(Repas.id == id).first()
    if db_repas:
        return query_repas(db, [db_repas])[0]
    return None

# Read by type
def get_repas_by_type(db: Session, type_repas: str, utilisateur: UtilisateurOut):
    db_repas = db.query(Repas).filter(Repas.type_repas == type_repas, Repas.utilisateur_id == utilisateur.id).all()
    if db_repas:
        return query_repas(db, db_repas)
    return None

# Read by date
def get_repas_by_date(db: Session, date: datetime.date, utilisateur: UtilisateurOut):
    db_repas = db.query(Repas).filter(Repas.date == date, Repas.utilisateur_id == utilisateur.id).all()
    if db_repas:
        return query_repas(db, db_repas)
    return None

# Update
def update_repas(db: Session, repas: RepasOut):
    db_repas = db.query(Repas).filter(Repas.id == repas.id).first()
    if db_repas:
        db_repas.type_repas = repas.type_repas
        db_repas.date = repas.date
        db_repas.heure = repas.heure
        db.commit()
        db.refresh(db_repas)
        selected_repas = RepasOut(
            id=db_repas.id,
            type_repas=db_repas.type_repas,
            date=db_repas.date,
            heure=db_repas.heure
        )
        return selected_repas
    return None

# Delete
def delete_repas(db: Session, repas: RepasOut):
    db_repas = db.query(Repas).filter(Repas.id == repas.id).first()
    if db_repas:
        db.delete(db_repas)
        db.commit()
        return True
    return False

# repas_aliment CRUD
def add_aliment_to_repas(db: Session, repas_id: int, aliment: AlimentOut, quantite: float):
    db_repas_aliment = RepasAliment(
        repas_id=repas_id,
        aliment_id=aliment.id,
        quantite=quantite,
        calories_totales=aliment.calories * quantite
    )
    db.add(db_repas_aliment)
    db.commit()
    db.refresh(db_repas_aliment)
    return db_repas_aliment

# TODO: Read
def get_repas_aliment(db: Session, repas_id: int, aliment_id: int):
    db_repas_aliment = db.query(RepasAliment)\
        .join(Repas, RepasAliment.repas_id == Repas.id)\
        .join(Aliment, RepasAliment.aliment_id == Aliment.id)\
        .filter(Repas.id == repas_id, Aliment.id == aliment_id).first()
    if db_repas_aliment:
        repas_aliment = RepasAlimentOutOne(
            aliment = get_aliment(db, db_repas_aliment.aliment_id),
            quantite = db_repas_aliment.quantite,
            calories_totales = db_repas_aliment.calories_totales,
            repas_id = repas_id
        )
        return repas_aliment
    return None

# TODO: Update
def update_repas_aliment(db: Session, repas_aliment: RepasAlimentOutOne):
    db_repas_aliment = db.query(RepasAliment)\
    .join(Repas, RepasAliment.repas_id == Repas.id)\
    .join(Aliment, RepasAliment.aliment_id == Aliment.id)\
    .filter(Repas.id == repas_aliment.repas_id, Aliment.id == repas_aliment.aliment.id).first()
    if db_repas_aliment:
        db_repas_aliment.quantite = repas_aliment.quantite
        db_repas_aliment.calories_totales = repas_aliment.calories_totales
        db.commit()
        db.refresh(db_repas_aliment)
        selected_repas_aliment = RepasAlimentOutOne(
            aliment = get_aliment(db, db_repas_aliment.aliment_id),
            quantite = db_repas_aliment.quantite,
            calories_totales = db_repas_aliment.calories_totales,
            repas_id = db_repas_aliment.repas_id
        )
        return selected_repas_aliment
    return None

# TODO: Delete
def delete_repas_aliment(db: Session, repas_aliment: RepasAlimentOutOne):
    db_repas_aliment = db.query(RepasAliment)\
        .join(Repas, RepasAliment.repas_id == Repas.id)\
        .join(Aliment, RepasAliment.aliment_id == Aliment.id)\
        .filter(Repas.id == repas_aliment.repas_id, Aliment.id == repas_aliment.aliment.id).first()
    if db_repas_aliment:
        db.delete(db_repas_aliment)
        db.commit()
        return True
    return False

# activité physique CRUD
def create_activite_physique(db: Session, activite: ActivitePhysiqueCreate, utilisateur_id: int):
    db_activite = ActivitePhysique(
        type_activite=activite.type_activite,
        date=activite.date,
        heure=activite.heure,
        duree=activite.duree,
        utilisateur_id=utilisateur_id
    )
    db.add(db_activite)
    db.commit()
    db.refresh(db_activite)
    return db_activite

# TODO: Read
def create_activite_physique():
    pass

# TODO: Update
def update_activite_physique():
    pass

# TODO: Delete
def delete_activite_physique():
    pass

# poids CRUD
def create_poids(db: Session, poids: float, utilisateur_id: int):
    db_poids = Poids(
        poids=poids,
        utilisateur_id=utilisateur_id
    )
    db.add(db_poids)
    db.commit()
    db.refresh(db_poids)
    return db_poids

# TODO: Read
def get_poids():
    pass

# TODO: Update
def update_poids():
    pass

# TODO: Delete
def delete_poids():
    pass

def get_total_calories_for_repas(db: Session, repas_id: int):
    total_calories = db.query(
        func.sum(RepasAliment.calories_totales)
    ).filter(RepasAliment.repas_id == repas_id).scalar()
    return total_calories
