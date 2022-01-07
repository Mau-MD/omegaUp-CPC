# omegaUp Code Plagiarism Check

Esta es una herramienta que permite checar el plagio de código dentro de un concurso mediante la herramienta de `Moss` (WIP)

## Uso

Para poder usarlo clona este repositorio

`git clone https://github.com/Mau-MD/omegaUp-CPC.git`

Instala las dependencias

`pip install -r requirements.txt`

Y corre main

`python3 main.py`

Ingresa el nombre de usuario y constraseña con la cual entras a omegaUp, luego ingresa tu user_id de moss. Puedes obtener uno [aquí](http://theory.stanford.edu/~aiken/moss/)

_Si ingresaste mal tu usuario/contraseña, lo puedes cambiar dentro del archivo generado `login.txt`_

A continuación sigue las instrucciones.

**Solo puedes ver los concursos en los que eres admin/creador**

## Progreso

El código descarga todos los runs hechos por los usuarios de un concurso y los acomoda por carpetas, luego utiliza el servicio de `Moss` para detectar plagio (solo archivos `cpp` por el momento). Actualmente realiza el analisis a absolutamente todos los archivos sin excepciones, es decir puede que el programa marque plagio entre dos archivos que subio el mismo usuario. Se busca proximamente evitar este comportamiento
