TL-TP
=====

Teoría de Lenguajes: Trabajo Práctico

2° Cuatrimestre 2014

Departamento de Computación,  
Facultad de Ciencias Exactas y Naturales,  
Universidad de Buenos Aires.

Alumnos
-------

Nahuel Delgado (LU 601/11) [nahueldelgado@gmail.com](mailto:nahueldelgado@gmail.com)  
Leandro Lovisolo (LU 645/11) [leandro@leandro.me](mailto:leandro@leandro.me)  
Lautaro José Petaccio (LU 443/11) [lausuper@gmail.com](mailto:lausuper@gmail.com)

Requerimientos
--------------

- Python 2.7
- Librería PLY (http://www.dabeaz.com/ply/)
- Librería Panda3D (https://www.panda3d.org/)

Modo de uso
-----------

Ejecutar `./pegv <archivo>` en el directorio raíz, reemplazando `<archivo>` por la ruta a algún archivo en formato PEGS. Ejemplo: `./pegv ejemplos/eg01.peg`.

Alternativamente proveer el código a interpretar por la entrada estándar. Ejemplo: `cat ejemplos/eg01.peg
| ./pegv`.

Opcionalmente puede imprimirse cada regla reconocida y su respectivo árbol de parsing con la opción `-p`. Ejemplo: `./pegv -p ejemplos/eg01.peg`.
