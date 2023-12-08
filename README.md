# SKillSetGo (Sistema de Reserva de Clases en Academia)

Este proyecto Django permite la reserva de clases en una academia.

## Requisitos

- Python 3.10 o superior
- Django 4

## Instalación

1. Clona el repositorio:

```bash
https://github.com/PGPI-2023-1-06/PGPI-G1.06.git
git checkout develop
```
2. Instala las depemdencias del proyecto
```bash
pip install -r requirements.txt
```
3. Haz las migraciones 
```bash
python manage.py makemigrations
python manage.py migrate
```
4. Ejecuta el proyecto
```bash
python manage.py runserver
```
5. Abre el navegador y dirijete `http://127.0.0.1:8000/` para acceder a la página web.


## Estructura del proyecto
El proyecto sigue la siguiente estructura:

- `SkillSetGo` Directorio base.
- `account` Gestión de usuarios y administrador.
- `payment` Gestión de pagos.
- `shop` Gestión de productos para el usuario.









   
