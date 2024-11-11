Explicación del Código del Proyecto Final de Métodos Númericos.

1. Revisar el archivo llamado arquitectura, con esté se entenderá de mejor manera la secuencia y modularidad del proyecto
2. Todos los archivos que están contenidos en carpetas, tienen un archivo __init__.py que permite tener como modulo a las carpetas y a los archivos contenidos en ellas.
3. Archivo main.py, en este archivo se encuentra la ejecución principal, es el que permite al código funcionar
   a. Para ejecutar el programa llamar desde consola o en VS Code esté archivo con el comando "python main.py"
4. Carpeta resources, en ella se encuentra todos los archivos gui de las interfaces
5. Carpeta utils, está carpeta tiene los cálculos bases mediante el método de diferencias finitas.
   a. Archivo H2_stress_DF.py, archivo encargado de generar las gráficas de estrés radial y tangencial mediante diferencias finitas
   b. difussionH2_stress_DF.py, archivo encargado de generar la simulación 3D para la difusión
6. Carpeta simulatios, carpeta que permite generar la simulación de difusión
   a. difussion, carpeta que contiene el archivo que genera la imagen 3D

Para poder probar el código se recomienda tener los archivos descomprimidos en el escritorio, y desde la CMD ejecutar el comando del directorio, ejemplo a continuación:
 python  C:\Users\Admin\Desktop\proyecto\main.py
     Esto es, comando python y posterior a esto la ruta del proyecto con el nombre del main.py
Recordar que el CMD se puede abrir con el comando "Windows + r" y escribir cmd

El tiempo de ejecución  y los recursos que exige el proyecto son altos

De no poder ejecutar el proyecto, recomendable visualizar el github y abrirlo en VS CODE

    Para la ejecución en VS CODE, abrir la carpeta donde está todo el proyecto, posterior a esto abrir una terminal con el comando "ctrl + ñ"
	Y posterior a esto en consola escribir el comando "python main.py"

Enlace al GitHub:https://github.com/Jdparra2004/Simulacion_Hidrogeno
