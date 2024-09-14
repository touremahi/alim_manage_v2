import datetime
from fastapi.testclient import TestClient
from app.main import app  # Assurez-vous que 'app' est l'instance FastAPI de votre application

client = TestClient(app)

# test create utilisateur
def test_create_utilisateur(client):
    utilisateur_data = {
        "nom": "Mahinema",
        "email" : "test@example.com",
        "mot_de_passe": "password123",
        "age" : 22,
        "poids_initial" : 71.2
    }
    response = client.post("/api/utilisateurs", json=utilisateur_data)
    assert response.status_code == 200
    assert response.json()["nom"] == "Mahinema"
    assert response.json()["email"] == "test@example.com"
    assert response.json()["age"] == 22
    assert response.json()["poids_initial"] == 71.2
    assert response.json()["id"] is not None

# get list utilisateurs
def test_get_utilisateurs(client, utilisateurs):
    response = client.get("/api/utilisateurs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == len(utilisateurs)

# get utilisateur
def test_get_utilisateur(client, utilisateurs):
    utilisateur_get = utilisateurs[0]
    response = client.get(f"/api/utilisateurs/{utilisateur_get.id}")
    assert response.status_code == 200
    assert response.json()["nom"] == utilisateur_get.nom
    assert response.json()["email"] == utilisateur_get.email
    assert response.json()["age"] == utilisateur_get.age
    assert response.json()["poids_initial"] == utilisateur_get.poids_initial
    assert response.json()["id"] == utilisateur_get.id

# Update
def test_update_utilisateur(client, utilisateurs):
    utilisateur_update = utilisateurs[-1]
    utilisateur_data = {
        "id" : utilisateur_update.id,
        "nom": "Mahinema2",
        "email" : "test2@example.com", # TODO email à gerer
        "age" : 23,
        "poids_initial" : 75
    }
    response = client.put(f"/api/utilisateurs/{utilisateur_update.id}", json=utilisateur_data)
    assert response.status_code == 200
    assert response.json()["nom"] == "Mahinema2"
    assert response.json()["age"] == 23
    assert response.json()["poids_initial"] == 75
    assert response.json()["id"] == utilisateur_update.id

# Delete
def test_delete_utilisateur(client, utilisateurs):
    utilisateur_delete = utilisateurs[-1]
    response = client.delete(f"/api/utilisateurs/{utilisateur_delete.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Utilisateur supprimé avec succès."

# Update password
def test_update_utilisateur_password(client, utilisateurs):
    pass

# CRUD test aliment
# Create
def test_create_aliment(client):
    aliment = {
        "nom": "Poulet",
        "categorie": "Viandes",
        "calories": 2.39,
        "unite" : "g"
    }
    response = client.post("/api/aliments", json=aliment)
    assert response.status_code == 200
    assert response.json()["nom"] == "Poulet"
    assert response.json()["categorie"] == "Viandes"
    assert response.json()["calories"] == 2.39
    assert response.json()["unite"] == "g"
    assert response.json()["id"] is not None

# Get list aliments
def test_get_aliments(client, aliments):
    response = client.get("/api/aliments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == len(aliments)

def test_get_aliment(client, aliments):
    aliment_get = aliments[0]
    
    response = client.get(f"/api/aliments/{aliment_get.id}")
    assert response.status_code == 200
    assert response.json()["nom"] == aliment_get.nom
    assert response.json()["categorie"] == aliment_get.categorie
    assert response.json()["calories"] == aliment_get.calories
    assert response.json()["unite"] == aliment_get.unite
    assert response.json()["id"] == aliment_get.id

def test_get_aliments_by_categorie(client, aliments):
    aliments_categorie = aliments[0].categorie
    response = client.get(f"/api/aliments/categorie/{aliments_categorie}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for aliment in response.json():
        assert aliment["categorie"] == aliments_categorie

# update 
def test_update_aliment(client, aliments):
    aliment_update = aliments[-1]
    aliment_data = {
        "id" : aliment_update.id,
        "nom": "Pourrit",
        "categorie": "Viandes",
        "calories": 2.39,
        "unite" : "g"
    }
    response = client.put(f"/api/aliments/{aliment_update.id}", json=aliment_data)
    assert response.status_code == 200
    assert response.json()["nom"] == "Pourrit"
    assert response.json()["categorie"] == "Viandes"
    assert response.json()["calories"] == 2.39
    assert response.json()["unite"] == "g"
    assert response.json()["id"] == aliment_update.id

# delete
def test_delete_aliment(client, aliments):
    aliment_delete = aliments[-1]
    response = client.delete(f"/api/aliments/{aliment_delete.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Aliment supprimé avec succès."

# CRUD test repas
# Create
def test_create_repas(client, utilisateurs):
    repas = {
        "type_repas": "Diner",
        "date": "2024-09-10",
        "heure" : "19:00",
        "utilisateur_id" : utilisateurs[0].id
    }
    response = client.post("/api/repas", json=repas)
    assert response.status_code == 200
    assert response.json()["type_repas"] == "Diner"
    assert response.json()["date"] == "2024-09-10"
    assert response.json()["heure"] == "19:00:00"
    assert response.json()["id"] is not None

# get repas by id
def test_get_repas_by_id(client, repas, repas_aliments):
    
    response = client.get(f"/api/repas/{repas[0].id}")
    assert response.status_code == 200
    assert response.json()["type_repas"] == repas[0].type_repas
    assert response.json()["date"] == repas[0].date.strftime("%Y-%m-%d")
    assert response.json()["heure"] == repas[0].heure.strftime("%H:%M:%S")
    assert response.json()["id"] == repas[0].id

# get repas by date
def test_get_repas_by_date(client, repas):
    repas_date = repas[0].date.strftime("%Y-%m-%d")
    response = client.get(
        f"/api/repas/user_{repas[0].utilisateur_id}/d_{repas_date}"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for repas in response.json():
        assert repas["date"] == repas_date

# get repas by type_repas
def test_get_repas_by_type(client, repas):
    type_repas = repas[0].type_repas
    user_repas = repas[0].utilisateur_id
    response = client.get(
        f"/api/repas/user_{user_repas}/t_{type_repas}"
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for repas in response.json():
        assert repas["type_repas"] == type_repas

# test update repas
def test_update_repas(client, repas):
    repas_data = {
        "type_repas": "Diner",
        "date": "2024-09-10",
        "heure" : "19:00",
        "utilisateur_id" : repas[-1].utilisateur_id
    }
    response = client.put(
        f"/api/repas/{repas[-1].id}", 
        json=repas_data
    )
    assert response.status_code == 200
    assert response.json()["type_repas"] == "Diner"
    assert response.json()["date"] == "2024-09-10"
    assert response.json()["heure"] == "19:00:00"
    assert response.json()["id"] == repas[-1].id

# delete repas
def test_delete_repas(client, repas):
    response = client.delete(f"/api/repas/{repas[-1].id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Repas supprimé avec succès."

# add aliment to repas (repas_aliment)
def test_add_aliment_to_repas(client, repas, aliments):
    id_repas = repas[-1].id
    id_aliment = aliments[-1].id
    calorie_aliment = aliments[-1].calories
    repas_aliment = {
        "repas_id" : id_repas,
        "aliment_id" : id_aliment,
        "quantite" : 100,
        "calories_totales" : 100 * calorie_aliment
    }
    response = client.post(
        f"/api/repas_{repas[-1].id}/aliment_{aliments[-1].id}",
        json=repas_aliment
    )
    assert response.status_code == 200
    assert response.json()["repas_id"] == id_repas
    assert response.json()["aliment_id"] == id_aliment
    assert response.json()["quantite"] == 100
    assert response.json()["calories_totales"] == 100 * calorie_aliment

def test_get_repas_aliment(client, repas_aliments):
    id_repas = repas_aliments[-1].repas_id
    id_aliment = repas_aliments[-1].aliment_id
    calories_totales = repas_aliments[-1].calories_totales
    response = client.get(
        f"/api/repas_{id_repas}/aliment_{id_aliment}"
    )
    assert response.status_code == 200
    assert response.json()["repas_id"] == id_repas
    assert response.json()["aliment_id"] == id_aliment
    assert response.json()["quantite"] == 100
    assert response.json()["calories_totales"] == calories_totales

# update repas_aliment
def test_update_repas_aliment(client, repas_aliments):
    id_repas = repas_aliments[-1].repas_id
    id_aliment = repas_aliments[-1].aliment_id
    calories_totales = repas_aliments[-1].calories_totales
    quantite = repas_aliments[-1].calories_totales
    calorie = calories_totales / quantite
    repas_aliment = {
        "repas_id" : id_repas,
        "aliment_id" : id_aliment,
        "quantite" : 100,
        "calories_totales" : 100 * calorie
    }
    response = client.put(
        f"/api/repas/aliment/update",
        json=repas_aliment
    )
    assert response.status_code == 200
    assert response.json()["repas_id"] == id_repas
    assert response.json()["aliment_id"] == id_aliment
    assert response.json()["quantite"] == 100
    assert response.json()["calories_totales"] == 100 * calorie

# delete repas_aliment
def test_delete_repas_aliment(client, repas_aliments):
    id_repas = repas_aliments[-1].repas_id
    id_aliment = repas_aliments[-1].aliment_id
    response = client.delete(
        f"/api/repas/aliment/delete/{id_repas}_{id_aliment}"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Aliment supprimé avec succès du repas."

# CRUD activite physique
# Create
def test_create_activite_physique(client, utilisateurs):
    id_utilisateur = utilisateurs[-1].id
    activite = {
        "type_activite": "Course à pied",
        "date" : "2024-09-10",
        "heure" :"19:00",
        "duree" : datetime.timedelta(minutes=60).total_seconds()
    }
    response = client.post(
        f"/api/activite/user_{id_utilisateur}",
        json=activite
    )

    assert response.status_code == 200
    assert response.json()["type_activite"] == "Course à pied"
    assert response.json()["date"] == "2024-09-10"
    assert response.json()["heure"] == "19:00:00"
    assert response.json()["duree"] == datetime.timedelta(minutes=60).total_seconds()
    assert response.json()["utilisateur_id"] == id_utilisateur

# get activite physique
def test_get_activite_physique(client, activites):
    id_activite = activites[-1].id
    id_user = activites[-1].utilisateur_id
    response = client.get(f"/api/activite/user_{id_user}/{id_activite}")
    assert response.status_code == 200
    activite = response.json()
    assert activite["utilisateur_id"] == id_user
    assert activite["type_activite"] is not None
    assert activite["date"] is not None
    assert activite["heure"] is not None
    assert activite["duree"] is not None

# get liste activite physique
def test_get_liste_activite_physique(client, activites):
    id_user = activites[-1].utilisateur_id
    response = client.get(f"/api/activite/user_{id_user}")
    assert response.status_code == 200
    for activite in response.json():
        assert activite["utilisateur_id"] == id_user
        assert activite["type_activite"] is not None
        assert activite["date"] is not None
        assert activite["heure"] is not None
        assert activite["duree"] is not None

# update activite physique
def test_update_activite_physique(client, activites):
    id_activite = activites[-1].id
    id_user = activites[-1].utilisateur_id
    activite = {
        "utilissateur_id": id_user,
        "date" : "2024-05-23",
        "heure" : "10:00",
        "duree" : datetime.timedelta(minutes = 60).total_seconds(),
        "type_activite" :"Course à pied",
    }
    response = client.put(
        f"/api/activite/update/{id_activite}",
        json=activite
    )
    assert response.status_code == 200
    assert response.json()["type_activite"] == "Course à pied"
    assert response.json()["date"] == "2024-05-23"
    assert response.json()["heure"] == "10:00:00"
    assert response.json()["duree"] == datetime.timedelta(minutes = 60).total_seconds()
    assert response.json()["utilisateur_id"] == id_user

# delete activite physique
def test_delete_activite_physique(client, activites):
    id_activite = activites[-1].id
    response = client.delete(
        f"/api/activite/delete/{id_activite}"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Activité supprimée avec succès."

# CRUD Poids
# Create
def test_create_poids(client, utilisateurs):
    id_utilisateur = utilisateurs[-1].id
    poids = {
        "date" : "2024-05-23",
        "poids" : 75,
        "utilisateur_id" : id_utilisateur
    }
    response = client.post(
        f"/api/poids",
        json=poids
    )
    assert response.status_code == 200
    assert response.json()["date"] == "2024-05-23"
    assert response.json()["poids"] == 75
    assert response.json()["utilisateur_id"] == id_utilisateur

# Read liste
def test_get_liste_poids(client, poids):
    id_utilisateur = poids[-1].utilisateur_id
    response = client.get(f"/api/poids/user_{id_utilisateur}")
    assert response.status_code == 200
    for poids_get in response.json():
        assert poids_get["utilisateur_id"] == id_utilisateur
        assert poids_get["date"] is not None
        assert poids_get["poids"] is not None

# update poids
def test_update_poids(client, poids):
    id_poids = poids[-1].id
    id_utilisateur = poids[-1].utilisateur_id
    poids = {
        "date" : "2024-05-23",
        "poids" : 75,
        "utilisateur_id" : id_utilisateur
    }
    response = client.put(
        f"/api/poids/update/{id_poids}",
        json=poids
    )
    assert response.status_code == 200
    assert response.json()["date"] == "2024-05-23"
    assert response.json()["poids"] == 75
    assert response.json()["utilisateur_id"] == id_utilisateur
    assert response.json()["id"] == id_poids

# delete poids
def test_delete_poids(client, poids):
    id_poids = poids[-1].id
    response = client.delete(
        f"/api/poids/delete/{id_poids}"
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Poids supprimé avec succès."