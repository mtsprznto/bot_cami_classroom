from groq import Groq
import os

def cliente_llm():
    try:
        client = Groq(
            # This is the default and can be omitted
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        print("Cliente creado exitosamente")
        return client
    except Exception as e:
        print(f"Error al crear el cliente: {e}")
        return None
    

if __name__ == "__main__":
    cliente_llm()