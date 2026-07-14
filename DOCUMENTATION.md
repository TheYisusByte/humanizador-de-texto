---
# 📄 Manual de Documentación Técnica
**Desarrollado y automatizado bajo la arquitectura de: YisusByte
---

 He analizado el código fuente de este proyecto. A continuación, se presenta una documentación técnica completa en formato Markdown.

---

## 1. ¿Qué hace este proyecto?

Este proyecto implementa una aplicación web interactiva diseñada para **humanizar y corregir la redacción de documentos de Microsoft Word (.docx)** utilizando capacidades de Inteligencia Artificial (IA) generativa, específicamente los modelos de Google Gemini. Su objetivo principal es transformar textos que puedan sonar automáticos, robóticos, monótonos o con una "sensación de IA" en una prosa más natural, fluida, conversacional y empática, manteniendo la integridad del contenido informativo.

La aplicación opera a través de una interfaz de usuario sencilla (construida con Streamlit) que guía al usuario por el siguiente flujo:

1.  **Carga de Documento**: El usuario sube un archivo `.docx`.
2.  **Extracción y Previsualización**: La aplicación extrae el texto del documento y lo muestra para una previsualización.
3.  **Configuración de IA**: El usuario introduce una clave API de Google Gemini.
4.  **Procesamiento por IA**: El texto es enviado a un modelo Gemini junto con un "prompt" cuidadosamente diseñado que le instruye sobre cómo reescribirlo para sonar más humano, aplicando reglas como variar la longitud de las oraciones, usar conectores naturales y mantener la información original.
5.  **Visualización de Resultado**: El texto reescrito por la IA se muestra en la interfaz.
6.  **Descarga**: El usuario puede descargar el texto humanizado en un nuevo archivo `.docx`.

**Tecnologías, Frameworks y Dependencias Utilizadas:**

*   **Python**: Lenguaje de programación principal del proyecto.
*   **Streamlit**: Framework de Python utilizado para construir rápidamente la interfaz de usuario web de la aplicación. Es ideal para crear herramientas interactivas y demos de IA.
*   **Google Generative AI (Gemini API)**: Biblioteca de Python (`google-generativeai`) para interactuar con los modelos de IA generativa de Google. Es el motor de inteligencia artificial que realiza la tarea de reescritura y humanización del texto. El modelo por defecto utilizado es `models/gemini-3.5-flash`, pero se permite la configuración de otros modelos.
*   **`python-docx`**: Biblioteca de Python (`docx`) para crear, leer y modificar archivos de Microsoft Word (.docx). Fundamental para la ingesta y la salida de documentos.
*   **`io`**: Módulo estándar de Python para trabajar con flujos de entrada/salida. Se utiliza específicamente `io.BytesIO` para manejar el documento Word en memoria antes de la descarga, evitando operaciones de disco innecesarias.
*   **`os`**: Módulo estándar de Python utilizado en el script de utilidad para interactuar con el sistema operativo, principalmente para acceder a variables de entorno (como una API Key).

## 2. Estructura del Proyecto

El proyecto se organiza en tres archivos principales de Python, cada uno con una función específica:

```
.
├── app_humanizador.py         # La aplicación web principal de humanización de Word.
├── humanizador.py             # Un script de utilidad que genera/escribe el archivo app_humanizador.py.
└── list_models.py             # Un script de utilidad para listar los modelos disponibles de Google Gemini.
```

*   **`app_humanizador.py`**: Este es el archivo ejecutable de la aplicación web. Contiene toda la lógica de la interfaz de usuario con Streamlit, la interacción con la API de Google Gemini para el procesamiento del texto, y la manipulación de documentos Word para leer el input y generar el output. Es el punto de entrada para el usuario final.

*   **`humanizador.py`**: Este archivo actúa como un *script generador*. Su propósito es escribir (o sobrescribir) el contenido de un archivo llamado `app_humanizador.py`. Es notable que la versión de `app_humanizador.py` que genera tiene algunas diferencias menores respecto al `app_humanizador.py` proporcionado directamente, como el modelo Gemini por defecto (`gemini-1.5-flash` vs `gemini-3.5-flash`) y la adición de metadatos de autoría al documento generado. Este script no es parte de la ejecución normal de la aplicación, sino una herramienta para crear o actualizar el archivo principal de la aplicación.

*   **`list_models.py`**: Este es un script de utilidad independiente. Su función es ayudar a los desarrolladores a verificar y listar los nombres de los modelos de IA generativa de Google Gemini a los que tienen acceso con su clave API. Es útil para depuración o para conocer qué opciones de modelo se pueden usar en `app_humanizador.py`.

## 3. Explicación de Módulos (Paso a Paso)

A continuación, se detalla el rol y la funcionalidad de cada archivo analizado:

### `app_humanizador.py` (Aplicación Principal)

Este archivo es la implementación completa de la aplicación web interactiva.

1.  **Importaciones**:
    *   `streamlit as st`: Importa el framework para construir la UI.
    *   `google.generativeai as genai`: Importa el SDK de Gemini.
    *   `docx.Document`: Importa la clase para manejar documentos Word.
    *   `io`: Importa el módulo para operaciones de E/S en memoria.

2.  **Configuración Inicial de Streamlit**:
    *   `st.set_page_config(...)`: Configura el título de la pestaña del navegador, el icono de la página y el diseño general (centrado).
    *   `st.title(...)` y `st.write(...)`: Muestran el título principal de la aplicación y una breve descripción en la interfaz de usuario.

3.  **Barra Lateral (`st.sidebar`)**:
    *   `st.sidebar.header("Configuración")`: Define el encabezado de la sección de configuración.
    *   `api_key = st.sidebar.text_input("Introduce tu Gemini API Key:", type="password", key='api_key')`: Un campo de entrada de texto para la API Key de Gemini. El `type="password"` oculta la entrada, y `key='api_key'` asegura una identificación única del widget.
    *   `model_name = st.sidebar.text_input("Modelo a usar:", value="models/gemini-3.5-flash", key='model_name')`: Permite al usuario especificar qué modelo Gemini usar, con un valor por defecto.
    *   `st.sidebar.markdown(...)`: Proporciona enlaces útiles para obtener la API Key.

4.  **Carga de Archivo Word**:
    *   `uploaded_file = st.file_uploader("Elige un archivo de Word (.docx)", type=["docx"])`: Widget para que el usuario suba un archivo. Solo acepta archivos `.docx`.

5.  **Lógica de Procesamiento Principal (`if uploaded_file:` bloque)**:
    *   **Validación de API Key**: `if not api_key:` muestra una advertencia si la API Key no se ha introducido.
    *   **Configuración de Gemini**: `genai.configure(api_key=api_key)` inicializa el cliente de la API con la clave proporcionada.
    *   **Lectura del Documento**:
        *   `doc = Document(uploaded_file)`: Carga el archivo subido en un objeto `Document`.
        *   Un bucle extrae el texto de cada párrafo del documento y lo concatena en `texto_original`, separando los párrafos con dos saltos de línea.
    *   **Previsualización del Texto Original**: `st.text_area("Texto detectado:", texto_original, ...)` muestra el texto extraído en un área de texto deshabilitada.
    *   **Botón de Humanización**: `if st.button("✨ Humanizar y Corregir Texto"):` activa el proceso de IA.
        *   `with st.spinner(...)`: Muestra un indicador de carga mientras la IA procesa.
        *   **Definición del Prompt**: Se construye un `prompt` multi-línea detallado que instruye al modelo Gemini sobre cómo debe reescribir el texto. Este prompt incluye reglas críticas para la "humanización" (variación de longitud de oraciones, conectores, mantenimiento de la información, etc.).
        *   **Invocación del Modelo**:
            *   `modelo = genai.GenerativeModel(model_name)`: Instancia el modelo Gemini con el nombre especificado.
            *   `respuesta = modelo.generate_content(prompt)`: Envía el prompt al modelo y obtiene la respuesta.
        *   **Manejo de Errores de Modelo**: Un bloque `try-except` captura errores comunes al invocar la API de Gemini (ej., clave incorrecta, modelo inválido).
        *   **Extracción del Texto Humanizado**: `texto_humanizado = getattr(respuesta, 'text', None)` extrae el texto generado de la respuesta del modelo, con lógica de fallback si la estructura de la respuesta no es la esperada.
    *   **Visualización del Resultado**: `st.text_area("Resultado:", texto_humanizado, ...)` muestra el texto procesado por la IA.
    *   **Generación y Descarga del Nuevo Word**:
        *   `doc_salida = Document()`: Crea un nuevo documento Word vacío.
        *   El `texto_humanizado` se divide en párrafos y se añade al `doc_salida`.
        *   `buffer = io.BytesIO()`: Crea un búfer en memoria.
        *   `doc_salida.save(buffer)`: Guarda el documento recién creado en el búfer.
        *   `buffer.seek(0)`: Reposiciona el puntero del búfer al inicio para la lectura.
        *   `st.download_button(...)`: Proporciona un botón para descargar el archivo Word generado, con un nombre de archivo predefinido y tipo MIME correcto.

6.  **Manejo de Errores Generales**:
    *   `except Exception as e:`: Captura cualquier excepción no manejada durante el procesamiento del archivo Word y muestra un mensaje de error al usuario.

### `humanizador.py` (Script de Generación/Ejemplo)

Este archivo es un script auxiliar cuyo único propósito es generar (escribir) el archivo `app_humanizador.py`.

1.  **`code_content = """..."""`**: Contiene una cadena de texto multi-línea que es el código fuente completo de una versión de la aplicación `app_humanizador.py`. Esta versión incrustada difiere de la `app_humanizador.py` principal en:
    *   El modelo Gemini por defecto usado (`gemini-1.5-flash` directamente en la llamada al modelo).
    *   La falta del parámetro `key` en `st.sidebar.text_input` para la API key.
    *   La falta del input para seleccionar el nombre del modelo.
    *   La adición de metadatos de autoría (`core_properties.author`, `core_properties.comments`) al documento Word de salida.
2.  **Escritura del Archivo**:
    *   `with open("app_humanizador.py", "w", encoding="utf-8") as f: f.write(code_content)`: Abre el archivo `app_humanizador.py` en modo escritura (`"w"`) y escribe todo el contenido de `code_content` en él, sobrescribiendo cualquier contenido existente.
3.  **Confirmación**:
    *   `print("Archivo creado exitosamente.")`: Muestra un mensaje en la consola confirmando que la operación se realizó.

**Propósito**: Este script podría ser utilizado para una distribución simplificada o para recrear una versión específica del archivo de la aplicación, posiblemente como base o plantilla para futuros desarrollos.

### `list_models.py` (Script de Utilidad)

Este script de consola es una herramienta para desarrolladores que desean inspeccionar qué modelos de Google Gemini están disponibles para su API Key.

1.  **Importaciones**:
    *   `google.generativeai as genai`: Para interactuar con la API de Gemini.
    *   `os`: Para acceder a variables de entorno.

2.  **Obtención de API Key**:
    *   `api_key = os.environ.get("GENAI_API_KEY")`: Intenta obtener la API Key de una variable de entorno llamada `GENAI_API_KEY`. Esta es una práctica recomendada para la seguridad.
    *   Si no la encuentra, `api_key = input("Introduce tu Gemini API Key: ").strip()` solicita al usuario que la introduzca por consola.
    *   Si no se proporciona ninguna clave, el script imprime un mensaje y sale.

3.  **Configuración de Gemini**:
    *   `genai.configure(api_key=api_key)`: Inicializa el cliente de la API con la clave obtenida.

4.  **Listado de Modelos**:
    *   `for m in genai.list_models():`: Itera sobre la lista de modelos devuelta por `genai.list_models()`.
    *   Dentro del bucle, se utiliza `getattr(m, "name", None) or ...` para extraer el nombre del modelo de varias posibles ubicaciones dentro del objeto `m`, asegurando la compatibilidad y robustez.
    *   `print(name)`: Imprime el nombre de cada modelo disponible en la consola.

## 4. Conceptos y Glosario Técnico

Aquí se explican los términos técnicos clave, algoritmos específicos o lógicas complejas utilizadas en el código.

*   **Streamlit**: Un framework de código abierto en Python que permite a los ingenieros y científicos de datos crear rápidamente aplicaciones web interactivas utilizando solo código Python. Elimina la necesidad de conocer HTML, CSS o JavaScript para desarrollar interfaces de usuario.
*   **Google Gemini API**: Es una interfaz de programación de aplicaciones que permite a los desarrolladores acceder y utilizar los modelos de IA generativa de Google (como Gemini, que es una familia de modelos multimodal) en sus propias aplicaciones. Estos modelos son capaces de comprender y generar texto, imágenes, audio y video.
*   **`python-docx`**: Una biblioteca de Python que proporciona una API para leer, escribir y modificar documentos de Microsoft Word (`.docx`). Permite manipular elementos como párrafos, encabezados, tablas, estilos, etc.
*   **`io.BytesIO`**: Una clase del módulo `io` de Python que se comporta como un archivo binario pero opera completamente en la memoria del programa. Es útil para manejar datos binarios (como documentos Word o imágenes) sin tener que leerlos o escribirlos en el disco físico, mejorando el rendimiento y la flexibilidad.
*   **API Key (Clave de API)**: Una cadena única de caracteres alfanuméricos que sirve como autenticador para que una aplicación o usuario acceda a un servicio web o API. Garantiza que solo los usuarios autorizados puedan consumir los recursos de la API y permite el seguimiento del uso.
*   **Prompt Engineering (Ingeniería de Prompts)**: Es el arte y la ciencia de diseñar, refinar y optimizar las "instrucciones" o "preguntas" (conocidas como "prompts") que se le dan a un modelo de lenguaje grande (LLM) o a cualquier modelo de IA generativa. El objetivo es guiar a la IA para que genere respuestas precisas, relevantes, coherentes y con el formato deseado. Un buen prompt es crucial para obtener resultados de alta calidad.
*   **Humanización de Texto**: En el contexto de la IA, se refiere al proceso de transformar un texto que ha sido generado por una máquina (y que por lo tanto puede sonar formal, repetitivo o artificial) en uno que suene como si hubiera sido escrito por un ser humano. Esto implica aplicar técnicas lingüísticas como variar la sintaxis, usar un vocabulario más rico y diverso, introducir conectores naturales, y adaptar el tono para que sea más conversacional y empático.
*   **Modelos de Lenguaje Grandes (LLMs - Large Language Models)**: Son tipos de modelos de IA entrenados con vastos volúmenes de datos textuales. Son capaces de comprender, generar, traducir y resumir texto, así como de responder a preguntas de una manera conversacional. Los modelos Gemini de Google son ejemplos de LLMs avanzados.
*   **`st.spinner`**: Un componente de Streamlit que muestra un indicador de carga (spinner) mientras se ejecuta un bloque de código. Mejora la experiencia de usuario al indicar que una operación está en curso y que la aplicación no está congelada.

## 5. Guía de Instalación y Ejecución

Sigue estos pasos para configurar el entorno de desarrollo, instalar las dependencias y ejecutar la aplicación.

### Requisitos Previos

*   **Python 3.8 o superior**: Asegúrate de tener una versión compatible de Python instalada en tu sistema. Puedes descargarla desde el sitio web oficial: [python.org](https://www.python.org/downloads/).
*   **Google Gemini API Key**: Necesitarás una clave de API válida para acceder a los modelos de Google Gemini. Puedes obtenerla de forma gratuita en [Google AI Studio](https://aistudio.google.com/app/apikey).

### 1. Preparar el Entorno

Es una buena práctica utilizar entornos virtuales para aislar las dependencias del proyecto.

1.  **Clonar o Descargar el Proyecto**:
    Si tienes los archivos en un repositorio Git, clónalo:
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd <nombre_del_directorio_del_proyecto>
    ```
    Si tienes los archivos sueltos, simplemente colócalos en una carpeta dedicada para el proyecto.

2.  **Crear un Entorno Virtual**:
    Abre tu terminal o línea de comandos en el directorio raíz del proyecto y ejecuta:
    ```bash
    python -m venv venv
    ```

3.  **Activar el Entorno Virtual**:
    *   **En Windows (CMD):**
        ```bash
        .\venv\Scripts\activate
        ```
    *   **En Windows (PowerShell):**
        ```powershell
        .\venv\Scripts\Activate.ps1
        ```
    *   **En macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    Verás `(venv)` al inicio de tu prompt de terminal, indicando que el entorno virtual está activo.

### 2. Instalar Dependencias del Proyecto

Con el entorno virtual activado, instala todas las librerías necesarias utilizando `pip`:

```bash
pip install streamlit google-generativeai python-docx
```

### 3. (Opcional) Listar Modelos de Gemini Disponibles

Puedes usar el script `list_models.py` para verificar qué modelos de Gemini están accesibles con tu API Key.

1.  **Configurar la API Key (recomendado)**:
    Para mayor seguridad y comodidad, puedes establecer tu API Key como una variable de entorno `GENAI_API_KEY`.
    *   **En Windows (CMD, solo para la sesión actual):**
        ```bash
        set GENAI_API_KEY=TU_API_KEY_DE_GEMINI
        ```
    *   **En Windows (PowerShell, solo para la sesión actual):**
        ```powershell
        $env:GENAI_API_KEY="TU_API_KEY_DE_GEMINI"
        ```
    *   **En macOS/Linux (solo para la sesión actual):**
        ```bash
        export GENAI_API_KEY="TU_API_KEY_DE_GEMINI"
        ```
    (Para hacerla permanente, deberías añadirla a tu perfil de usuario, como `.bashrc`, `.zshrc` o variables de entorno del sistema.)

2.  **Ejecutar el script de listado de modelos**:
    ```bash
    python list_models.py
    ```
    Si no configuraste la variable de entorno, el script te pedirá que introduzcas tu API Key directamente en la consola. Esto imprimirá una lista de los nombres de los modelos disponibles.

### 4. Ejecutar la Aplicación Principal

Finalmente, para lanzar la aplicación web "Humanizador de Word":

1.  Asegúrate de que tu entorno virtual esté activado y que todas las dependencias estén instaladas.
2.  Ejecuta el script principal de Streamlit:
    ```bash
    streamlit run app_humanizador.py
    ```

3.  Streamlit iniciará un servidor web local y abrirá automáticamente la aplicación en tu navegador predeterminado (normalmente en `http://localhost:8501`).

4.  **Uso de la Aplicación**:
    *   En la barra lateral izquierda de la aplicación, **introduce tu Gemini API Key**.
    *   (Opcional) Puedes cambiar el nombre del modelo de IA a usar en la barra lateral.
    *   Haz clic en "Elige un archivo de Word (.docx)" y selecciona el documento que deseas humanizar.
    *   Presiona el botón "✨ Humanizar y Corregir Texto".
    *   Después de que la IA procese el texto, podrás ver el resultado y descargar el nuevo archivo `.docx` humanizado.

---
**Nota sobre `humanizador.py`**: Si por alguna razón necesitas generar o recrear el archivo `app_humanizador.py` a partir del script `humanizador.py` (por ejemplo, si el archivo original no existe o deseas aplicar la versión definida en el generador), simplemente ejecuta:
```bash
python humanizador.py
```
Esto creará o sobrescribirá `app_humanizador.py` con su contenido. Luego podrás ejecutar `streamlit run app_humanizador.py` como se describe en el punto 4.
---