from pathlib import Path
from typing import List


def cargar_textos_desde_carpeta(ruta_carpeta: str) -> List[str]:
    ruta = Path(ruta_carpeta)
    textos = []

    if not ruta.exists():
        print(f"La carpeta no existe: {ruta_carpeta}")
        return textos

    for archivo in ruta.glob("*.txt"):
        try:
            contenido = archivo.read_text(encoding="utf-8")
            textos.append(contenido)
        except Exception as e:
            print(f"Error al leer {archivo.name}: {e}")

    return textos


if __name__ == "__main__":
    internos = cargar_textos_desde_carpeta("data/internos")
    externos = cargar_textos_desde_carpeta("data/externos")

    print(f"Documentos internos cargados: {len(internos)}")
    print(f"Documentos externos cargados: {len(externos)}")