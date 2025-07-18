
from .client import cliente_llm, get_groq_client
import random
import logging
import os



logger = logging.getLogger("teacher_bot")
logger.setLevel(logging.INFO)

# Handler para consola
console_handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
console_handler.setFormatter(formatter)

# Evitar duplicados
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    logger.addHandler(console_handler)










async def teacher_bot():
    try:
        client = get_groq_client()
        if not client:
            raise RuntimeError("❌ Cliente Groq no disponible")

        system_message = """
        Tienes una excelente redaccion y una excelente ortografia ademas de mucho manejo de la gramatica y sintaxis
        Eres una especialista de pedagogia, lenguaje y comunicacion
        Incluye siempre 
        - Estimos estudiantes
        - Queridos estudiantes
        
        
        Contexto:
        - Se espera que los estudiantes revisen el contenido de la semana pasada
        
        
        - Tienes que devolver solo un titulo
        - Solo devuelve el titulo
        - Agrega palabras de animo y motivacion
        
        Ejemplo:
        - Estimados estudiantes comparto la presentacion correspondiente al contenido revisado durante la ultima semana
        - Queridos estudiantes comparto con ustedes el canvas de la ultima semana, les deseo un buen fin de semana
        
        
        Solo tienes que devolver estricatemente una respuesta
        """

        user_message = ""

        generated = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=1,
            max_completion_tokens=1024,
            stream=True
        )

        final_text = ""
        for chunk in generated:
            final_text += chunk.choices[0].delta.content or ""

        return final_text.strip()

    except Exception as e:
        print(f"❌ Error en teacher_bot: {e}")
        logger.error(f"❌ Error en teacher_bot: {e}")
        
        
        
        logger.warning(f"⚠️ Fallback activado. Error: {e}")
        
        # Fallback pedagógico
        respuestas_fallback = [
            "Estimados estudiantes, les comparto el material revisado la semana pasada. ¡Mucho éxito!",
            "Queridos estudiantes, les dejo la presentación correspondiente. ¡Sigan aprendiendo con entusiasmo!",
            "Estimados estudiantes, revisen el contenido compartido. ¡Vamos que se puede!",
            "Queridos estudiantes, les deseo un excelente día y buena energía para continuar con sus estudios.",
            "Estimados estudiantes, aquí está el material de esta semana. ¡Confíen en sus capacidades!",
            "Queridos estudiantes, repasen este contenido y sigan construyendo su aprendizaje. ¡Adelante!",
            "Estimados estudiantes, les comparto el recurso que vimos. ¡Qué alegría seguir aprendiendo juntos!",
        ]
        mensaje = random.choice(respuestas_fallback)


        return mensaje



