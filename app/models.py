from sqlalchemy import Column, Integer, String, Float, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Utilisateur(Base):
    __tablename__ = 'utilisateurs'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    email = Column(String)#, unique=True, index=True, nullable=False)
    mot_de_passe = Column(String)
    age = Column(Integer)
    poids_initial = Column(Float)

class Repas(Base):
    __tablename__ ='repas'

    id = Column(Integer, primary_key=True, index=True)
    type_repas = Column(String(100))
    date = Column(Date)
    heure = Column(Time)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))

    aliments = relationship("RepasAliment", back_populates="repas")

class Aliment(Base):
    __tablename__ = 'aliments'

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100))
    calories = Column(Float)
    unite = Column(String(100))
    categorie = Column(String(100))

    repas = relationship("RepasAliment", back_populates="aliment")

class RepasAliment(Base):
    __tablename__ ='repas_aliments'

    id = Column(Integer, primary_key=True, index=True)
    repas_id = Column(Integer, ForeignKey('repas.id'))
    aliment_id = Column(Integer, ForeignKey('aliments.id'))
    quantite = Column(Float)
    calories_totales = Column(Float)

    repas = relationship("Repas", back_populates="aliments")
    aliment = relationship("Aliment", back_populates="repas")

class ActivitePhysique(Base):
    __tablename__ = 'activites_physiques'

    id = Column(Integer, primary_key=True, index=True)
    type_activite = Column(String(100))
    date = Column(Date)
    heure = Column(Time)
    duree = Column(Float)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))

class Poids(Base):
    __tablename__ = 'poids'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    poids = Column(Float)
    utilisateur_id = Column(Integer, ForeignKey('utilisateurs.id'))
