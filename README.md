# Hotel Pacific Reef - Release Semana 8

Proyecto desarrollado para la asignatura **PRY3211 - IngenierÃ­a de Software**.

## DescripciÃ³n

Este repositorio contiene el **release funcional de Semana 8** del Sistema de GestiÃ³n de Reserva Hotelera para **Hotel Pacific Reef**.

El proyecto corresponde a la Evaluación Final Transversal de Semana 9 y tiene como objetivo demostrar la integraciÃ³n entre **front-end, back-end, base de datos SQLite, servicio web externo y endpoints JSON** en un ambiente local de prueba.

Actualmente, el sistema permite consultar disponibilidad de habitaciones, registrar reservas desde la interfaz web, crear o reutilizar clientes segÃºn el correo ingresado, calcular automÃ¡ticamente los montos asociados a la reserva, visualizar las reservas registradas desde un panel administrador, consultar informaciÃ³n climÃ¡tica del destino mediante un servicio web externo y exponer recursos del sistema mediante endpoints JSON.

## TecnologÃ­as utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja Templates
- API REST externa Open-Meteo
- Endpoints JSON propios desarrollados con Flask

## Funcionalidades implementadas

- PÃ¡gina principal del prototipo funcional.
- Consulta de disponibilidad de habitaciones.
- ValidaciÃ³n de fechas de entrada y salida.
- Listado de habitaciones disponibles segÃºn capacidad y disponibilidad real.
- Registro de reserva desde interfaz web.
- BÃºsqueda de cliente por correo electrÃ³nico.
- CreaciÃ³n automÃ¡tica de usuario cliente cuando el correo no existe.
- CreaciÃ³n automÃ¡tica de registro en tabla cliente asociado al usuario.
- ReutilizaciÃ³n de cliente existente cuando el correo ya estÃ¡ registrado.
- AsociaciÃ³n de la reserva al `id_cliente` real.
- CÃ¡lculo automÃ¡tico de:
  - total de reserva;
  - abono requerido del 30%;
  - saldo pendiente.
- ConfirmaciÃ³n de reserva con cÃ³digo generado.
- ConfirmaciÃ³n visible con datos de reserva, estadÃ­a, valores y cliente asociado.
- Panel administrador para visualizar reservas registradas.
- Panel administrador con datos de cliente, correo y telÃ©fono.
- VerificaciÃ³n de conexiÃ³n con la base de datos mediante ruta de salud.
- IntegraciÃ³n funcional entre interfaz, lÃ³gica back-end y base de datos SQLite.
- IntegraciÃ³n con servicio web externo para consultar el clima del destino.
- VisualizaciÃ³n de temperatura, viento, condiciÃ³n climÃ¡tica, cÃ³digo climÃ¡tico, fecha/hora y fuente de datos.
- DisponibilizaciÃ³n de endpoints JSON para que otras aplicaciones puedan consultar recursos bÃ¡sicos del sistema.

## Funcionalidades pendientes para cierre de Semana 8

- ActualizaciÃ³n de planilla de pruebas Semana 8.
- ActualizaciÃ³n de DOD Semana 8.
- ElaboraciÃ³n de Manual de Usuario Testing.
- ConsolidaciÃ³n final de evidencias.
- ActualizaciÃ³n final de Trello.
- RevisiÃ³n final de GitHub.
- GrabaciÃ³n de video demostrativo funcional.
- GrabaciÃ³n de presentaciÃ³n grupal en Teams.
- PreparaciÃ³n de ZIP final limpio para AVA.

## Estructura principal del proyecto

```text
PRY3211_Gestion_Reserva_Hotelera_s8/
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ app.py
â”‚   â”œâ”€â”€ database.py
â”‚   â”œâ”€â”€ requirements.txt
â”‚   â”œâ”€â”€ templates/
â”‚   â””â”€â”€ static/
â”œâ”€â”€ bd/
â”‚   â””â”€â”€ hotel_pacific_reef.db
â”œâ”€â”€ docs/
â”œâ”€â”€ dod/
â”œâ”€â”€ testing/
â”œâ”€â”€ evidencias/
â”‚   â”œâ”€â”€ semana7/
â”‚   â””â”€â”€ semana8/
â”œâ”€â”€ frontend/
â”œâ”€â”€ uml/
â”œâ”€â”€ videos/
â”œâ”€â”€ README.md
â”œâ”€â”€ .gitignore
â””â”€â”€ enlaces_entrega_s8.txt
```

