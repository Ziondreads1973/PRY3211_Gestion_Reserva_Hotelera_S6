# Hotel Pacific Reef - Release Semana 8

Proyecto desarrollado para la asignatura **PRY3211 - Ingeniería de Software**.

## Descripción

Este repositorio contiene el **release funcional de Semana 8** del Sistema de Gestión de Reserva Hotelera para **Hotel Pacific Reef**.

El proyecto se basa en el MVP funcional construido en Semana 7 y tiene como objetivo demostrar la integración entre **front-end, back-end y base de datos SQLite** en un ambiente de prueba.

Actualmente, el sistema permite consultar disponibilidad de habitaciones, registrar reservas desde la interfaz web, calcular automáticamente los montos asociados a la reserva y visualizar las reservas registradas desde un panel administrador.

## Tecnologías utilizadas

- Python
- Flask
- SQLite
- HTML
- CSS
- Jinja Templates

## Funcionalidades implementadas

- Página principal del prototipo funcional.
- Consulta de disponibilidad de habitaciones.
- Validación de fechas de entrada y salida.
- Listado de habitaciones disponibles.
- Registro básico de reserva desde interfaz web.
- Cálculo automático de:
  - total de reserva;
  - abono requerido del 30%;
  - saldo pendiente.
- Confirmación de reserva con código generado.
- Panel administrador para visualizar reservas registradas.
- Verificación de conexión con la base de datos mediante ruta de salud.
- Integración funcional entre interfaz, lógica back-end y base de datos SQLite.

## Funcionalidades planificadas para Semana 8

- Integración con servicio web externo.
- Disponibilización de endpoints JSON para consumo de recursos por otras aplicaciones.
- Mejoras en el registro de cliente asociado a la reserva.
- Actualización de planilla de pruebas Semana 8.
- Actualización de DOD Semana 8.
- Elaboración de Manual de Usuario Testing.
- Consolidación de evidencias, GitHub, Trello y videos demostrativos.

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
