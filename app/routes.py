import datetime
from typing import List


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .schemas import (
    UtilisateurCreate, UtilisateurOut,
    AlimentCreate, AlimentOut,
    RepasAlimentOut, RepasCreate, RepasAlimentCreate,
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

# Read repas par id
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
    
# TODO: Read repas par utilisateur
@router.get("/repas/user_{utilisateur_id}")#, response_model=ListeRepasOut)
def route_get_repas_by_utilisateur(
    utilisateur_id: int,
    db: Session = Depends(get_db)
):
    return {
        "message": "Route non implémentée"
    }

# Repas par date
@router.get("/repas/user_{utilisateur_id}/d_{date}", response_model=List[ListeRepasOut])
def route_get_repas_by_date(
    date: str,
    utilisateur_id: int,
    db: Session = Depends(get_db)
):
    try:
        date_t = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        repas_date = get_repas_by_date(db=db, utilisateur_id=utilisateur_id, date=date_t)
        if repas_date:
            return repas_date
        message = f"Aucun repas trouvé pour la date {date}."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    except Exception as e:
        message = f"Impossible de récupérer les repas.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Repas par type_repas
@router.get("/repas/user_{utilisateur_id}/t_{type_repas}", response_model=List[ListeRepasOut])
def route_get_repas_by_type(
    type_repas: str,
    utilisateur_id: int,
    db: Session = Depends(get_db)
):
    try:
        repas_type = get_repas_by_type(db=db, utilisateur_id=utilisateur_id, type_repas=type_repas)
        if repas_type:
            return repas_type
        message = f"Aucun repas trouvé pour le type {type_repas}."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    except Exception as e:
        message = f"Impossible de récupérer les repas.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Update par id
@router.put("/repas/{id}", response_model=RepasOut)
def route_update_repas(
    id: int,
    repas: RepasCreate,
    db: Session = Depends(get_db)
):
    try:
        return update_repas(db=db, id=id, repas=repas)
    except Exception as e:
        message = f"Impossible de mettre à jour le repas.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# delete repas
@router.delete("/repas/{id}")
def route_delete_repas(
    id: int,
    db: Session = Depends(get_db)
):
    if delete_repas(db=db, id=id):
        message = f"Repas supprimé avec succès."
        return {"message": message}
    message = f"Impossible de supprimer le repas."
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# add aliment to repas (repas_aliment)
@router.post("/repas_{id}/aliment_{aliment_id}", response_model=RepasAlimentCreate)
def route_add_aliment_to_repas(
    id: int,
    r_aliment: RepasAlimentCreate,
    db: Session = Depends(get_db)
):
    try:
        return add_aliment_to_repas(
            db=db,
            repas_id=r_aliment.repas_id,
            aliment_id=r_aliment.aliment_id,
            quantite=r_aliment.quantite
        )
    except Exception as e:
        message = f"Impossible d'ajouter l'aliment au repas.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

@router.get("/repas_{repas_id}/aliment_{aliment_id}", response_model=RepasAlimentCreate)
def route_get_repas_aliment(
    repas_id:int,
    aliment_id: int,
    db: Session = Depends(get_db)
):
    try:
        return get_repas_aliment(db=db, repas_id=repas_id, aliment_id=aliment_id)
    except Exception as e:
        message = f"Impossible de récupérer les repas.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# update repas_aliment
@router.put("/repas/aliment/update", response_model=RepasAlimentCreate)
def route_update_repas_aliment(
    r_aliment: RepasAlimentCreate,
    db: Session = Depends(get_db)
):
    try:
        return update_repas_aliment(
            db=db,
            repas_aliment=r_aliment
        )
    except Exception as e:
        message = f"Impossible de mettre à jour le repas.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# delete repas_aliment
@router.delete("/repas/aliment/delete/{repas_id}_{aliment_id}")
def route_delete_repas_aliment(
    repas_id: int,
    aliment_id: int,
    db: Session = Depends(get_db)
):
    if delete_repas_aliment(db=db, repas_id=repas_id, aliment_id=aliment_id):
        message = f"Aliment supprimé avec succès du repas."
        return {"message": message}
    message = f"Impossible de supprimer le repas."
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# CRUD Activite physique
# Create
@router.post("/activite/user_{user_id}", response_model=ActivitePhysiqueOut)
def route_create_activite_physique(
    activite: ActivitePhysiqueCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        utilisateur = get_utilisateur(db=db, id=user_id)
        if not utilisateur:
            message = f"L'utilisateur n'existe pas."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        db_activite = create_activite_physique(
            db=db,
            activite=activite,
            utilisateur_id=user_id
        )
        return ActivitePhysiqueOut(
            id=db_activite.id,
            type_activite=db_activite.type_activite,
            date=db_activite.date,
            heure=db_activite.heure,
            duree=db_activite.duree,
            utilisateur_id=db_activite.utilisateur_id
        )
    except Exception as e:
        message = f"Impossible de créer l'activité physique.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
   
# Read activite TODO 
@router.get("/activite/user_{user_id}/{id}", response_model=ActivitePhysiqueOut)
def route_get_activite_physique(
    id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        if not get_utilisateur(db=db, id=user_id):
            message = f"L'utilisateur n'existe pas."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        activites = get_activite_physique(db=db, utilisateur_id=user_id, id=id)
        if activites:
            return activites[0]
    except Exception as e:
        message = f"Impossible de récupérer l'activité physique.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Read liste
@router.get("/activite/user_{user_id}", response_model=List[ActivitePhysiqueOut])
def route_get_liste_activite_physique(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        if not get_utilisateur(db=db, id=user_id):
            message = f"L'utilisateur n'existe pas."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        activites = get_activite_physique(db=db, utilisateur_id=user_id)
        if activites:
            return activites
        message = f"Aucune activité physique trouvée pour cet utilisateur."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    except Exception as e:
        message = f"Impossible de récupérer les activités physiques.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Update par id
@router.put("/activite/update/{id}", response_model=ActivitePhysiqueOut)
def route_update_activite_physique(
    id: int,
    activite: ActivitePhysiqueCreate,
    db: Session = Depends(get_db)
):
    try:
        activite_physique = update_activite_physique(
            db=db,
            activite=activite,
            id=id
        )
        return ActivitePhysiqueOut(
            id=activite_physique.id,
            type_activite=activite_physique.type_activite,
            date=activite_physique.date,
            heure=activite_physique.heure,
            duree=activite_physique.duree,
            utilisateur_id=activite_physique.utilisateur_id
        )
    except Exception as e:
        message = f"Impossible de mettre à jour l'activité physique.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# delete activite
@router.delete("/activite/delete/{id}")
def route_delete_activite_physique(
    id: int,
    db: Session = Depends(get_db)
):
    if delete_activite_physique(db=db, id=id):
        message = f"Activité supprimée avec succès."
        return {"message": message}
    message = f"Impossible de supprimer l'activité physique."
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# CRUD Poids
# Create
@router.post("/poids", response_model=PoidsOut)
def route_create_poids(
    poids: PoidsCreate,
    db: Session = Depends(get_db)
):
    try:
        if not get_utilisateur(db=db, id=poids.utilisateur_id):
            message = f"L'utilisateur n'existe pas."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        db_poids = create_poids(
            db=db,
            poids=poids
        )
        return PoidsOut(
            id=db_poids.id,
            poids=db_poids.poids,
            date=db_poids.date,
            utilisateur_id=db_poids.utilisateur_id
        )
    except Exception as e:
        message = f"Impossible de créer le poids.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# Read poids
@router.get("/poids/user_{user_id}", response_model=List[PoidsOut])
def route_get_liste_poids(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        if not get_utilisateur(db=db, id=user_id):
            message = f"L'utilisateur n'existe pas."
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
        poids = get_poids(db=db, utilisateur_id=user_id)
        if poids:
            return poids
        message = f"Aucun poids trouvé pour cet utilisateur."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    except Exception as e:
        message = f"Impossible de récupérer les poids.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# update poids
@router.put("/poids/update/{id}", response_model=PoidsOut)
def route_update_poids(
    id: int,
    poids: PoidsCreate,
    db: Session = Depends(get_db)
):
    try:
        poids_db = update_poids(
            db=db,
            poids=poids,
            id=id
        )
        if poids_db:
            return poids_db
        message = f"Impossible de mettre à jour le poids."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    except Exception as e:
        message = f"Impossible de mettre à jour le poids.\n{str(e)}"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

# delete poids
@router.delete("/poids/delete/{id}")
def route_delete_poids(
    id: int,
    db: Session = Depends(get_db)
):
    if delete_poids(db=db, id=id):
        message = f"Poids supprimé avec succès."
        return {"message": message}
    message = f"Impossible de supprimer le poids."
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)