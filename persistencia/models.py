from sqlalchemy import Column, Integer, String, Boolean, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from core.database import Base


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    contenido = Column(String, nullable=True)
    completada = Column(Boolean, default=False)


class Seccion(Base):
    __tablename__ = "secciones"

    id = Column(Integer, primary_key=True, index=True)
    grado = Column(Integer, nullable=False)
    letra = Column(String, nullable=False)
    modalidad = Column(String, default="Media General")
    anio_escolar = Column(String, nullable=True)


class Alumno(Base):
    __tablename__ = "alumnos"

    id = Column(Integer, primary_key=True, index=True)
    cedula = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    codigo = Column(String, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    lugar_nacimiento = Column(String, nullable=True)
    estado_nacimiento = Column(String, nullable=True)
    nombre_representante = Column(String, nullable=True)
    correo_representante = Column(String, nullable=True)
    direccion_representante = Column(String, nullable=True)
    correo_estudiante = Column(String, nullable=True)
    grado = Column(Integer, nullable=True) # Grado actual
    seccion = Column(String, nullable=True) # Sección actual
    numero_lista = Column(Integer, nullable=True)
    modalidad = Column(String, default="Media General")
    telefono_representante = Column(String, nullable=True)

    boletas = relationship("Boleta", back_populates="alumno", cascade="all, delete-orphan")
    calificaciones = relationship("Calificacion", back_populates="alumno", cascade="all, delete-orphan")


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    grado = Column(Integer, nullable=False, index=True)
    es_numerica = Column(Boolean, default=True)
    modalidad = Column(String, default="Media General")

    calificaciones = relationship("Calificacion", back_populates="materia")


class Boleta(Base):
    __tablename__ = "boletas"

    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    anio_escolar = Column(String, nullable=False)
    grado = Column(Integer, nullable=False)
    seccion = Column(String, nullable=False)
    numero_lista = Column(Integer, nullable=True)
    tipo_evaluacion = Column(String, nullable=False)
    observaciones = Column(String, nullable=True)
    hasta_lapso = Column(Integer, default=3) # 1, 2 o 3
    media_lapso_1 = Column(Float, nullable=True)
    media_lapso_2 = Column(Float, nullable=True)
    media_lapso_3 = Column(Float, nullable=True)
    medias_globales = Column(Float, nullable=True)

    # Inasistencias
    inasistencias_lapso_1 = Column(Integer, default=0)
    inasistencias_lapso_2 = Column(Integer, default=0)
    inasistencias_lapso_3 = Column(Integer, default=0)

    media_seccion = Column(Float, nullable=True)
    profesor = Column(String, nullable=True)
    nombre_plantel = Column(String, nullable=True)
    direccion_plantel = Column(String, nullable=True)
    modalidad = Column(String, default="Media General")
    created_at = Column(DateTime, server_default=func.now())

    alumno = relationship("Alumno", back_populates="boletas")


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)
    alumno_id = Column(Integer, ForeignKey("alumnos.id"), nullable=False)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    anio_escolar = Column(String, nullable=False, index=True)
    lapso_1_def = Column(Integer, nullable=True)
    lapso_2_def = Column(Integer, nullable=True)
    lapso_3_def = Column(Integer, nullable=True)
    def_final = Column(Integer, nullable=True)
    literal = Column(String, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    alumno = relationship("Alumno", back_populates="calificaciones")
    materia = relationship("Materia", back_populates="calificaciones")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class Configuracion(Base):
    __tablename__ = "configuracion"

    id = Column(Integer, primary_key=True, index=True)
    nombre_plantel = Column(String, nullable=True)
    direccion_plantel = Column(String, nullable=True)
    anio_escolar_actual = Column(String, nullable=True)
    profesor_guia_default = Column(String, nullable=True)
    # Solo debería existir un registro (Singleton) para esta tabla.
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
