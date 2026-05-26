"""Tests para el modulo de memoria del agente."""

import pytest
from src.memoria import (
    MemoriaBuffer,
    MemoriaWindow,
    MemoriaSummary,
    crear_memoria,
    crear_memoria_corto_plazo,
    obtener_resumen_memoria,
    MEMORIA_TIPOS,
)


# --- Tests de MemoriaBuffer ---

def test_buffer_vacia_al_inicio():
    mem = MemoriaBuffer()
    assert len(mem.obtener_mensajes()) == 0


def test_buffer_guarda_todo():
    mem = MemoriaBuffer()
    for i in range(10):
        mem.agregar_interaccion(f"Pregunta {i}", f"Respuesta {i}")
    # 10 interacciones = 20 mensajes, sin recortar
    assert len(mem.obtener_mensajes()) == 20


def test_buffer_resumen_vacia():
    mem = MemoriaBuffer()
    assert "vacia" in mem.obtener_resumen().lower()


def test_buffer_limpiar():
    mem = MemoriaBuffer()
    mem.agregar_interaccion("Hola", "Hola")
    mem.limpiar()
    assert len(mem.obtener_mensajes()) == 0


# --- Tests de MemoriaWindow ---

def test_window_vacia_al_inicio():
    mem = MemoriaWindow(window_size=3)
    assert len(mem.obtener_mensajes()) == 0


def test_window_recorta_correctamente():
    mem = MemoriaWindow(window_size=2)
    mem.agregar_interaccion("Pregunta 1", "Respuesta 1")
    mem.agregar_interaccion("Pregunta 2", "Respuesta 2")
    mem.agregar_interaccion("Pregunta 3", "Respuesta 3")
    # Ventana de 2 = maximo 4 mensajes
    assert len(mem.obtener_mensajes()) == 4


def test_window_conserva_los_recientes():
    mem = MemoriaWindow(window_size=1)
    mem.agregar_interaccion("Antigua", "Vieja")
    mem.agregar_interaccion("Reciente", "Nueva")
    msgs = mem.obtener_mensajes()
    assert msgs[0].content == "Reciente"
    assert msgs[1].content == "Nueva"


def test_window_resumen():
    mem = MemoriaWindow(window_size=5)
    mem.agregar_interaccion("Hola", "Hola")
    resumen = mem.obtener_resumen()
    assert "2 mensajes" in resumen


def test_window_limpiar():
    mem = MemoriaWindow()
    mem.agregar_interaccion("Hola", "Hola")
    mem.limpiar()
    assert len(mem.obtener_mensajes()) == 0


# --- Tests de MemoriaSummary ---

def test_summary_vacia_al_inicio():
    mem = MemoriaSummary()
    assert len(mem.obtener_mensajes()) == 0


def test_summary_guarda_sin_llm():
    """Sin LLM no puede resumir, pero guarda los mensajes."""
    mem = MemoriaSummary(llm=None)
    mem.agregar_interaccion("Pregunta", "Respuesta")
    assert len(mem.obtener_mensajes()) == 2


def test_summary_resumen_vacia():
    mem = MemoriaSummary()
    assert "vacia" in mem.obtener_resumen().lower()


def test_summary_cuenta_interacciones():
    mem = MemoriaSummary()
    mem.agregar_interaccion("P1", "R1")
    mem.agregar_interaccion("P2", "R2")
    assert "2 interacciones" in mem.obtener_resumen()


def test_summary_limpiar():
    mem = MemoriaSummary()
    mem.agregar_interaccion("Hola", "Hola")
    mem.limpiar()
    assert len(mem.obtener_mensajes()) == 0
    assert mem._interaction_count == 0


# --- Tests de fabrica ---

def test_crear_memoria_window():
    mem = crear_memoria("window", window_size=3)
    assert isinstance(mem, MemoriaWindow)


def test_crear_memoria_buffer():
    mem = crear_memoria("buffer")
    assert isinstance(mem, MemoriaBuffer)


def test_crear_memoria_summary():
    mem = crear_memoria("summary")
    assert isinstance(mem, MemoriaSummary)


def test_crear_memoria_tipo_invalido():
    with pytest.raises(ValueError):
        crear_memoria("inexistente")


def test_tipos_registrados():
    assert "buffer" in MEMORIA_TIPOS
    assert "window" in MEMORIA_TIPOS
    assert "summary" in MEMORIA_TIPOS


# --- Tests de compatibilidad ---

def test_crear_memoria_corto_plazo_retorna_window():
    mem = crear_memoria_corto_plazo()
    assert isinstance(mem, MemoriaWindow)


def test_obtener_resumen_funciona_con_cualquier_tipo():
    for tipo in ["buffer", "window", "summary"]:
        mem = crear_memoria(tipo)
        resumen = obtener_resumen_memoria(mem)
        assert isinstance(resumen, str)
        assert len(resumen) > 0
