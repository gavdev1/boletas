from typing import List
from fastapi import APIRouter, Depends, HTTPException

from domain.schemas.seccion import SeccionCreate, SeccionUpdate, SeccionResponse
from domain.services.seccion import SeccionService
from api.deps import get_seccion_service

router = APIRouter()


@router.post("/", response_model=SeccionResponse, status_code=201)
def create_seccion(
    seccion_in: SeccionCreate,
    service: SeccionService = Depends(get_seccion_service),
) -> SeccionResponse:
    return service.crear_seccion(seccion_in)


@router.get("/", response_model=List[SeccionResponse])
def read_secciones(
    skip: int = 0,
    limit: int = 100,
    service: SeccionService = Depends(get_seccion_service),
) -> List[SeccionResponse]:
    return service.listar_secciones(skip=skip, limit=limit)


@router.get("/{seccion_id}", response_model=SeccionResponse)
def read_seccion(
    seccion_id: int,
    service: SeccionService = Depends(get_seccion_service),
) -> SeccionResponse:
    seccion = service.obtener_seccion(seccion_id)
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return seccion


@router.put("/{seccion_id}", response_model=SeccionResponse)
def update_seccion(
    seccion_id: int,
    seccion_in: SeccionUpdate,
    service: SeccionService = Depends(get_seccion_service),
) -> SeccionResponse:
    seccion = service.actualizar_seccion(seccion_id, seccion_in)
    if not seccion:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
    return seccion


@router.delete("/{seccion_id}", status_code=204)
def delete_seccion(
    seccion_id: int,
    service: SeccionService = Depends(get_seccion_service),
):
    success = service.eliminar_seccion(seccion_id)
    if not success:
        raise HTTPException(status_code=404, detail="Sección no encontrada")
