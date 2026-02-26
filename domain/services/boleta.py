from typing import List, Optional
from domain.schemas.boleta import BoletaCreate, BoletaUpdate, BoletaResponse, BoletaListResponse
from persistencia.repositories.boleta import BoletaRepository


class BoletaService:
    def __init__(self, repository: BoletaRepository):
        self.repository = repository

    def crear_boleta(self, boleta_in: BoletaCreate) -> BoletaResponse:
        db_boleta = self.repository.create(boleta_in)
        # Re-fetch con joins para incluir alumno y calificaciones.materia
        db_boleta = self.repository.get_by_id(db_boleta.id)
        return BoletaResponse.model_validate(db_boleta)

    def obtener_boleta(self, boleta_id: int) -> Optional[BoletaResponse]:
        db_boleta = self.repository.get_by_id(boleta_id)
        if db_boleta:
            return BoletaResponse.model_validate(db_boleta)
        return None

    def listar_boletas(
        self,
        skip: int = 0,
        limit: int = 100,
        alumno_id: Optional[int] = None,
        anio_escolar: Optional[str] = None,
        tipo_evaluacion: Optional[str] = None,
    ) -> List[BoletaListResponse]:
        db_boletas = self.repository.get_all(
            skip=skip,
            limit=limit,
            alumno_id=alumno_id,
            anio_escolar=anio_escolar,
            tipo_evaluacion=tipo_evaluacion,
        )
        return [BoletaListResponse.model_validate(b) for b in db_boletas]

    def actualizar_boleta(self, boleta_id: int, boleta_in: BoletaUpdate) -> Optional[BoletaResponse]:
        db_boleta = self.repository.update(boleta_id, boleta_in)
        if db_boleta:
            return BoletaResponse.model_validate(db_boleta)
        return None

    def eliminar_boleta(self, boleta_id: int) -> bool:
        return self.repository.delete(boleta_id)
