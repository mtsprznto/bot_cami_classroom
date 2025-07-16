# Google Classroom Automation Tool

Herramienta de automatización para Google Classroom que permite gestionar anuncios y materiales del curso de manera programática.

## 🚀 Características

- Publicación automatizada de anuncios en múltiples cursos
- Inclusión de enlaces, videos y formularios en los anuncios
- Validación de anuncios para evitar duplicados
- Interfaz sencilla para la gestión de contenido del curso
- Soporte para múltiples tipos de materiales educativos

## 📋 Requisitos Previos

- Python 3.12
- Cuenta de Google con acceso a Google Classroom
- Credenciales de API de Google Cloud Platform
- Las siguientes bibliotecas de Python:
  - google-api-python-client
  - google-auth-oauthlib
  - google-auth-httplib2
  - google-auth

## 🛠 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/bot_cami_classroom.git
   cd bot_cami_classroom
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las credenciales de Google Cloud Platform:
   - Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com/)
   - Habilita la API de Google Classroom
   - Crea credenciales OAuth 2.0
   - Descarga el archivo JSON de credenciales y guárdalo como `client_secret_603744710152.json`

## 📁 Estructura del Proyecto

- `addanuncio.py`: Script principal para publicar anuncios en los cursos
- `dinamic_announ.py`: Módulo para crear anuncios dinámicos con diferentes tipos de contenido
- `insertcourse.py`: Herramienta para insertar materiales del curso
- `quickstart.py`: Script de ejemplo para listar cursos disponibles
- `utils.py`: Utilidades de validación y funciones auxiliares
- `main.py`: Punto de entrada principal (actualmente vacío)

## 🚀 Uso

### Publicar Anuncios

1. Edita el archivo `addanuncio.py` para configurar los anuncios que deseas publicar.
2. Ejecuta el script:
   ```bash
   python addanuncio.py
   ```

### Listar Cursos Disponibles

Para ver una lista de tus cursos:
```bash
python quickstart.py
```

### Insertar Materiales del Curso

Para agregar materiales a un curso específico:
```bash
python insertcourse.py
```

## 🔧 Configuración

El archivo `addanuncio.py` contiene las siguientes configuraciones:

```python
# IDs de los cursos
CLAS = "example_id"
TEST = "example_id"

# Lista de cursos donde se publicarán los anuncios
ID_COURSES = [CLAS, CLAS, CLAS, TEST, TEST, TEST]
```

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Haz un Fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Distribuido bajo la licencia MIT. Ver `LICENSE` para más información.

## 📧 Contacto

Tu Nombre - [@tucuenta](https://twitter.com/tucuenta)

Enlace del Proyecto: [https://github.com/tuusuario/bot_cami_classroom](https://github.com/tuusuario/bot_cami_classroom)

## 🙏 Agradecimientos

- [Google Classroom API](https://developers.google.com/classroom)
- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
