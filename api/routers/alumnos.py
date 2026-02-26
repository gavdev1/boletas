from typing import List
from fastapi import APIRouter, Depends, HTTPException

from domain.schemas.alumno import AlumnoCreate, AlumnoUpdate, AlumnoResponse
from domain.services.alumno import AlumnoService
from api.deps import get_alumno_service

router = APIRouter()


@router.post("/", response_model=AlumnoResponse, status_code=201)
def create_alumno(
    alumno_in: AlumnoCreate,
    service: AlumnoService = Depends(get_alumno_service),
) -> AlumnoResponse:
    return service.crear_alumno(alumno_in)


@router.get("/", response_model=List[AlumnoResponse])
def read_alumnos(
    skip: int = 0,
    limit: int = 100,
    service: AlumnoService = Depends(get_alumno_service),
) -> List[AlumnoResponse]:
    return service.listar_alumnos(skip=skip, limit=limit)


@router.get("/{alumno_id}", response_model=AlumnoResponse)
def read_alumno(
    alumno_id: int,
    service: AlumnoService = Depends(get_alumno_service),
) -> AlumnoResponse:
    alumno = service.obtener_alumno(alumno_id)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno


@router.get("/cedula/{cedula}", response_model=AlumnoResponse)
def read_alumno_by_cedula(
    cedula: str,
    service: AlumnoService = Depends(get_alumno_service),
) -> AlumnoResponse:
    alumno = service.obtener_alumno_por_cedula(cedula)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno


@router.put("/{alumno_id}", response_model=AlumnoResponse)
def update_alumno(
    alumno_id: int,
    alumno_in: AlumnoUpdate,
    service: AlumnoService = Depends(get_alumno_service),
) -> AlumnoResponse:
    alumno = service.actualizar_alumno(alumno_id, alumno_in)
    if not alumno:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    return alumno


@router.delete("/{alumno_id}", status_code=204)
def delete_alumno(
    alumno_id: int,
    service: AlumnoService = Depends(get_alumno_service),
):
    success = service.eliminar_alumno(alumno_id)
    if not success:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
