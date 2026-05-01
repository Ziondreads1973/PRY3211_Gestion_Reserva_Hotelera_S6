# Hotel Pacific Reef - Release Semana 8

Proyecto desarrollado para la asignatura **PRY3211 - Ingeniería de Software**.

## Descripción

Este repositorio contiene el **release funcional de Semana 8** del Sistema de Gestión de Reserva Hotelera para **Hotel Pacific Reef**.

El proyecto se basa en el MVP funcional construido en Semana 7 y tiene como objetivo demostrar la integración entre **front-end, back-end, base de datos SQLite, servicio web externo y endpoints JSON** en un ambiente local de prueba.

Actualmente, el sistema permite consultar disponibilidad de habitaciones, registrar reservas desde la interfaz web, crear o reutilizar clientes según el correo ingresado, calcular automáticamente los montos asociados a la reserva, visualizar las reservas registradas desde un panel administrador, consultar información climática del destino mediante un servicio web externo y exponer recursos del sistema mediante endpoints JSON.

## Tecnologías utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja Templates
- API REST externa Open-Meteo
- Endpoints JSON propios desarrollados con Flask

## Funcionalidades implementadas

- Página principal del prototipo funcional.
- Consulta de disponibilidad de habitaciones.
- Validación de fechas de entrada y salida.
- Listado de habitaciones disponibles según capacidad y disponibilidad real.
- Registro de reserva desde interfaz web.
- Búsqueda de cliente por correo electrónico.
- Creación automática de usuario cliente cuando el correo no existe.
- Creación automática de registro en tabla cliente asociado al usuario.
- Reutilización de cliente existente cuando el correo ya está registrado.
- Asociación de la reserva al `id_cliente` real.
- Cálculo automático de:
  - total de reserva;
  - abono requerido del 30%;
  - saldo pendiente.
- Confirmación de reserva con código generado.
- Confirmación visible con datos de reserva, estadía, valores y cliente asociado.
- Panel administrador para visualizar reservas registradas.
- Panel administrador con datos de cliente, correo y teléfono.
- Verificación de conexión con la base de datos mediante ruta de salud.
- Integración funcional entre interfaz, lógica back-end y base de datos SQLite.
- Integración con servicio web externo para consultar el clima del destino.
- Visualización de temperatura, viento, condición climática, código climático, fecha/hora y fuente de datos.
- Disponibilización de endpoints JSON para que otras aplicaciones puedan consultar recursos básicos del sistema.

## Funcionalidades pendientes para cierre de Semana 8

- Actualización de planilla de pruebas Semana 8.
- Actualización de DOD Semana 8.
- Elaboración de Manual de Usuario Testing.
- Consolidación final de evidencias.
- Actualización final de Trello.
- Revisión final de GitHub.
- Grabación de video demostrativo funcional.
- Grabación de presentación grupal en Teams.
- Preparación de ZIP final limpio para AVA.

## Estructura principal del proyecto

```text
PRY3211_Gestion_Reserva_Hotelera_s8/
├── app/
│   ├── app.py
│   ├── database.py
│   ├── requirements.txt
│   ├── templates/
│   └── static/
├── bd/
│   └── hotel_pacific_reef.db
├── docs/
├── dod/
├── testing/
├── evidencias/
│   ├── semana7/
│   └── semana8/
├── frontend/
├── uml/
├── videos/
├── README.md
├── .gitignore
└── enlaces_entrega_s8.txt
```
