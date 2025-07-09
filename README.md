# Django APP: Modelo de optimización

Aplicación web construida con Django para resolver problemas de optimización lineal utilizando `PuLP`.

## Características

- Interfaz web para cargar parámetros del modelo mediante un archivo CSV.
- Visualización de resultados óptimos.
- Edición y eliminación de conjuntos de parámetros.
- Ejecución local sin necesidad de levantar el servidor (vía `main.py`).

---

## Requisitos

- Python 3.10+
- pip


---

## Problema a resolver

El modelo ejecutado resuelve un problema de optimización lineal de dos dimensiones bajo restricciones lineales. El caso de ejemplo corresponde a resolver el problema:

max Z = P_A x_A + P_B x_B
T_A1 x_A + T_B1 x_B ≤ T_M1
T_A2 x_A + T_B2 x_B ≤ T_M2
x_A, x_B ≥ 0

---

## Cómo instalar las dependencias y ejecutar el código

1. Instalar Python
2. Instalar virtual env y actualizar pip con la consola
```bash
pip install virtualenv
python.exe -m pip install --upgrade pip
```
3. (Opcional) Instalar Visual Studio Code y añadir paquete de extensiones "Python Extension Pack"

4.	Descargar espacio de trabajo y cargar entorno virtual
* Con consola de comandos: Abrir carpeta del espacio de trabajo (Asignar la consola a esa carpeta) y cargar entorno virtual con sus dependencias
```bash
cd ruta-espacio-de-trabajo
.\env\Scripts\activate
pip install -r requirements.txt
```
* Con Visual Studio Code:
Ctrl+Shift+P Python: Select Interpreter
```bash
pip install -r requirements.txt
```

5. Ejecutar ejemplo main.py:
```bash
python main.py
```

5. Ejecutar web:
```bash
python manage.py runserver
```

---
## Cómo ejecutar la app
Al ejecutar la web, se tiene disponible un enlace para acceder desde el navegador.

Para abrir la app, escribir acceder al "http://127.0.0.1:8000/optimizador/"

Para ejecutar la app, apretar el botón "Seleccionar archivo" y subir un archivo csv con las caracteristicas requeridas como se estipula en los ejemplos disponibles en la carpeta data.

Presionar "Ejecutar optimización" para visualizar los resultados del modelo de optimización. En caso de querer editar los parámetros, acceder a "Agregar restricciones"
