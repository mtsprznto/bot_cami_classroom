from groq import Groq
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

_groq_client = None

def cliente_llm():
    try:
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY no está definido en el entorno")
        client = Groq(
            api_key=api_key
        )
        print("Cliente creado exitosamente")
        return client
    except Exception as e:
        print(f"Error al crear el cliente: {e}")
        return None

def get_groq_client():
    global _groq_client

    if _groq_client is not None:
        return _groq_client

    try:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY no está definido en el entorno")

        _groq_client = Groq(api_key=api_key)
        print("✅ Cliente Groq creado exitosamente")
        return _groq_client

    except Exception as e:
        print(f"❌ Error al crear cliente Groq: {e}")
        return None

    
