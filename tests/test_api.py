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
        "email" : "test2@example.com",
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

def test_get_repas(client, repas, repas_aliments):
    
    response = client.get(f"/api/repas/{repas[0].id}")
    assert response.status_code == 200
    assert response.json()["type_repas"] == repas[0].type_repas
    assert response.json()["date"] == repas[0].date.stringify_dialect
    assert response.json()["heure"] == repas[0].heure.stringify_dialect
    assert response.json()["id"] == repas[0].id