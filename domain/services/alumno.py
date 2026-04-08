from typing import List, Optional
from domain.schemas.alumno import AlumnoCreate, AlumnoUpdate, AlumnoResponse
from persistencia.repositories.alumno import AlumnoRepository
from persistencia.repositories.seccion import SeccionRepository
from fastapi import HTTPException


class AlumnoService:
    def __init__(self, repository: AlumnoRepository, seccion_repo: SeccionRepository):
        self.repository = repository
        self.seccion_repo = seccion_repo

    def contar_alumnos(self) -> int:
        return self.repository.count()

    def obtener_stats(self) -> dict:
        return {
            "total": self.repository.count(),
            "presente": self.repository.count_by_status("presente"),
            "egresado": self.repository.count_by_status("egresado"),
            "retirado": self.repository.count_by_status("retirado"),
        }

    def crear_alumno(self, alumno_in: AlumnoCreate) -> AlumnoResponse:
        if alumno_in.grado is not None and alumno_in.seccion is not None:
            mod = getattr(alumno_in, "modalidad", "Media General")
            if not self.seccion_repo.get_by_unique_fields(alumno_in.grado, alumno_in.seccion, mod):
                raise HTTPException(status_code=400, detail="La sección especificada no ha sido creada para este grado y modalidad.")
                
        db_alumno = self.repository.create(alumno_in)
        return AlumnoResponse.model_validate(db_alumno)

    def obtener_alumno(self, alumno_id: int) -> Optional[AlumnoResponse]:
        db_alumno = self.repository.get_by_id(alumno_id)
        if db_alumno:
            return AlumnoResponse.model_validate(db_alumno)
        return None

    def obtener_alumno_por_cedula(self, cedula: str) -> Optional[AlumnoResponse]:
        db_alumno = self.repository.get_by_cedula(cedula)
        if db_alumno:
            return AlumnoResponse.model_validate(db_alumno)
        return None

    def listar_alumnos(self, skip: int = 0, limit: int = 100) -> List[AlumnoResponse]:
        db_alumnos = self.repository.get_all(skip=skip, limit=limit)
        return [AlumnoResponse.model_validate(a) for a in db_alumnos]

    def actualizar_alumno(self, alumno_id: int, alumno_in: AlumnoUpdate) -> Optional[AlumnoResponse]:
        db_alumno = self.repository.get_by_id(alumno_id)
        if not db_alumno:
            return None
            
        grado = alumno_in.grado if alumno_in.grado is not None else db_alumno.grado
        seccion = alumno_in.seccion if alumno_in.seccion is not None else db_alumno.seccion
        mod = getattr(alumno_in, "modalidad", None) or getattr(db_alumno, "modalidad", "Media General")
        
        if grado is not None and seccion is not None:
            if not self.seccion_repo.get_by_unique_fields(grado, seccion, mod):
                raise HTTPException(status_code=400, detail="La sección especificada no ha sido creada para este grado y modalidad.")
                
        db_alumno = self.repository.update(alumno_id, alumno_in)
        if db_alumno:
            return AlumnoResponse.model_validate(db_alumno)
        return None

    def eliminar_alumno(self, alumno_id: int) -> bool:
        return self.repository.delete(alumno_id)
