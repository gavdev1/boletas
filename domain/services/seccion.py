from typing import List, Optional
from domain.schemas.seccion import SeccionCreate, SeccionUpdate, SeccionResponse
from persistencia.repositories.seccion import SeccionRepository
from fastapi import HTTPException


class SeccionService:
    def __init__(self, repository: SeccionRepository):
        self.repository = repository

    def contar_secciones(self) -> int:
        return self.repository.count()

    def crear_seccion(self, seccion_in: SeccionCreate) -> SeccionResponse:
        db_seccion = self.repository.get_by_unique_fields(seccion_in.grado, seccion_in.letra, seccion_in.modalidad)
        if db_seccion:
            raise HTTPException(status_code=400, detail="Esta sección ya existe en esta modalidad")
            
        db_seccion = self.repository.create(seccion_in)
        return SeccionResponse.model_validate(db_seccion)

    def obtener_seccion(self, seccion_id: int) -> Optional[SeccionResponse]:
        db_seccion = self.repository.get_by_id(seccion_id)
        if db_seccion:
            return SeccionResponse.model_validate(db_seccion)
        return None

    def verificar_existencia_seccion(self, grado: int, letra: str, modalidad: str) -> bool:
        db_seccion = self.repository.get_by_unique_fields(grado, letra, modalidad)
        return db_seccion is not None

    def listar_secciones(self, skip: int = 0, limit: int = 100) -> List[SeccionResponse]:
        db_secciones = self.repository.get_all(skip=skip, limit=limit)
        return [SeccionResponse.model_validate(s) for s in db_secciones]

    def actualizar_seccion(self, seccion_id: int, seccion_in: SeccionUpdate) -> Optional[SeccionResponse]:
        db_seccion = self.repository.update(seccion_id, seccion_in)
        if db_seccion:
            return SeccionResponse.model_validate(db_seccion)
        return None

    def eliminar_seccion(self, seccion_id: int) -> bool:
        return self.repository.delete(seccion_id)
