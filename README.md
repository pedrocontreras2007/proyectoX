# Proyecto Creador de Recorridos de Buses

Este proyecto es una aplicación de escritorio que permite gestionar la creación y visualización de rutas de buses. Utiliza una interfaz gráfica construida con Tkinter y permite a los usuarios agregar paradas, crear rutas y gestionar una flota de buses.

## Estructura del Proyecto

- **src/RecorridoBuses.py**: Contiene la clase `CreadorRecorridosBuses`, que gestiona la creación y visualización de rutas de buses. Incluye métodos para cargar y guardar datos en un archivo JSON, así como para crear y gestionar rutas y buses a través de una interfaz gráfica.

- **data/datos_buses.json**: Archivo JSON que almacena los datos de las rutas y buses. Se utiliza para cargar y guardar la información de manera persistente.

- **tests/test_recorridos.py**: Contiene pruebas unitarias para verificar el funcionamiento de las funcionalidades implementadas en `RecorridoBuses.py`. Asegura que las rutas y buses se gestionen correctamente.

- **.gitignore**: Especifica qué archivos o directorios deben ser ignorados por Git, evitando que se suban al repositorio.

- **requirements.txt**: Lista las dependencias necesarias para el proyecto, permitiendo instalar los paquetes requeridos mediante un gestor de paquetes como pip.

- **README.md**: Este archivo contiene la documentación del proyecto, incluyendo una descripción del mismo, instrucciones de instalación y uso.

- **LICENSE**: Contiene la licencia bajo la cual se distribuye el proyecto, especificando los términos de uso y distribución.

## Instalación

1. Clona el repositorio en tu máquina local:
   ```
   git clone <URL del repositorio>
   ```

2. Navega al directorio del proyecto:
   ```
   cd proyectoX
   ```

3. Instala las dependencias necesarias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la aplicación, simplemente ejecuta el archivo `RecorridoBuses.py`:
```
python src/RecorridoBuses.py
```

## Contribuciones

Las contribuciones son bienvenidas. Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia [nombre de la licencia]. Consulta el archivo LICENSE para más detalles.