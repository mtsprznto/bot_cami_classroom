from groq import Groq
import os
from dotenv import load_dotenv

def cliente_llm():
    try:
        # Cargar variables desde .env
        load_dotenv()

        client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )
        print("Cliente creado exitosamente")
        return client
    except Exception as e:
        print(f"Error al crear el cliente: {e}")
        return None

if __name__ == "__main__":
    cliente_llm()