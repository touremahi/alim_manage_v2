from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .schemas import (
    UtilisateurCreate, UtilisateurOut,
    AlimentCreate, AlimentOut,
    RepasAlimentOut, RepasCreate, RepasAlimentOutOne,
    RepasOut, ListeRepasOut,
    ActivitePhysiqueCreate, ActivitePhysiqueOut,
    PoidsCreate, PoidsOut
)
from .database import get_db
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


router = APIRouter(
    prefix="/api",
    tags=["api"]
)

# utilisateur CRUD
# Create
@router.post("/utilisateurs", response_model=UtilisateurOut)
def route_create_utilisateur(
    utilisateur: UtilisateurCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_utilisateur(db=db, utilisateur=utilisateur)
    except Exception as e:
        message = f"Impossible d'ajouter l'utilisateur.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# CRUD utilisateur
# Create
@router.get("/utilisateurs", response_model=List[UtilisateurOut])
def route_get_utilisateurs(
    db: Session = Depends(get_db)
):
    try:
        return get_utilisateurs(db=db)
    except Exception as e:
        message = f"Impossible de récupérer les utilisateurs.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Read
@router.get("/utilisateurs/{id}", response_model=UtilisateurOut)
def route_get_utilisateur(
    id: int,
    db: Session = Depends(get_db)
):
    try:
        return get_utilisateur(db=db, id=id)
    except Exception as e:
        message = f"Impossible de récupérer l'utilisateur.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Update
@router.put("/utilisateurs/{id}", response_model=UtilisateurOut)
def route_update_utilisateur(
    id: int,
    utilisateur: UtilisateurOut,
    db: Session = Depends(get_db)
):
    try:
        return update_utilisateur(db=db, utilisateur=utilisateur)
    except Exception as e:
        message = f"Impossible de mettre à jour l'utilisateur.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# TODO: update password

# Delete
@router.delete("/utilisateurs/{id}")
def route_delete_utilisateur(
    id: int,
    db: Session = Depends(get_db)
):
    if delete_utilisateur(db=db, utilisateur_id=id):
        message = f"Utilisateur supprimé avec succès."
        return {"message": message}
    message = f"Impossible de supprimer l'utilisateur."
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# CRUD aliment
# Create
@router.post("/aliments", response_model=AlimentOut)
def route_create_aliment(
    aliment: AlimentCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_aliment(db=db, aliment=aliment)
    except Exception as e:
        message = f"Impossible d'ajouter l'aliment.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
# Read liste aliments
@router.get("/aliments", response_model=List[AlimentOut])
def route_get_aliments(
    db: Session = Depends(get_db)
):
    try:
        return get_aliments(db=db)
    except Exception as e:
        message = f"Impossible de récupérer les aliments.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Read aliment par id
@router.get("/aliments/{id}", response_model=AlimentOut)
def route_get_aliment(
    id: int,
    db: Session = Depends(get_db)
):
    try:
        aliment = get_aliment(db=db, id=id)
        if aliment:
            return aliment
        raise Exception("Aliment non trouvé")
    except Exception as e:
        message = f"Impossible de récupérer l'aliment.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Read aliments par categorie
@router.get("/aliments/categorie/{categorie}", response_model=List[AlimentOut])
def route_get_aliments_by_categorie(
    categorie: str,
    db: Session = Depends(get_db)
):
    try:
        return get_aliments_by_categorie(db=db, categorie=categorie)
    except Exception as e:
        message = f"Impossible de récupérer les aliments.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Update par id
@router.put("/aliments/{id}", response_model=AlimentOut)
def route_update_aliment(
    id: int,
    aliment: AlimentCreate,
    db: Session = Depends(get_db)
):
    try:
        return update_aliment(db=db, id=id, aliment=aliment)
    except Exception as e:
        message = f"Impossible de mettre à jour l'aliment.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Delete aliment par id
@router.delete("/aliments/{id}")
def route_delete_aliment(
    id: int,
    db: Session = Depends(get_db)
):
    if delete_aliment(db=db, id=id):
        message = f"Aliment supprimé avec succès."
        return {"message": message}
    message = f"Impossible de supprimer l'aliment."
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# CRUD repas
# Create
@router.post("/repas", response_model=RepasOut)
def route_create_repas(
    repas: RepasCreate,
    db: Session = Depends(get_db)
):
    try:
        repas_db = create_repas(db=db, repas=repas)
        return RepasOut(
            id=repas_db.id,
            type_repas=repas_db.type_repas,
            date=repas_db.date,
            heure=repas_db.heure,
            utilisateur_id=repas_db.utilisateur_id
        )
    except Exception as e:
        message = f"Impossible d'ajouter le repas.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

@router.get("/repas/{id}", response_model=ListeRepasOut)
def route_get_repas_by_id(
    id: int,
    db: Session = Depends(get_db)
):
    try:
        return get_repas_by_id(db=db, id=id)
    except Exception as e:
        message = f"Impossible de récupérer les repas.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)