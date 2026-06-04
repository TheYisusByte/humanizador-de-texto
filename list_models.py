import google.generativeai as genai
import os

# Obtiene la API Key de la variable de entorno GENAI_API_KEY o la solicita por input
api_key = os.environ.get("GENAI_API_KEY")
if not api_key:
    api_key = input("Introduce tu Gemini API Key: ").strip()

if not api_key:
    print("No se facilitó API Key. Saliendo.")
    raise SystemExit(1)

genai.configure(api_key=api_key)

print("Modelos disponibles:")
for m in genai.list_models():
    name = getattr(m, "name", None) or (m.get("name") if isinstance(m, dict) else None) or getattr(m, "model", None) or str(m)
    print(name)
