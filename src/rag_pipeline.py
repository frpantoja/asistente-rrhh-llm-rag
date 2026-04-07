import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


load_dotenv()


PROMPT_SISTEMA = """
Eres un asistente interno de recursos humanos de una empresa de servicios.
Tu función es responder consultas frecuentes de los trabajadores sobre vacaciones,
permisos administrativos, licencias médicas, beneficios, horarios y normativas internas.

Debes responder únicamente en base a la información entregada por los documentos recuperados.
Si la información no es suficiente, debes indicarlo claramente y sugerir que la consulta
sea revisada por el área de recursos humanos.

Usa un lenguaje formal, claro, preciso y fácil de comprender.
No inventes información.
"""


def responder_consulta(pregunta: str) -> str:
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        raise ValueError("No se encontró GITHUB_TOKEN en el archivo .env")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=github_token,
        base_url="https://models.inference.ai.azure.com"
    )

    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    documentos_relevantes = vectorstore.similarity_search(pregunta, k=3)
    contexto = "\n\n".join([doc.page_content for doc in documentos_relevantes])

    prompt_final = f"""
{PROMPT_SISTEMA}

Consulta del usuario:
{pregunta}

Contexto recuperado:
{contexto}

Responde de forma breve, clara y ordenada.
"""

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=github_token,
        base_url="https://models.inference.ai.azure.com"
    )

    respuesta = llm.invoke(prompt_final)
    return respuesta.content


if __name__ == "__main__":
    pregunta = input("Ingresa tu consulta: ")
    respuesta = responder_consulta(pregunta)
    print("\nRespuesta del asistente:\n")
    print(respuesta)