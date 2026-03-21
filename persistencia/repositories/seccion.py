from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import List, Optional
from persistencia.models import Seccion
from domain.schemas.seccion import SeccionCreate, SeccionUpdate


class SeccionRepository:
    def __init__(self, session: Session):
        self.session = session

    def count(self) -> int:
        stmt = select(func.count()).select_from(Seccion)
        return self.session.scalars(stmt).first() or 0

    def create(self, seccion_in: SeccionCreate) -> Seccion:
        db_seccion = Seccion(**seccion_in.model_dump())
        self.session.add(db_seccion)
        self.session.commit()
        self.session.refresh(db_seccion)
        return db_seccion

    def get_by_id(self, seccion_id: int) -> Optional[Seccion]:
        stmt = select(Seccion).where(Seccion.id == seccion_id)
        return self.session.scalars(stmt).first()
        
    def get_by_unique_fields(self, grado: int, letra: str, modalidad: str) -> Optional[Seccion]:
        stmt = select(Seccion).where(
            Seccion.grado == grado,
            Seccion.letra == letra,
            Seccion.modalidad == modalidad
        )
        return self.session.scalars(stmt).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Seccion]:
        stmt = select(Seccion).offset(skip).limit(limit)
        return list(self.session.scalars(stmt).all())

    def update(self, seccion_id: int, seccion_in: SeccionUpdate) -> Optional[Seccion]:
        db_seccion = self.get_by_id(seccion_id)
        if not db_seccion:
            return None

        update_data = seccion_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_seccion, key, value)

        self.session.commit()
        self.session.refresh(db_seccion)
        return db_seccion

    def delete(self, seccion_id: int) -> bool:
        db_seccion = self.get_by_id(seccion_id)
        if not db_seccion:
            return False

        self.session.delete(db_seccion)
        self.session.commit()
        return True
