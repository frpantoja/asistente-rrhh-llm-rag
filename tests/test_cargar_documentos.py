"""Tests para el módulo de carga de documentos."""

import tempfile
from pathlib import Path

from src.cargar_documentos import (
    clasificar_documento,
    extraer_titulo,
    detectar_encoding,
    cargar_documentos,
)


def test_clasificar_documento_interno():
    ruta = Path("data/internos/politica_vacaciones.txt")
    assert clasificar_documento(ruta) == "interno"


def test_clasificar_documento_externo():
    ruta = Path("data/externos/codigo_trabajo.txt")
    assert clasificar_documento(ruta) == "externo"


def test_clasificar_documento_general():
    ruta = Path("data/otro_archivo.txt")
    assert clasificar_documento(ruta) == "general"


def test_extraer_titulo():
    contenido = "POLÍTICA DE VACACIONES\n\n1. Derecho a feriado legal"
    assert extraer_titulo(contenido) == "POLÍTICA DE VACACIONES"


def test_extraer_titulo_con_lineas_vacias():
    contenido = "\n\n  \nTÍTULO DEL DOCUMENTO\nContenido."
    assert extraer_titulo(contenido) == "TÍTULO DEL DOCUMENTO"


def test_extraer_titulo_vacio():
    assert extraer_titulo("") == "Sin título"


def test_cargar_documentos_carpeta_inexistente():
    docs = cargar_documentos("/ruta/que/no/existe")
    assert docs == []


def test_cargar_documentos_con_archivos():
    with tempfile.TemporaryDirectory() as tmpdir:
        internos = Path(tmpdir) / "internos"
        internos.mkdir()
        archivo = internos / "test.txt"
        archivo.write_text("TÍTULO TEST\n\nContenido de prueba.", encoding="utf-8")

        docs = cargar_documentos(tmpdir)

        assert len(docs) == 1
        assert docs[0].metadata["titulo"] == "TÍTULO TEST"
        assert docs[0].metadata["tipo"] == "interno"
        assert "Contenido de prueba" in docs[0].page_content


def test_cargar_documentos_omite_vacios():
    with tempfile.TemporaryDirectory() as tmpdir:
        archivo = Path(tmpdir) / "vacio.txt"
        archivo.write_text("", encoding="utf-8")

        docs = cargar_documentos(tmpdir)
        assert len(docs) == 0
