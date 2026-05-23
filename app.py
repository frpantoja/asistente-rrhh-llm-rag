"""
Interfaz de consola del Asistente de RRHH.

Mejoras respecto a la versión original:
- Usa la clase AsistenteRRHH (instancia única, no recrea por consulta).
- Muestra fuentes utilizadas en cada respuesta.
- Logging configurado.
- Manejo robusto de errores con mensajes descriptivos.
"""

import logging

from config.settings import LOG_LEVEL, LOG_FORMAT
from src.rag_pipeline import AsistenteRRHH

logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def main():
    print("\n" + "=" * 60)
    print("  Asistente Inteligente de RRHH - Comercial Andina SpA")
    print("  Escribe tu consulta o 'salir' para terminar.")
    print("=" * 60 + "\n")

    try:
        asistente = AsistenteRRHH()
    except ValueError as e:
        print(f"\n❌ Error de configuración: {e}")
        print("Revisa el archivo .env y asegúrate de tener un GITHUB_TOKEN válido.")
        return

    while True:
        try:
            pregunta = input("📝 Consulta: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nPrograma finalizado.")
            break

        if not pregunta:
            continue

        if pregunta.lower() in ("salir", "exit", "quit"):
            print("Programa finalizado.")
            break

        try:
            resultado = asistente.consultar(pregunta)

            print(f"\n💬 Respuesta:")
            print(resultado.respuesta)

            if resultado.fuentes:
                print(f"\n📄 Fuentes consultadas:")
                for fuente in set(resultado.fuentes):
                    print(f"   - {fuente}")

            print(f"\n📊 Documentos relevantes: {resultado.num_documentos_relevantes}")
            print("\n" + "-" * 60 + "\n")

        except Exception as e:
            logger.error("Error al procesar consulta: %s", e, exc_info=True)
            print(f"\n❌ Ocurrió un error: {e}")
            print("Intenta reformular tu consulta.\n")


if __name__ == "__main__":
    main()
