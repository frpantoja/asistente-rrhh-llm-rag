"""Tests para el módulo de prompts."""

from src.prompts import RAG_PROMPT_TEMPLATE, SYSTEM_PROMPT, FEW_SHOT_EXAMPLES


def test_prompt_template_tiene_variables():
    assert "contexto" in RAG_PROMPT_TEMPLATE.input_variables
    assert "fuentes" in RAG_PROMPT_TEMPLATE.input_variables
    assert "pregunta" in RAG_PROMPT_TEMPLATE.input_variables


def test_prompt_template_formatea_correctamente():
    resultado = RAG_PROMPT_TEMPLATE.format(
        contexto="Contexto de prueba",
        fuentes="- Fuente 1",
        pregunta="¿Cuántos días de vacaciones tengo?",
    )
    assert "Contexto de prueba" in resultado
    assert "Fuente 1" in resultado
    assert "¿Cuántos días de vacaciones tengo?" in resultado


def test_system_prompt_contiene_guardrails():
    assert "ÚNICAMENTE" in SYSTEM_PROMPT
    assert "NO inventes" in SYSTEM_PROMPT
    assert "Recursos Humanos" in SYSTEM_PROMPT


def test_few_shot_tiene_ejemplos():
    assert "Ejemplo 1" in FEW_SHOT_EXAMPLES
    assert "Ejemplo 2" in FEW_SHOT_EXAMPLES


def test_prompt_incluye_instrucciones_fuera_alcance():
    """Verifica que el prompt tiene guardrail para preguntas no-RRHH."""
    assert "no está relacionada con RRHH" in SYSTEM_PROMPT
