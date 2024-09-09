from pydantic import BaseModel, ConfigDict
from datetime import date, time, timedelta
from typing import List, Optional

class UtilisateurBase(BaseModel):
    nom: str
    email: str
    age: int
    poids_initial: float

class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str

class UtilisateurOut(UtilisateurBase):
    id: int

    model_config = ConfigDict(from_attributes = True)

class AlimentBase(BaseModel):
    nom: str
    calories: float
    unite: str
    categorie: str

class AlimentCreate(AlimentBase):
    pass

class AlimentOut(AlimentBase):
    id: int

    model_config = ConfigDict(from_attributes = True)

class RepasAlimentBase(BaseModel):
    quantite: float
    calories_totales: float

class RepasAlimentOut(RepasAlimentBase):
    # repas_id: int
    aliment: AlimentOut

    model_config = ConfigDict(from_attributes = True)

class RepasAlimentCreate(RepasAlimentBase):
    repas_id: int
    aliment_id: int

    model_config = ConfigDict(from_attributes = True)

class RepasBase(BaseModel):
    type_repas: str
    date: date
    heure: time

class RepasCreate(RepasBase):
    utilisateur_id: int

class RepasOut(RepasBase):
    id: int

    model_config = ConfigDict(from_attributes = True)

class ListeRepasOut(RepasBase):
    id: int
    aliments: List[RepasAlimentOut]
    
    model_config = ConfigDict(from_attributes = True)

class ActivitePhysiqueBase(BaseModel):
    type_activite: str
    date: date
    heure: time
    duree: timedelta

class ActivitePhysiqueCreate(ActivitePhysiqueBase):
    utilisateur_id: Optional[int] = None

class ActivitePhysiqueOut(ActivitePhysiqueBase):
    id: int
    utilisateur_id: int
    duree: float
    
    model_config = ConfigDict(from_attributes = True)

class PoidsBase(BaseModel):
    date: date
    poids: float

class PoidsCreate(PoidsBase):
    utilisateur_id: int

    model_config = ConfigDict(from_attributes = True)

class PoidsOut(PoidsBase):
    id: int
    utilisateur_id: int

    model_config = ConfigDict(from_attributes = True)
