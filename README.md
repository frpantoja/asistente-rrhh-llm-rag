# Asistente Inteligente para Consultas Internas de Recursos Humanos usando LLM y RAG

## Descripción del proyecto
Este proyecto corresponde al desarrollo de un prototipo académico orientado a responder consultas frecuentes del área de recursos humanos mediante el uso de inteligencia artificial.

La solución fue diseñada para una empresa ficticia llamada **Comercial Andina SpA**, la cual presenta una problemática común en muchas organizaciones: el área de recursos humanos recibe consultas repetitivas sobre vacaciones, permisos administrativos, licencias médicas, beneficios y normativas internas, lo que genera carga operativa y tiempos de respuesta variables.

Para abordar este problema, se desarrolló un asistente inteligente que combina un modelo de lenguaje (LLM) con un sistema de Recuperación Aumentada de Información (RAG). Esto permite que las respuestas no dependan solo del conocimiento general del modelo, sino también de documentos internos y externos cargados en el sistema.

## Objetivo del proyecto
Diseñar un prototipo capaz de responder consultas internas de recursos humanos de forma clara, rápida y contextualizada, utilizando información proveniente de documentos de la empresa y de fuentes externas relacionadas con la normativa laboral.

## ¿Qué hace el sistema?
El sistema permite que un usuario escriba preguntas en lenguaje natural (por ejemplo, sobre vacaciones, permisos, licencias médicas o beneficios internos). Luego, el programa:
1. Busca información relevante en los documentos cargados.
2. Recupera el contexto más útil.
3. Genera una respuesta apoyada específicamente en esa información.

De esta manera, el prototipo busca mejorar el acceso a la información, reducir la dependencia del área de recursos humanos y entregar respuestas más consistentes.

---

## Tecnologías utilizadas
* Python
* LangChain
* FAISS
* GitHub Models
* Embeddings
* Archivos de texto (`.txt`) como base documental
* Visual Studio Code
* Git y GitHub

---

## Estructura del proyecto
* `data/internos/`: Contiene documentos internos simulados del área de recursos humanos.
* `data/externos/`: Contiene documentos externos de apoyo normativo.
* `src/`: Contiene los archivos de lógica del sistema.
* `evidencias/`: Carpeta destinada a capturas y pruebas del prototipo.
* `app.py`: Archivo principal para ejecutar el asistente.
* `requirements.txt`: Lista de dependencias del proyecto.
* `.env`: Archivo de configuración local para credenciales (no se sube al repositorio).
* `.gitignore`: Archivo que evita subir información sensible o innecesaria.
* `README.md`: Documentación general del proyecto.

---

## Documentos utilizados
El sistema trabaja con documentos internos y externos, los cuales fueron elaborados con fines académicos y simulados de acuerdo con un contexto organizacional realista.

**Documentos internos:**
* Reglamento interno
* Política de vacaciones
* Instructivo de permisos administrativos
* Manual de beneficios
* Procedimiento de licencias médicas

**Documentos externos:**
* Resumen académico del Código del Trabajo
* Información de apoyo de la Dirección del Trabajo
* Referencia general de normativa laboral

---

## Requisitos previos
* **Python** instalado en el equipo.
* **Visual Studio Code** (o un editor de código similar).
* **Git** instalado.
* Un **token personal de GitHub** con permisos habilitados para el uso de modelos.

---

## Instalación del proyecto

1. **Clonar el repositorio:** Clona o descarga este repositorio en tu equipo.  
2. **Abrir el editor:** Abre la carpeta del proyecto en Visual Studio Code.  
3. **Crear un entorno virtual:** Abre la terminal integrada y ejecuta el siguiente comando:

```bash
python -m venv venv
```

### 4. Activar el entorno virtual

En Windows:

```bash
venv\Scripts\activate
```

En macOS o Linux:

```bash
source venv/bin/activate
```

### 5. Instalar dependencias

Con el entorno virtual activado, ejecuta:

```bash
pip install -r requirements.txt
```

## Configuración del archivo `.env`

Para que el sistema funcione, es necesario crear un archivo llamado `.env` en la raíz del proyecto. Este archivo no debe subirse al repositorio, ya que contiene información sensible.

Dentro del archivo `.env`, debe escribirse lo siguiente:

```env
GITHUB_TOKEN=TU_TOKEN_AQUI
OPENAI_BASE_URL=https://models.inference.ai.azure.com
```

### Importante sobre el token

La persona que ejecute el proyecto debe usar su propio token personal de GitHub.

Ese token debe tener permiso para modelos. En GitHub puede aparecer como:

- `Models`
- `Models: Read`
- `models`
- `models:read`

Esto puede variar según el idioma de la cuenta o el tipo de token creado, pero la idea es que tenga permiso de lectura para usar modelos.

No se debe reutilizar ni publicar el token de otra persona. Cada usuario debe crear y configurar el suyo de forma local.

---

## ¿Cómo funciona el sistema?

El funcionamiento general del prototipo es el siguiente:

1. El usuario realiza una consulta en lenguaje natural.
2. El sistema busca fragmentos relevantes dentro de los documentos previamente cargados.
3. Se recupera el contexto más útil para responder a la consulta.
4. El modelo de lenguaje genera una respuesta basada exclusivamente en ese contexto.
5. La respuesta se entrega al usuario en la pantalla de la consola.

---

## Ejecución del proyecto

### 1. Creación de la base vectorial

Antes de ejecutar el asistente por primera vez, o si se modifican los documentos base, es necesario crear la base vectorial. Ejecuta el siguiente comando en la terminal:

```bash
python src\crear_vectores.py
```

Si todo está correcto, el sistema mostrará mensajes indicando que los documentos fueron cargados y que la base vectorial fue creada exitosamente.

### 2. Ejecución del asistente

Una vez creada la base vectorial, puedes iniciar el asistente interactivo con este comando:

```bash
python app.py
```

Al iniciar, el programa solicitará que el usuario ingrese una consulta.

---

## Ejemplos de uso

Puedes probar el asistente con preguntas como las siguientes:

- ¿Cuántos días de vacaciones me corresponden?
- ¿Cómo se solicita un permiso administrativo?
- ¿Qué debo hacer si tengo una licencia médica?
- ¿Qué beneficios internos entrega la empresa?
- ¿Dónde puedo hacer consultas sobre vacaciones o permisos?

---

## Archivos principales del sistema

### `src/cargar_documentos.py`

Permite leer los documentos de texto desde las carpetas internas y externas.

### `src/crear_vectores.py`

Carga los documentos, los divide en fragmentos, genera embeddings y crea la base vectorial.

### `src/rag_pipeline.py`

Contiene la lógica principal del sistema RAG. Recupera contexto y genera respuestas con el modelo.

### `app.py`

Permite ejecutar el asistente desde consola y realizar preguntas.


---

## Uso ético de inteligencia artificial

Este proyecto fue desarrollado con apoyo de inteligencia artificial para mejorar redacción, organización de ideas y orientación técnica general. El análisis del caso, la definición de requerimientos, el diseño de la solución, la arquitectura y la validación del contenido fueron realizados y revisados por el equipo.

---

## Autoría

Proyecto académico desarrollado para la asignatura **Ingeniería de Soluciones con Inteligencia Artificial**.
