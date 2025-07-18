import asyncio
from .client import cliente_llm, get_groq_client



async def teacher_bot():
    #client = cliente_llm()
    client = get_groq_client()
    
    if not client:
        raise RuntimeError("❌ No se pudo crear el cliente")
    
    
    
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
    
    generated_message = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    final_text = ""
    for chunk in generated_message:
        final_text += chunk.choices[0].delta.content or ""
    return final_text.strip()



if __name__ == "__main__":
    asyncio.run(teacher_bot())
