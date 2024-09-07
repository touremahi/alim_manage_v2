import datetime

from app.schemas import (
    UtilisateurCreate, AlimentCreate, RepasCreate, 
    ActivitePhysiqueCreate, ListeRepasOut
)
from app.services import (
    create_utilisateur, get_utilisateur, get_utilisateurs,
    update_utilisateur, update_utilisateur_password, delete_utilisateur,
    create_aliment, get_aliment, get_aliments,
    get_aliments_by_categorie, update_aliment, delete_aliment,
    create_repas, get_repas, get_repas_by_type, get_repas_by_date,
    get_repas_by_id, update_repas, delete_repas,
    add_aliment_to_repas, get_repas_aliment, update_repas_aliment,
    create_activite_physique, create_poids, get_total_calories_for_repas,
)

# CRUD test utilisateur
# Create
def test_create_utilisateur(db_session):
    utilisateur = UtilisateurCreate(
        nom="mahinema",
        email="test@test.com",
        mot_de_passe="Monopoly",
        age=18,
        poids_initial=70
    )
    db_utilisateur = create_utilisateur(db=db_session, utilisateur=utilisateur)
    assert db_utilisateur.nom == utilisateur.nom
    assert db_utilisateur.email == utilisateur.email # unique constraint
    assert db_utilisateur.mot_de_passe == utilisateur.mot_de_passe
    assert db_utilisateur.age == utilisateur.age
    assert db_utilisateur.poids_initial == utilisateur.poids_initial

# Read
def test_get_utilisateur(db_session, utilisateurs):
    db_utilisateur = utilisateurs[0]
    db_utilisateur_get = get_utilisateur(db=db_session, id=db_utilisateur.id)
    assert db_utilisateur_get.id == db_utilisateur.id
    assert db_utilisateur_get.nom == db_utilisateur.nom
    assert db_utilisateur_get.email == db_utilisateur.email
    assert db_utilisateur_get.age == db_utilisateur.age
    assert db_utilisateur_get.poids_initial == db_utilisateur.poids_initial

def test_get_utilisateurs(db_session, utilisateurs):
    db_utilisateur = utilisateurs[-1]
    db_utilisateurs = get_utilisateurs(db=db_session)
    db_utilisateur_get = db_utilisateurs[-1]
    assert db_utilisateur_get.id == db_utilisateur.id
    assert db_utilisateur_get.nom == db_utilisateur.nom
    assert db_utilisateur_get.email == db_utilisateur.email
    assert db_utilisateur_get.age == db_utilisateur.age
    assert db_utilisateur_get.poids_initial == db_utilisateur.poids_initial

# Update
def test_update_utilisateur(db_session, utilisateurs):
    db_utilisateur = utilisateurs[-1]

    db_utilisateur_get = get_utilisateur(db=db_session, id=db_utilisateur.id)
    db_utilisateur_get.nom = "mahinema2"
    db_utilisateur_get.age = 20
    db_utilisateur_get.poids_initial = 75
    db_utilisateur_updated = update_utilisateur(db=db_session, utilisateur=db_utilisateur_get)
    assert db_utilisateur_updated.nom == db_utilisateur_get.nom
    assert db_utilisateur_updated.age == db_utilisateur_get.age
    assert db_utilisateur_updated.poids_initial == db_utilisateur_get.poids_initial

# TODO Update password
def test_update_utilisateur_password(db_session, utilisateurs):
    pass

# Delete
def test_delete_utilisateur(db_session, utilisateurs):
    db_utilisateur = utilisateurs[-1]

    db_utilisateur_get = get_utilisateur(db=db_session, id=db_utilisateur.id)
    assert delete_utilisateur(db=db_session, utilisateur=db_utilisateur_get)
    db_utilisateur_get = get_utilisateur(db=db_session, id=db_utilisateur.id)
    assert db_utilisateur_get == None

# CRUD test aliment
# Create
def test_create_aliment(db_session):
    aliment = AlimentCreate(
        nom="Riz",
        calories=100,
        unite="g",
        categorie="Feculents"
    )
    db_aliment = create_aliment(db=db_session, aliment=aliment)
    assert db_aliment.nom == aliment.nom
    assert db_aliment.calories == aliment.calories
    assert db_aliment.unite == aliment.unite
    assert db_aliment.categorie == aliment.categorie

# Read
def test_get_aliment(db_session, aliments):
    db_aliment_get = get_aliment(db=db_session, id=aliments[-1].id)
    assert db_aliment_get.id == aliments[-1].id
    assert db_aliment_get.nom == aliments[-1].nom
    assert db_aliment_get.calories == aliments[-1].calories
    assert db_aliment_get.unite == aliments[-1].unite
    assert db_aliment_get.categorie == aliments[-1].categorie

def test_get_aliments(db_session, aliments):
    db_aliments = get_aliments(db=db_session)
    assert db_aliments[-1].id == aliments[-1].id
    assert db_aliments[-1].nom == aliments[-1].nom
    assert db_aliments[-1].calories == aliments[-1].calories
    assert db_aliments[-1].unite == aliments[-1].unite
    assert db_aliments[-1].categorie == aliments[-1].categorie

def test_get_aliments_by_categorie(db_session, aliments):
    db_aliments = get_aliments_by_categorie(
        db=db_session,
        categorie=aliments[-1].categorie
    )
    for db_aliment_get in db_aliments:
        assert db_aliment_get.categorie == aliments[-1].categorie

# Update
def test_update_aliment(db_session, aliments):
    db_aliment_get = get_aliment(db=db_session, id=aliments[-1].id)
    db_aliment_get.nom = "Yaourt"
    db_aliment_get.calories = 150
    db_aliment_get.unite = "g"
    db_aliment_get.categorie = "Laitage"
    db_aliment_updated = update_aliment(db=db_session, aliment=db_aliment_get)

    assert db_aliment_updated.nom == db_aliment_get.nom
    assert db_aliment_updated.calories == db_aliment_get.calories
    assert db_aliment_updated.unite == db_aliment_get.unite
    assert db_aliment_updated.categorie == db_aliment_get.categorie
    assert db_aliment_updated.id == db_aliment_get.id

# Delete
def test_delete_aliment(db_session, aliments):
    db_aliment_get = get_aliment(db=db_session, id=aliments[-1].id)
    assert delete_aliment(db=db_session, aliment=db_aliment_get)
    db_aliment_get = get_aliment(db=db_session, id=aliments[-1].id)
    assert db_aliment_get == None

# CRUD test repas
# Create
def test_create_repas(db_session, utilisateurs):
    utilisateur_get = get_utilisateur(db=db_session, id=utilisateurs[-1].id)
    repas = RepasCreate(
        type_repas="Déjeuner",
        date=datetime.date(2024,9,10),
        heure=datetime.time(10,0,0),
        utilisateur=utilisateur_get
    )
    db_repas = create_repas(db=db_session, repas=repas)
    assert db_repas.type_repas == repas.type_repas
    assert db_repas.date == repas.date
    assert db_repas.heure == repas.heure
    assert db_repas.utilisateur_id == utilisateur_get.id

# test add aliment to repas
def test_add_aliment_to_repas(db_session, aliments, repas):

    db_aliment_get = get_aliment(db=db_session, id=aliments[-1].id)
    db_repas_aliment = add_aliment_to_repas(
        db=db_session,
        repas_id=repas[-1].id,
        aliment=db_aliment_get,
        quantite=100
    )
    assert db_repas_aliment.quantite == 100
    assert db_repas_aliment.repas_id == repas[-1].id
    assert db_repas_aliment.aliment_id == db_aliment_get.id
    assert db_repas_aliment.calories_totales == 100 * db_aliment_get.calories

# Read
def test_get_repas(db_session, utilisateurs, repas, repas_aliments):
    utilisateur_get = get_utilisateur(db=db_session, id=utilisateurs[-1].id)

    db_repas_get = get_repas(db=db_session, utilisateur=utilisateur_get)
    
    assert db_repas_get != None
    assert db_repas_get[-1].id == repas[-1].id
    assert db_repas_get[-1].type_repas == repas[-1].type_repas
    assert db_repas_get[-1].date == repas[-1].date
    assert db_repas_get[-1].heure == repas[-1].heure

# TODO 
def test_get_repas_by_date(db_session, utilisateurs, repas, repas_aliments):
    utilisateur_get = get_utilisateur(db=db_session, id=utilisateurs[-1].id)

    db_repas_get = get_repas_by_date(
        db=db_session,
        utilisateur=utilisateur_get,
        date=repas[-1].date
    )
    assert db_repas_get != None
    for repa in db_repas_get:
        assert repa.date == repas[-1].date

# TODO 
def test_get_repas_by_type(db_session, utilisateurs, repas, repas_aliments):
    utilisateur_get = get_utilisateur(db=db_session, id=utilisateurs[-1].id)

    db_repas_get = get_repas_by_type(
        db=db_session,
        utilisateur=utilisateur_get,
        type_repas=repas[-1].type_repas
    )
    assert db_repas_get != None
    for repa in db_repas_get:
        assert repa.type_repas == repas[-1].type_repas

# TODO
def test_get_repas_by_id(db_session, utilisateurs, repas, repas_aliments):
    repas_db_get = get_repas_by_id(db=db_session, id=repas[-1].id)
    assert repas_db_get != None
    assert repas_db_get.id == repas[-1].id
    assert repas_db_get.type_repas == repas[-1].type_repas
    assert repas_db_get.date == repas[-1].date
    assert repas_db_get.heure == repas[-1].heure

# Update
def test_update_repas(db_session, repas):
    repas_get = get_repas_by_id(db=db_session, id=repas[-1].id)
    repas_get.type_repas = "Déjeuner"
    repas_get.date = datetime.date(2024,9,10)
    repas_get.heure = datetime.time(10,0,0)
    repas_updated = update_repas(db=db_session, repas=repas_get)
    
    assert repas_updated.type_repas == repas_get.type_repas
    assert repas_updated.date == repas_get.date
    assert repas_updated.heure == repas_get.heure
    assert repas_updated.id == repas_get.id

# Delete
def test_delete_repas(db_session, repas, repas_aliments):
    repas_get = get_repas_by_id(db=db_session, id=repas[-1].id)
    assert delete_repas(db=db_session, repas=repas_get)
    repas_get = get_repas_by_id(db=db_session, id=repas[-1].id)
    assert repas_get == None

# CRUD test repas_aliment
# Create
def test_create_repas_aliment(db_session):
    pass

# Read
def test_get_repas_aliment(db_session, repas_aliments): 
    repas_aliment_get = get_repas_aliment(
        db=db_session,
        repas_id=repas_aliments[0].repas_id,
        aliment_id=repas_aliments[0].aliment_id
    )

    assert repas_aliment_get != None
    assert repas_aliment_get.repas_id == repas_aliments[0].repas_id
    assert repas_aliment_get.aliment == repas_aliments[0].aliment_id
    assert repas_aliment_get.quantite == repas_aliments[0].quantite
    assert repas_aliment_get.calories_totales == repas_aliments[0].calories_totales

#  Update
def test_update_repas_aliment(db_session):
    pass

# Delete
def test_delete_repas_aliment(db_session):
    pass
