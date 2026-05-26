"""
Modulo de memoria del agente con tres estrategias.

Implementa tres tipos de memoria de corto plazo, mas la memoria
de largo plazo basada en RAG:

1. Buffer Memory (historial completo):
   Almacena todas las interacciones sin limite.
   Util para conversaciones cortas donde se necesita todo el contexto.

2. Window Memory (ventana deslizante):
   Mantiene solo las ultimas K interacciones.
   Balancea contexto y eficiencia en conversaciones moderadas.

3. Summary Memory (resumen con LLM):
   Resume la conversacion usando el modelo de lenguaje.
   Ideal para conversaciones largas donde los detalles especificos
   pierden importancia frente al contexto general.

4. Memoria de largo plazo (RAG / FAISS):
   Base vectorial con los documentos de RRHH.
   Persistente entre sesiones.
"""

import logging
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

logger = logging.getLogger(__name__)

MEMORY_WINDOW_SIZE = 5
SUMMARY_PROMPT = (
    "Resume la siguiente conversacion en maximo 3 oraciones en espanol. "
    "Conserva los temas principales, las preguntas clave del usuario "
    "y la informacion relevante que se le entrego:\n\n{conversacion}"
)


class MemoriaBuffer:
    """
    Memoria tipo Buffer: almacena el historial completo.

    Guarda todos los mensajes sin recortar. Es la estrategia mas simple
    pero puede consumir muchos tokens en conversaciones largas.
    """

    def __init__(self):
        self._history = InMemoryChatMessageHistory()
        logger.info("MemoriaBuffer creada (sin limite)")

    def agregar_interaccion(self, pregunta: str, respuesta: str) -> None:
        self._history.add_message(HumanMessage(content=pregunta))
        self._history.add_message(AIMessage(content=respuesta))

    def obtener_mensajes(self) -> list:
        return self._history.messages

    def obtener_resumen(self) -> str:
        n = len(self._history.messages)
        if not n:
            return "Memoria buffer vacia."
        return f"Memoria buffer: {n} mensajes almacenados (historial completo)."

    def limpiar(self) -> None:
        self._history.clear()


class MemoriaWindow:
    """
    Memoria tipo Window: ventana deslizante de K interacciones.

    Solo conserva las ultimas K interacciones (2K mensajes).
    Cuando se supera el limite, descarta las mas antiguas.
    Balancea contexto reciente con eficiencia de tokens.
    """

    def __init__(self, window_size: int = MEMORY_WINDOW_SIZE):
        self._history = InMemoryChatMessageHistory()
        self._window_size = window_size
        logger.info("MemoriaWindow creada (ventana=%d)", window_size)

    def agregar_interaccion(self, pregunta: str, respuesta: str) -> None:
        self._history.add_message(HumanMessage(content=pregunta))
        self._history.add_message(AIMessage(content=respuesta))
        self._recortar()

    def _recortar(self) -> None:
        max_msgs = self._window_size * 2
        msgs = self._history.messages
        if len(msgs) > max_msgs:
            self._history.messages = msgs[-max_msgs:]

    def obtener_mensajes(self) -> list:
        return self._history.messages

    def obtener_resumen(self) -> str:
        n = len(self._history.messages)
        if not n:
            return "Memoria window vacia."
        return (
            f"Memoria window: {n} mensajes almacenados "
            f"(ventana de {self._window_size} interacciones)."
        )

    def limpiar(self) -> None:
        self._history.clear()


class MemoriaSummary:
    """
    Memoria tipo Summary: resume la conversacion con el LLM.

    En lugar de guardar todos los mensajes, mantiene un resumen
    generado por el modelo. Cada vez que se agrega una interaccion,
    el resumen se actualiza incorporando la nueva informacion.

    Ventajas:
    - Consumo de tokens constante sin importar la longitud de la conversacion.
    - Retiene el contexto general aunque se pierdan detalles especificos.

    Requiere una instancia de LLM para generar los resumenes.
    """

    def __init__(self, llm=None):
        self._llm = llm
        self._summary = ""
        self._history = InMemoryChatMessageHistory()
        self._interaction_count = 0
        logger.info("MemoriaSummary creada")

    def agregar_interaccion(self, pregunta: str, respuesta: str) -> None:
        self._history.add_message(HumanMessage(content=pregunta))
        self._history.add_message(AIMessage(content=respuesta))
        self._interaction_count += 1

        # Actualizar resumen cada 2 interacciones para no llamar al LLM siempre
        if self._llm and self._interaction_count % 2 == 0:
            self._actualizar_resumen()

    def _actualizar_resumen(self) -> None:
        """Genera un nuevo resumen usando el LLM."""
        mensajes = self._history.messages
        if not mensajes:
            return

        # Armar texto de la conversacion
        texto_conversacion = ""
        if self._summary:
            texto_conversacion += f"Resumen previo: {self._summary}\n\n"
        texto_conversacion += "Interacciones recientes:\n"
        for msg in mensajes:
            rol = "Trabajador" if isinstance(msg, HumanMessage) else "Asistente"
            texto_conversacion += f"{rol}: {msg.content}\n"

        prompt = SUMMARY_PROMPT.format(conversacion=texto_conversacion)

        try:
            respuesta = self._llm.invoke(prompt)
            self._summary = respuesta.content
            # Limpiar historial ya resumido
            self._history.clear()
            logger.info("Resumen de memoria actualizado")
        except Exception as e:
            logger.error("Error al resumir memoria: %s", e)

    def obtener_mensajes(self) -> list:
        """
        Retorna el resumen como mensaje de sistema + mensajes recientes.

        El resumen se inyecta como contexto al inicio, y los mensajes
        que aun no han sido resumidos se agregan despues.
        """
        mensajes = []
        if self._summary:
            mensajes.append(SystemMessage(
                content=f"Resumen de la conversacion previa: {self._summary}"
            ))
        mensajes.extend(self._history.messages)
        return mensajes

    def obtener_resumen(self) -> str:
        n_pendientes = len(self._history.messages)
        if not self._summary and not n_pendientes:
            return "Memoria summary vacia."

        info = f"Memoria summary: {self._interaction_count} interacciones totales."
        if self._summary:
            info += f"\nResumen activo: {self._summary[:120]}..."
        if n_pendientes:
            info += f"\nMensajes pendientes de resumir: {n_pendientes}."
        return info

    def limpiar(self) -> None:
        self._history.clear()
        self._summary = ""
        self._interaction_count = 0


# Tipos de memoria disponibles
MEMORIA_TIPOS = {
    "buffer": MemoriaBuffer,
    "window": MemoriaWindow,
    "summary": MemoriaSummary,
}


def crear_memoria(tipo: str = "window", **kwargs):
    """
    Fabrica de memorias. Crea la memoria segun el tipo solicitado.

    Args:
        tipo: "buffer", "window" o "summary"
        **kwargs: argumentos adicionales (window_size, llm, etc.)

    Returns:
        Instancia de la memoria solicitada.
    """
    if tipo not in MEMORIA_TIPOS:
        raise ValueError(
            f"Tipo de memoria '{tipo}' no reconocido. "
            f"Opciones: {list(MEMORIA_TIPOS.keys())}"
        )

    clase = MEMORIA_TIPOS[tipo]
    memoria = clase(**kwargs)
    logger.info("Memoria creada: tipo=%s", tipo)
    return memoria


# Aliases de compatibilidad
def crear_memoria_corto_plazo():
    """Crea memoria window por defecto (compatibilidad)."""
    return crear_memoria("window", window_size=MEMORY_WINDOW_SIZE)


def obtener_resumen_memoria(memoria) -> str:
    """Obtiene resumen de cualquier tipo de memoria."""
    return memoria.obtener_resumen()
