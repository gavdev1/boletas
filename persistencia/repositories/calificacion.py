from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_
from typing import List, Optional
from persistencia.models import Calificacion, Alumno
from domain.schemas.calificacion import CalificacionCreate, CalificacionUpdate


class CalificacionRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, calif_in: CalificacionCreate) -> Calificacion:
        db_calif = Calificacion(**calif_in.model_dump())
        self.session.add(db_calif)
        self.session.commit()
        self.session.refresh(db_calif)
        return db_calif

    def get_by_id(self, calif_id: int) -> Optional[Calificacion]:
        stmt = select(Calificacion).options(joinedload(Calificacion.materia)).where(Calificacion.id == calif_id).execution_options(populate_existing=True)
        return self.session.scalars(stmt).first()

    def get_by_alumno_materia_year(self, alumno_id: int, materia_id: int, anio_escolar: str) -> Optional[Calificacion]:
        stmt = select(Calificacion).where(
            Calificacion.alumno_id == alumno_id,
            Calificacion.materia_id == materia_id,
            Calificacion.anio_escolar == anio_escolar
        )
        return self.session.scalars(stmt).first()

    def get_all_by_alumno_year(self, alumno_id: int, anio_escolar: str) -> list[Calificacion]:
        stmt = select(Calificacion).options(joinedload(Calificacion.materia)).where(
            Calificacion.alumno_id == alumno_id,
            Calificacion.anio_escolar == anio_escolar
        )
        return list(self.session.scalars(stmt).all())

    def get_all_by_section_and_year(self, grado: int, seccion: str, anio_escolar: str) -> list[Calificacion]:
        """Fetches all qualifications for all students in a specific section and year."""
        stmt = (
            select(Calificacion)
            .join(Alumno, Calificacion.alumno_id == Alumno.id)
            .options(joinedload(Calificacion.materia))
            .where(
                Alumno.grado == grado,
                Alumno.seccion == seccion,
                Calificacion.anio_escolar == anio_escolar
            )
        )
        return list(self.session.scalars(stmt).all())

    def update(self, calif_id: int, calif_in: CalificacionUpdate) -> Optional[Calificacion]:
        db_calif = self.get_by_id(calif_id)
        if not db_calif:
            return None

        update_data = calif_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_calif, key, value)

        self.session.commit()
        self.session.refresh(db_calif)
        return db_calif

    def delete(self, calif_id: int) -> bool:
        db_calif = self.get_by_id(calif_id)
        if not db_calif:
            return False

        self.session.delete(db_calif)
        self.session.commit()
        return True
