import datetime

from app.schemas import (
    UtilisateurCreate, AlimentCreate, RepasCreate, 
    ActivitePhysiqueCreate, PoidsCreate
)
from app.services import (
    create_utilisateur, get_utilisateur, get_utilisateurs,
    update_utilisateur, update_utilisateur_password, delete_utilisateur,
    create_aliment, get_aliment, get_aliments,
    get_aliments_by_categorie, update_aliment, delete_aliment,
    create_repas, get_repas, get_repas_by_type, get_repas_by_date,
    get_repas_by_id, update_repas, delete_repas,
    add_aliment_to_repas, get_repas_aliment, update_repas_aliment,
    delete_repas_aliment,
    create_activite_physique, get_activite_physique, update_activite_physique,
    delete_activite_physique, create_poids, get_poids, update_poids,
    delete_poids, get_total_calories_for_repas
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

# Update password
def test_update_utilisateur_password(db_session, utilisateurs):
    pass

# Delete
def test_delete_utilisateur(db_session, utilisateurs):
    db_utilisateur = utilisateurs[-1]

    assert delete_utilisateur(db=db_session, utilisateur_id=db_utilisateur.id)
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
    aliment_update = AlimentCreate(
        nom="Yaourt",
        calories=150,
        unite="g",
        categorie="Laitage"
    )
    db_aliment_updated = update_aliment(db=db_session, id=aliments[-1].id, aliment=aliment_update)

    assert db_aliment_updated.nom == aliment_update.nom
    assert db_aliment_updated.calories == aliment_update.calories
    assert db_aliment_updated.unite == aliment_update.unite
    assert db_aliment_updated.categorie == aliment_update.categorie
    assert db_aliment_updated.id == aliments[-1].id

# Delete
def test_delete_aliment(db_session, aliments):
    assert delete_aliment(db=db_session, id=aliments[-1].id)
    db_aliment_get = get_aliment(db=db_session, id=aliments[-1].id)
    assert db_aliment_get == None

# CRUD test repas
# Create
def test_create_repas(db_session, utilisateurs):
    repas = RepasCreate(
        type_repas="Déjeuner",
        date=datetime.date(2024,9,10),
        heure=datetime.time(10,0,0),
        utilisateur_id=utilisateurs[-1].id
    )
    db_repas = create_repas(db=db_session, repas=repas)
    assert db_repas.type_repas == repas.type_repas
    assert db_repas.date == repas.date
    assert db_repas.heure == repas.heure
    assert db_repas.utilisateur_id == utilisateurs[-1].id

# test add aliment to repas
def test_add_aliment_to_repas(db_session, aliments, repas):

    db_aliment_get = get_aliment(db=db_session, id=aliments[-1].id)
    db_repas_aliment = add_aliment_to_repas(
        db=db_session,
        repas_id=repas[-1].id,
        aliment_id=aliments[-1].id,
        quantite=100
    )
    assert db_repas_aliment.quantite == 100
    assert db_repas_aliment.repas_id == repas[-1].id
    assert db_repas_aliment.aliment_id == aliments[-1].id
    assert db_repas_aliment.calories_totales == 100 * db_aliment_get.calories

# Read
def test_get_repas(db_session, utilisateurs, repas, repas_aliments):
    db_repas_get = get_repas(db=db_session, utilisateur_id=utilisateurs[-1].id)
    
    assert db_repas_get != None
    assert db_repas_get[-1].id == repas[-1].id
    assert db_repas_get[-1].type_repas == repas[-1].type_repas
    assert db_repas_get[-1].date == repas[-1].date
    assert db_repas_get[-1].heure == repas[-1].heure

# test get repas by date
def test_get_repas_by_date(db_session, utilisateurs, repas, repas_aliments):
    db_repas_get = get_repas_by_date(
        db=db_session,
        utilisateur_id=utilisateurs[-1].id,
        date=repas[-1].date
    )
    assert db_repas_get != None
    for repa in db_repas_get:
        assert repa.date == repas[-1].date

# test get repas by type
def test_get_repas_by_type(db_session, utilisateurs, repas, repas_aliments):
    db_repas_get = get_repas_by_type(
        db=db_session,
        utilisateur_id=utilisateurs[-1].id,
        type_repas=repas[-1].type_repas
    )
    assert db_repas_get != None
    for repa in db_repas_get:
        assert repa.type_repas == repas[-1].type_repas

# test get repas by id
def test_get_repas_by_id(db_session, utilisateurs, repas, repas_aliments):
    repas_db_get = get_repas_by_id(db=db_session, id=repas[-1].id)
    assert repas_db_get != None
    assert repas_db_get.id == repas[-1].id
    assert repas_db_get.type_repas == repas[-1].type_repas
    assert repas_db_get.date == repas[-1].date
    assert repas_db_get.heure == repas[-1].heure

# Update
def test_update_repas(db_session, repas):
    repas_update = RepasCreate(
        type_repas="Déjeuner",
        date=datetime.date(2024,9,10),
        heure=datetime.time(10,0,0),
        utilisateur_id=repas[-1].utilisateur_id
    )
    repas_updated = update_repas(
        db=db_session,
        id=repas[-1].id,
        repas=repas_update
    )
    
    assert repas_updated.type_repas == repas_update.type_repas
    assert repas_updated.date == repas_update.date
    assert repas_updated.heure == repas_update.heure
    assert repas_updated.id == repas[-1].id

# Delete
def test_delete_repas(db_session, repas):
    assert delete_repas(db=db_session, id=repas[-1].id)
    repas_get = get_repas_by_id(db=db_session, id=repas[-1].id)
    assert repas_get == None

# CRUD test repas_aliment
# Create
def test_create_repas_aliment(db_session):
    pass

# Read
def test_get_repas_aliment(db_session, repas_aliments):
    id_repas = repas_aliments[-1].repas_id
    id_aliment = repas_aliments[-1].aliment_id
    quantite = repas_aliments[-1].quantite
    calories_totales = repas_aliments[-1].calories_totales
    repas_aliment_get = get_repas_aliment(
        db=db_session,
        repas_id=id_repas,
        aliment_id=id_aliment
    )

    assert repas_aliment_get != None
    assert repas_aliment_get.repas_id == id_repas
    assert repas_aliment_get.aliment_id == id_aliment
    assert repas_aliment_get.quantite == quantite
    assert repas_aliment_get.calories_totales == calories_totales

#  Update
def test_update_repas_aliment(db_session, repas_aliments):
    id_repas = repas_aliments[-1].repas_id
    id_aliment = repas_aliments[-1].aliment_id
    repas_aliment_get = get_repas_aliment(
        db=db_session,
        repas_id=id_repas,
        aliment_id=id_aliment
    )
    repas_aliment_get.quantite = 120
    repas_aliment_updated = update_repas_aliment(
        db=db_session,
        repas_aliment=repas_aliment_get
    )
    assert repas_aliment_updated.quantite == 120
    assert repas_aliment_updated.repas_id == id_repas
    assert repas_aliment_updated.aliment_id == id_aliment
    assert repas_aliment_updated.calories_totales == repas_aliment_get.calories_totales

# Delete
def test_delete_repas_aliment(db_session, repas_aliments):
    id_repas = repas_aliments[-1].repas_id
    id_aliment = repas_aliments[-1].aliment_id
    repas_aliment_get = get_repas_aliment(
        db=db_session,
        repas_id=repas_aliments[-1].repas_id,
        aliment_id=repas_aliments[-1].aliment_id
    )
    assert delete_repas_aliment(db=db_session, repas_id=id_repas, aliment_id=id_aliment)
    repas_aliment_get = get_repas_aliment(
        db=db_session,
        repas_id=id_repas,
        aliment_id=id_aliment
    )
    assert repas_aliment_get == None

# CRUD test Activite physique
# Create
def test_create_activite_physique(db_session, utilisateurs):
    activite_physique = ActivitePhysiqueCreate(
        date=datetime.date(2024,9,8),
        heure=datetime.time(1,0,0),
        duree=datetime.timedelta(seconds=3600),
        type_activite="Course à pied",
    )
    db_activite = create_activite_physique(
        db=db_session,
        activite=activite_physique,
        utilisateur_id=utilisateurs[-1].id
    )
    assert db_activite != None
    assert db_activite.utilisateur_id == utilisateurs[-1].id
    assert db_activite.date == activite_physique.date
    assert db_activite.duree == activite_physique.duree.total_seconds()
    assert db_activite.type_activite == activite_physique.type_activite

def test_get_activite_physique(db_session, utilisateurs, activites):
    id_user = utilisateurs[-1].id
    activite_physique_get = get_activite_physique(
        db=db_session,
        utilisateur_id=id_user,
        id=activites[-1].id
    )
    assert activite_physique_get != None
    assert len(activite_physique_get) == 1
    assert activite_physique_get[0].utilisateur_id == id_user
    assert activite_physique_get[0].date == activites[-1].date
    assert activite_physique_get[0].duree == activites[-1].duree
    assert activite_physique_get[0].type_activite == activites[-1].type_activite

def test_update_activite_physique(db_session, utilisateurs, activites):
    id_user = utilisateurs[-1].id
    id_activite = activites[-1].id
    activite = ActivitePhysiqueCreate(
        utilissateur_id=id_user,
        date=datetime.date(2024,9,10),
        heure=datetime.time(10,0,0),
        duree=datetime.timedelta(days=3600),
        type_activite="Course à pied",
    )
    activite_physique_updated = update_activite_physique(
        db=db_session,
        activite=activite,
        id=id_activite
    )
    assert activite_physique_updated.type_activite == activite.type_activite
    assert activite_physique_updated.utilisateur_id == id_user
    assert activite_physique_updated.date == datetime.date(2024,9,10)
    assert activite_physique_updated.heure == datetime.time(10,0,0)
    assert activite_physique_updated.duree == datetime.timedelta(days=3600).total_seconds()

def test_delete_activite_physique(db_session, utilisateurs, activites):
    id_activite = activites[-1].id
    id_utilisateur = activites[-1].utilisateur_id
    assert delete_activite_physique(db=db_session, id=id_activite)
    activite_physique_get = get_activite_physique(
        db=db_session,
        utilisateur_id=id_utilisateur,
        id=id_activite
    )
    assert activite_physique_get == None

def test_create_poids(db_session, utilisateurs):
    poids = PoidsCreate(
        date=datetime.date(2024,9,8),
        poids=70.0,
        utilisateur_id=utilisateurs[-1].id
    )
    db_poids = create_poids(
        db=db_session,
        poids=poids
    )
    assert db_poids != None
    assert db_poids.utilisateur_id == utilisateurs[-1].id
    assert db_poids.date == poids.date
    assert db_poids.poids == poids.poids

def test_get_poids(db_session, utilisateurs, poids):
    poids_get = get_poids(
        db=db_session,
        utilisateur_id=utilisateurs[-1].id,
        id=poids[-1].id
    )
    assert poids_get != None
    assert len(poids_get) == 1
    assert poids_get[0].utilisateur_id == utilisateurs[-1].id
    assert poids_get[0].date == poids[-1].date
    assert poids_get[0].poids == poids[-1].poids

    poids_get = get_poids(
        db=db_session,
        utilisateur_id=utilisateurs[-1].id
    )
    assert poids_get != None
    assert len(poids_get) >= 1
    for poids_get_item in poids_get:
        assert poids_get_item.utilisateur_id == utilisateurs[-1].id

def test_update_poids(db_session, poids):
    poids_update = PoidsCreate(
        date=datetime.date(2024,9,8),
        poids=70.0,
        utilisateur_id=poids[-1].utilisateur_id
    )
    poids_updated = update_poids(
        db=db_session,
        id=poids[-1].id,
        poids=poids_update
    )
    
    assert poids_updated != None
    assert poids_updated.id == poids[-1].id
    assert poids_updated.poids == poids_update.poids
    assert poids_updated.date == poids_update.date
    assert poids_updated.utilisateur_id == poids_update.utilisateur_id

def test_delete_poids(db_session, poids):
    assert delete_poids(db=db_session, id=poids[-1].id)
    poids_get = get_poids(
        db=db_session,
        utilisateur_id=poids[-1].utilisateur_id,
        id=poids[-1].id
    )
    assert poids_get == None
