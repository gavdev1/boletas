from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import SessionLocal

from persistencia.repositories.nota import NotaRepository
from persistencia.repositories.alumno import AlumnoRepository
from persistencia.repositories.materia import MateriaRepository
from persistencia.repositories.boleta import BoletaRepository

from domain.services.nota import NotaService
from domain.services.alumno import AlumnoService
from domain.services.materia import MateriaService
from domain.services.boleta import BoletaService
from domain.services.pdf import PDFService


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- PDF Service ---
def get_pdf_service() -> PDFService:
    return PDFService()


# --- Notas ---
def get_nota_repository(db: Session = Depends(get_db)) -> NotaRepository:
    return NotaRepository(db)

def get_nota_service(repository: NotaRepository = Depends(get_nota_repository)) -> NotaService:
    return NotaService(repository)


# --- Alumnos ---
def get_alumno_repository(db: Session = Depends(get_db)) -> AlumnoRepository:
    return AlumnoRepository(db)

def get_alumno_service(repository: AlumnoRepository = Depends(get_alumno_repository)) -> AlumnoService:
    return AlumnoService(repository)


# --- Materias ---
def get_materia_repository(db: Session = Depends(get_db)) -> MateriaRepository:
    return MateriaRepository(db)

def get_materia_service(repository: MateriaRepository = Depends(get_materia_repository)) -> MateriaService:
    return MateriaService(repository)


# --- Boletas ---
def get_boleta_repository(db: Session = Depends(get_db)) -> BoletaRepository:
    return BoletaRepository(db)

def get_boleta_service(repository: BoletaRepository = Depends(get_boleta_repository)) -> BoletaService:
    return BoletaService(repository)
