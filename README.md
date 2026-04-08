# 🎓 BackendApp - Sistema de Gestión Escolar y Boletas

Este sistema permite la gestión integral de alumnos, materias, calificaciones y la generación automatizada de boletas de evaluación en formato PDF.

---

## 🔐 Autenticación Global (`/auth`)

Todos los endpoints (excepto los de `/auth`) requieren un token JWT en la cabecera:
`Authorization: Bearer <tu_access_token>`

### Endpoints de Autenticación
- **POST `/auth/register`**: Registra un nuevo Director/Administrador.
    - **JSON Completo:**
    ```json
    {
      "username": "director",
      "email": "director@escuela.com",
      "password": "mi_password_segura"
    }
    ```
- **POST `/auth/login`**: Obtiene el token de acceso.
    - **JSON Completo:**
    ```json
    {
      "username": "director",
      "password": "mi_password_segura"
    }
    ```
- **POST `/auth/forgot-password`**: Inicia recuperación por email.
    - **JSON Completo:**
    ```json
    {
      "email": "director@escuela.com"
    }
    ```
- **POST `/auth/reset-password`**: Establece nueva contraseña.
    - **JSON Completo:**
    ```json
    {
      "token": "token_jwt_recuperacion_recibido",
      "new_password": "nueva_password_123"
    }
    ```

---

## 🛠️ Configuración General (`/configuracion`)

Define los datos del plantel y el año escolar actual.

- **POST `/configuracion/`**: Establece datos globales (se usan automáticamente en boletas).
    - **JSON Completo:**
    ```json
    {
      "nombre_plantel": "U.E. Colegio Las Acacias",
      "direccion_plantel": "Av. Principal Los Mangos, Valencia",
      "anio_escolar_actual": "2024-2025",
      "profesor_guia_default": "Prof. Roberto Gómez"
    }
    ```
- **GET `/configuracion/`**: Obtiene la configuración actual.

---

## 📊 Dashboard y Estadísticas (`/dashboard`)

Resumen dinámico del estado del sistema y la población escolar.

- **GET `/dashboard/stats`**: Devuelve estadísticas globales.
    - **Respuesta de ejemplo:**
    ```json
    {
      "alumnos": {
        "total": 150,
        "presente": 120,
        "egresado": 20,
        "retirado": 10
      },
      "secciones": 6,
      "materias": 45
    }
    ```

---

## 🏫 Gestión de Secciones (`/secciones`)

- **POST `/secciones/`**: Registra una nueva sección.
    - **JSON Completo:**
    ```json
    {
      "grado": 1,
      "letra": "A",
      "modalidad": "Media General",
      "anio_escolar": "2025-2026"
    }
    ```
- **GET `/secciones/`**: Lista de secciones. Permite filtros como `?grado=1&letra=A&modalidad=Técnica`.
- **GET `/secciones/{id}`**: Detalle de una sección específica.
- **PUT `/secciones/{id}`**: Actualiza los datos de la sección.
- **DELETE `/secciones/{id}`**: Elimina una sección.

---

## 👥 Gestión de Alumnos (`/alumnos`)

- **POST `/alumnos/`**: Registro de nuevo estudiante con todos sus datos.
    - **JSON Completo:**
    ```json
    {
      "cedula": "V-30000001",
      "nombre": "Andrés",
      "apellido": "Bello",
      "codigo": "AB-2024-X",
      "fecha_nacimiento": "2012-05-15",
      "lugar_nacimiento": "Caracas",
      "estado_nacimiento": "Distrito Capital",
      "municipio": "Libertador",
      "nombre_representante": "María de Bello",
      "correo_representante": "maria@ejemplo.com",
      "direccion_representante": "Av. Principal Los Mangos",
      "correo_estudiante": "andres@ejemplo.com",
      "grado": 1,
      "seccion": "A",
      "numero_lista": 1,
      "modalidad": "Media General",
      "status": "presente"
    }
    ```
*Nota: El campo `status` puede ser `presente`, `egresado` o `retirado`.*
- **GET `/alumnos/`**: Lista alumnos.
- **GET `/alumnos/{id}`**: Detalle por ID.
- **GET `/alumnos/cedula/{cedula}`**: Buscar por cédula.
- **PUT `/alumnos/{id}`**: Actualización parcial o total.
- **DELETE `/alumnos/{id}`**: Eliminar registro.

---

## 📚 Materias (`/materias`)

- **POST `/materias/`**: Crea una materia para un grado y modalidad específica.
    - **JSON Completo:**
    ```json
    {
      "nombre": "Matemática",
      "grado": 1,
      "es_numerica": true,
      "modalidad": "Media General"
    }
    ```
- **GET `/materias/`**: Lista materias. Permite filtrado matricial cruzado `?grado=1&modalidad=Técnica`.
- **PUT `/materias/{id}`**: Modifica nombre, grado o modalidad.
- **DELETE `/materias/{id}`**: Borrar materia.

---

## 📝 Calificaciones - Express Flow (`/calificaciones`)

Carga de notas simplificada. El servidor calcula promedios automáticamente.

- **POST `/calificaciones/`**: Registra/Actualiza una nota de lapso.
    - **JSON Completo:**
    ```json
    {
      "alumno_id": 1,
      "materia_id": 1,
      "lapso": 1,
      "nota": 18,
      "anio_escolar": "2024-2025",
      "literal": "A"
    }
    ```
- **GET `/calificaciones/alumno/{alumno_id}`**: Historial de notas del alumno.
- **PUT `/calificaciones/{id}`**: Editar registro individual.
- **DELETE `/calificaciones/{id}`**: Borrar nota.

> [!IMPORTANT]
> **Seguridad**: Solo se pueden registrar o modificar notas de alumnos con estatus `"presente"`. El sistema bloqueará automáticamente cualquier intento de cargar calificaciones a alumnos retirados o egresados.

---

## 📄 Boletas e Inteligencia de Negocio (`/boletas`)

Generación de reportes PDF con cálculos de promedios de sección automáticos.

- **POST `/boletas/`**: Genera el registro de la boleta.
    - **JSON Completo:**
    ```json
    {
      "alumno_id": 1,
      "hasta_lapso": 2,
      "tipo_evaluacion": "Acumulativa de Lapsos 1 y 2",
      "observaciones": "Alumno con excelente participación.",
      "profesor": "Lic. Pedro Pérez",
      "nombre_plantel": "U.E. Colegio Las Acacias",
      "direccion_plantel": "Valencia, Venezuela",
      "anio_escolar": "2024-2025",
      "grado": 1,
      "seccion": "A",
      "numero_lista": 1,
      "modalidad": "Media General",
      "inasistencias_lapso_1": 2,
      "inasistencias_lapso_2": 0,
      "inasistencias_lapso_3": 0
    }
    ```
    *Nota: `hasta_lapso` (1, 2 o 3) define qué columnas se llenarán en el reporte. El backend filtrará las calificaciones y aislará la métrica de promedios "media_seccion" dinámicamente según la `modalidad` enviada.*
- **GET `/boletas/{id}/pdf`**: **Descarga directa del PDF**. 🖨️
- **GET `/boletas/bulk/pdf`**: **Generación Masiva**. 🚀 
    - Genera un único PDF con todas las boletas de una sección.
    - **Query Params:** `grado`, `seccion`, `anio_escolar`, `tipo_evaluacion`.
- **GET `/boletas/`**: Listado de todas las boletas creadas.
- **GET `/boletas/{id}`**: JSON detallado con notas inyectadas.
- **DELETE `/boletas/{id}`**: Eliminar boleta.


## 🚀 Cómo utilizar los endpoints (Guía Rápida)

1.  **GET**: Utilízalos para consultar. Muchos aceptan query params como `?skip=0&limit=10` para paginar resultados.
2.  **POST**: Utilízalos para crear nuevos datos. Pasa el **JSON Completo** en el cuerpo de la petición.
3.  **PUT**: Utilízalos para editar. Solo necesitas enviar los campos que quieres cambiar en el JSON; los demás mantendrán su valor.
4.  **DELETE**: Utilízalos para borrar. Solo requieren el ID en la URL. Devuelven un código `204 No Content` si la operación fue exitosa.
