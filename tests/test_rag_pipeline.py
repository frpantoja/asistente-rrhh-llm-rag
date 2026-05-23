"""Tests para el pipeline RAG."""

from unittest.mock import patch
from src.rag_pipeline import RespuestaRAG


def test_respuesta_rag_estructura():
    respuesta = RespuestaRAG(
        respuesta="Test",
        fuentes=["Fuente 1"],
        num_documentos_recuperados=5,
        num_documentos_relevantes=3,
        consulta_original="¿Pregunta?",
    )
    assert respuesta.respuesta == "Test"
    assert len(respuesta.fuentes) == 1
    assert respuesta.num_documentos_recuperados == 5
    assert respuesta.num_documentos_relevantes == 3


def test_respuesta_rag_defaults():
    respuesta = RespuestaRAG(respuesta="Test")
    assert respuesta.fuentes == []
    assert respuesta.num_documentos_recuperados == 0
    assert respuesta.consulta_original == ""


@patch("src.rag_pipeline.GITHUB_TOKEN", "")
def test_asistente_sin_token_falla():
    """Verifica que se lanza error sin GITHUB_TOKEN."""
    from src.rag_pipeline import AsistenteRRHH

    raised = False
    try:
        AsistenteRRHH()
    except ValueError:
        raised = True
    assert raised, "Debería lanzar ValueError sin GITHUB_TOKEN"
