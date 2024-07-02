# 🎁 Sistemas de Gestión de Eventos 🎉

✨ **Descripción**

¡Bienvenido al proyecto **Sistemas de Gestión de Eventos**! 🛒

Este proyecto te sumerge en el mundo de la gestión de eventos, permitiéndote crear, organizar y administrar eventos de manera eficiente. Al finalizar esta tarea, habrás consolidado tus habilidades en Programación Orientada a Objetos con Python, bases de datos relacionales (PostgreSQL) y desarrollo de interfaces de usuario intuitivas.

🚀 **Características Principales**

*   **Creación y Gestión de Eventos:** Define detalles como fecha, hora, lugar, capacidad y más.
*   **Registro de Participantes:** Permite a los usuarios inscribirse en eventos.
*   **Panel de Administración:** Controla todos los aspectos de los eventos desde un panel intuitivo.
*   🎨 **Diseño Minimalista y Oscuro:** Una interfaz moderna y elegante para una experiencia de usuario óptima.

🛠️ **Tecnologías Utilizadas**

*   **Backend:**
    *   **Django:** El potente framework web de Python que impulsa la aplicación.
    *   **PostgreSQL:** Base de datos robusta y eficiente para almacenar los datos de eventos y participantes.
*   **Frontend:**
    *   **HTML, CSS, JavaScript:** Lenguajes esenciales para construir la interfaz de usuario.
    *   **Font Awesome:** Biblioteca de iconos para añadir elementos visuales atractivos.

## ⚙️ Cómo Ejecutar la Aplicación

**Prerrequisitos:**

*   **Python:** Asegúrate de tener Python instalado en tu sistema. Puedes descargarlo desde [https://www.python.org/](https://www.python.org/).
*   **PostgreSQL:** Descarga e instala PostgreSQL desde [https://www.postgresql.org/](https://www.postgresql.org/).
    *   **Configuración:**
        *   Crea una base de datos para el proyecto.
        *   Crea un usuario y otorga los permisos necesarios sobre la base de datos.
        *   Actualiza el archivo `settings.py` de Django con la información de conexión a tu base de datos:

            ```python
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'tu_base_de_datos',  # Reemplaza con el nombre de tu base de datos
                    'USER': 'tu_usuario',        # Reemplaza con tu usuario de PostgreSQL
                    'PASSWORD': 'tu_contraseña',  # Reemplaza con tu contraseña
                    'HOST': 'localhost',
                    'PORT': '5432',
                }
            }
            ```

**Pasos:**

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/fborjaz/Proy_System_Event.git](https://github.com/fborjaz/Proy_System_Event.git)
    cd Proy_System_Event
    ```

2.  **Crear (o activar) un entorno virtual:**

    ```bash
    py -m venv venv
    .\venv\Scripts\activate  # Windows
    source venv/bin/activate  # macOS/Linux
    ```

3.  **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplicar las migraciones:**

    ```bash
    py manage.py makemigrations
    py manage.py migrate
    ```

5.  **Crear un superusuario:**

    ```bash
    py manage.py createsuperuser
    ```

6.  **Ejecutar el servidor de desarrollo:**

    ```bash
    py manage.py runserver
    ```

7.  **Acceder a la aplicación:**

    *   Abre tu navegador web y visita: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (para la interfaz principal)
    *   Accede al panel de administración: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) (utiliza las credenciales del superusuario).

## ¡Explora y disfruta de Sistema de Gestión de Eventos! 🎉
