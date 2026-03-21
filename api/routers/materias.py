from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from domain.schemas.materia import MateriaCreate, MateriaUpdate, MateriaResponse
from domain.services.materia import MateriaService
from api.deps import get_materia_service

router = APIRouter()


@router.post("/", response_model=MateriaResponse, status_code=201)
def create_materia(
    materia_in: MateriaCreate,
    service: MateriaService = Depends(get_materia_service),
) -> MateriaResponse:
    return service.crear_materia(materia_in)


@router.get("/", response_model=List[MateriaResponse])
def read_materias(
    grado: int | None = Query(None, description="Filtrar por grado"),
    modalidad: str | None = Query(None, description="Filtrar por modalidad"),
    skip: int = 0,
    limit: int = 100,
    service: MateriaService = Depends(get_materia_service),
) -> List[MateriaResponse]:
    return service.listar_materias(skip=skip, limit=limit, grado=grado, modalidad=modalidad)


@router.get("/{materia_id}", response_model=MateriaResponse)
def read_materia(
    materia_id: int,
    service: MateriaService = Depends(get_materia_service),
) -> MateriaResponse:
    materia = service.obtener_materia(materia_id)
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia


@router.put("/{materia_id}", response_model=MateriaResponse)
def update_materia(
    materia_id: int,
    materia_in: MateriaUpdate,
    service: MateriaService = Depends(get_materia_service),
) -> MateriaResponse:
    materia = service.actualizar_materia(materia_id, materia_in)
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia


@router.delete("/{materia_id}", status_code=204)
def delete_materia(
    materia_id: int,
    service: MateriaService = Depends(get_materia_service),
):
    success = service.eliminar_materia(materia_id)
    if not success:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
