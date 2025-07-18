from groq import Groq
import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

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

if __name__ == "__main__":
    cliente_llm()
    
