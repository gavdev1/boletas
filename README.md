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
      "nombre_representante": "María de Bello",
      "direccion_representante": "Av. Principal Los Mangos, Edif Las Acacias",
      "grado": 1,
      "seccion": "A",
      "numero_lista": 1
    }
    ```
- **GET `/alumnos/`**: Lista alumnos.
- **GET `/alumnos/{id}`**: Detalle por ID.
- **GET `/alumnos/cedula/{cedula}`**: Buscar por cédula.
- **PUT `/alumnos/{id}`**: Actualización parcial o total.
- **DELETE `/alumnos/{id}`**: Eliminar registro.

---

## 📚 Materias (`/materias`)

- **POST `/materias/`**: Crea una materia para un grado específico.
    - **JSON Completo:**
    ```json
    {
      "nombre": "Matemática",
      "grado": 1,
      "es_numerica": true
    }
    ```
- **GET `/materias/`**: Lista materias. Filtra por `?grado=1`.
- **PUT `/materias/{id}`**: Modifica nombre o grado.
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
      "numero_lista": 1
    }
    ```
    *Nota: `hasta_lapso` (1, 2 o 3) define qué columnas se llenarán en el reporte.*
- **GET `/boletas/{id}/pdf`**: **Descarga directa del PDF**. 🖨️
- **GET `/boletas/`**: Listado de todas las boletas creadas.
- **GET `/boletas/{id}`**:JSON detallado con notas inyectadas.
- **DELETE `/boletas/{id}`**: Eliminar boleta.


## 🚀 Cómo utilizar los endpoints (Guía Rápida)

1.  **GET**: Utilízalos para consultar. Muchos aceptan query params como `?skip=0&limit=10` para paginar resultados.
2.  **POST**: Utilízalos para crear nuevos datos. Pasa el **JSON Completo** en el cuerpo de la petición.
3.  **PUT**: Utilízalos para editar. Solo necesitas enviar los campos que quieres cambiar en el JSON; los demás mantendrán su valor.
4.  **DELETE**: Utilízalos para borrar. Solo requieren el ID en la URL. Devuelven un código `204 No Content` si la operación fue exitosa.
