from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from domain.schemas.alumno import AlumnoResponse
from domain.schemas.materia import MateriaResponse
from domain.schemas.calificacion import CalificacionResponse


# --- Boleta Schemas ---

class BoletaBase(BaseModel):
    alumno_id: int
    anio_escolar: Optional[str] = None
    grado: Optional[int] = None
    seccion: Optional[str] = None
    numero_lista: Optional[int] = None
    tipo_evaluacion: Optional[str] = "Final de Lapso"
    observaciones: Optional[str] = None
    hasta_lapso: Optional[int] = 3
    profesor: Optional[str] = None
    nombre_plantel: Optional[str] = None
    direccion_plantel: Optional[str] = None
    modalidad: Optional[str] = "Media General"
    
    inasistencias_lapso_1: Optional[int] = 0
    inasistencias_lapso_2: Optional[int] = 0
    inasistencias_lapso_3: Optional[int] = 0


class BoletaCreate(BoletaBase):
    """Crea una boleta. Si no envías datos de plantel o año, 
    se usarán los de Configuración."""
    pass


class BoletaUpdate(BaseModel):
    anio_escolar: Optional[str] = None
    grado: Optional[int] = None
    seccion: Optional[str] = None
    numero_lista: Optional[int] = None
    tipo_evaluacion: Optional[str] = None
    observaciones: Optional[str] = None
    profesor: Optional[str] = None
    nombre_plantel: Optional[str] = None
    direccion_plantel: Optional[str] = None


class BoletaResponse(BoletaBase):
    id: int
    created_at: Optional[datetime] = None
    alumno: AlumnoResponse
    calificaciones: List[CalificacionResponse] = []
    
    # Campos calculados por el servidor
    media_lapso_1: Optional[float] = None
    media_lapso_2: Optional[float] = None
    media_lapso_3: Optional[float] = None
    medias_globales: Optional[float] = None
    media_seccion: Optional[float] = None

    model_config = {
        "from_attributes": True
    }


class BoletaListResponse(BoletaBase):
    """Response sin calificaciones anidadas, para listados."""
    id: int
    created_at: Optional[datetime] = None
    
    # Campos calculados por el servidor
    media_lapso_1: Optional[float] = None
    media_lapso_2: Optional[float] = None
    media_lapso_3: Optional[float] = None
    medias_globales: Optional[float] = None
    media_seccion: Optional[float] = None

    model_config = {
        "from_attributes": True
    }
