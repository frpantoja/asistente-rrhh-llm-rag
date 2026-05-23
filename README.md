# Asistente Inteligente de RRHH con LLM y RAG

[![CI](https://github.com/frpantoja/asistente-rrhh-llm-rag/actions/workflows/ci.yml/badge.svg)](https://github.com/frpantoja/asistente-rrhh-llm-rag/actions)

## Descripción

Prototipo académico de un asistente inteligente para consultas internas de Recursos Humanos, desarrollado para la empresa ficticia **Comercial Andina SpA**.

El sistema combina un modelo de lenguaje (LLM) con Retrieval-Augmented Generation (RAG) para responder consultas sobre vacaciones, permisos, licencias médicas, beneficios y normativas internas, basándose exclusivamente en documentos corporativos cargados en el sistema.

## Arquitectura del Sistema

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Consulta   │────▶│   Retrieval      │────▶│   Generación    │
│   usuario    │     │   (FAISS + MMR)  │     │   (LLM + Prompt)│
└─────────────┘     └──────────────────┘     └─────────────────┘
                           │                         │
                    ┌──────┴──────┐            ┌─────┴──────┐
                    │  Filtrado   │            │  Guardrails │
                    │  por umbral │            │  anti-aluc. │
                    │  + Re-rank  │            │  + Few-shot │
                    └─────────────┘            └────────────┘
```

### Pipeline RAG

1. **Ingesta**: Los documentos `.txt` se cargan con metadatos automáticos (tipo, título, fuente).
2. **Chunking**: División con `RecursiveCharacterTextSplitter` (300 chars, overlap 80) con separadores optimizados para español.
3. **Indexación**: Generación de embeddings (`text-embedding-3-small`) y almacenamiento en FAISS.
4. **Retrieval**: Búsqueda por similitud con filtrado por umbral (`>0.3`) y selección de top-k.
5. **Generación**: Prompt estructurado con few-shot examples y guardrails contra alucinaciones.

### Componentes Técnicos

| Componente | Tecnología | Propósito |
|---|---|---|
| Embeddings | `text-embedding-3-small` (Azure) | Representación vectorial de documentos |
| Vector Store | FAISS | Búsqueda de similitud eficiente |
| LLM | `gpt-4o-mini` (Azure) | Generación de respuestas |
| Framework | LangChain | Orquestación del pipeline RAG |
| CI/CD | GitHub Actions | Tests automáticos y validación |

## Estructura del Proyecto

```
asistente-rrhh-llm-rag/
├── app.py                      # Interfaz de consola principal
├── config/
│   ├── __init__.py
│   └── settings.py             # Configuración centralizada
├── src/
│   ├── __init__.py
│   ├── cargar_documentos.py    # Carga de documentos con metadatos
│   ├── crear_vectores.py       # Pipeline de indexación
│   ├── prompts.py              # Templates de prompts avanzados
│   └── rag_pipeline.py         # Pipeline RAG con re-ranking
├── tests/
│   ├── __init__.py
│   ├── test_cargar_documentos.py
│   ├── test_prompts.py
│   └── test_rag_pipeline.py
├── data/
│   ├── internos/               # Documentos corporativos simulados
│   └── externos/               # Normativa laboral de referencia
├── evidencias/                 # Capturas de pruebas
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de CI con GitHub Actions
├── .env.example                # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
└── README.md
```

## Requisitos Previos

- Python 3.10 o superior
- Git
- Token personal de GitHub con permisos de lectura de modelos

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/frpantoja/asistente-rrhh-llm-rag.git
cd asistente-rrhh-llm-rag

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate          # Linux/macOS
# venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu GITHUB_TOKEN personal
```

## Configuración del Token

Crea un token en [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens) con permiso de lectura para modelos (`models:read`).

Agrega el token en el archivo `.env`:
```env
GITHUB_TOKEN=ghp_tu_token_aqui
```

## Uso

### 1. Crear la base vectorial

```bash
python -m src.crear_vectores
```

### 2. Ejecutar el asistente

```bash
python app.py
```

### Ejemplos de consultas

- ¿Cuántos días de vacaciones me corresponden?
- ¿Cómo solicito un permiso administrativo?
- ¿Qué debo hacer si tengo una licencia médica?
- ¿Qué beneficios internos ofrece la empresa?

### 3. Ejecutar tests

```bash
python -m pytest tests/ -v
```

## Decisiones Técnicas

### ¿Por qué chunks de 300 caracteres?

Los documentos de RRHH son cortos y altamente estructurados (promedio ~650 chars). Chunks de 500 (versión anterior) podían contener múltiples secciones mezcladas, diluyendo la relevancia. Chunks de 300 con overlap de 80 permiten capturar secciones individuales con contexto suficiente.

### ¿Por qué umbral de similitud?

Sin umbral, el sistema siempre retorna k documentos aunque ninguno sea relevante, lo que causa alucinaciones. El umbral de 0.3 filtra chunks irrelevantes y permite al sistema responder honestamente cuando no tiene información.

### ¿Por qué few-shot en el prompt?

Los ejemplos en el prompt le muestran al modelo el formato esperado de respuesta y, especialmente, cómo responder cuando no tiene información suficiente. Esto reduce alucinaciones comparado con el prompt genérico original.

## Uso Ético de IA

Este proyecto fue desarrollado con apoyo de inteligencia artificial para mejorar redacción, organización y orientación técnica. El análisis del caso, diseño de la solución, arquitectura y validación fueron realizados por el equipo.

## Autoría

Proyecto académico para la asignatura **Ingeniería de Soluciones con Inteligencia Artificial**.
