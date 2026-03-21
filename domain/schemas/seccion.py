from pydantic import BaseModel
from typing import Optional


class SeccionBase(BaseModel):
    grado: int
    letra: str
    modalidad: Optional[str] = "Media General"
    anio_escolar: Optional[str] = None


class SeccionCreate(SeccionBase):
    pass


class SeccionUpdate(BaseModel):
    grado: Optional[int] = None
    letra: Optional[str] = None
    modalidad: Optional[str] = None
    anio_escolar: Optional[str] = None


class SeccionResponse(SeccionBase):
    id: int

    model_config = {
        "from_attributes": True
    }
