from pydantic import BaseModel, ConfigDict
from datetime import date, time
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

class RepasAlimentOutOne(RepasAlimentBase):
    repas_id: int
    aliment: AlimentOut

    model_config = ConfigDict(from_attributes = True)

class RepasBase(BaseModel):
    type_repas: str
    date: date
    heure: time

class RepasCreate(RepasBase):
    utilisateur: UtilisateurOut

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
    duree: float

class ActivitePhysiqueCreate(ActivitePhysiqueBase):
    pass

class ActivitePhysiqueOut(ActivitePhysiqueBase):
    id: int
    utilisateur_id: int
    
    model_config = ConfigDict(from_attributes = True)

class PoidsBase(BaseModel):
    date: date
    poids: float

class PoidsOut(PoidsBase):
    id: int
    utilisateur_id: int
    
    model_config = ConfigDict(from_attributes = True)
