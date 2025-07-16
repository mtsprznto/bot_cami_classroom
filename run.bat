@echo off
REM Verificar si existe el entorno virtual
IF NOT EXIST ".venv\" (
    echo Creando entorno virtual...
    python -m venv .venv
)


REM Activar entorno virtual
call .venv\Scripts\activate

REM Instalar dependencias
pip install -r requirements.txt

cls

REM Ejecutar script principal
python addanuncio.py

REM Opcional: pausar la terminal después de ejecutar
pause