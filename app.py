from src.rag_pipeline import responder_consulta


def main():
    print("Asistente inteligente de RRHH con LLM y RAG")
    print("Escribe tu consulta o escribe 'salir' para terminar.\n")

    while True:
        pregunta = input("Consulta: ")

        if pregunta.lower() == "salir":
            print("Programa finalizado.")
            break

        try:
            respuesta = responder_consulta(pregunta)
            print("\nRespuesta:")
            print(respuesta)
            print("\n" + "-" * 60 + "\n")
        except Exception as e:
            print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    main()