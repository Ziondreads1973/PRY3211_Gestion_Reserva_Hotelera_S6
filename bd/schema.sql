-- =========================================================
-- Proyecto: Sistema de Gestión de Reserva Hotelera
-- Hotel: Pacific Reef
-- Archivo: schema.sql
-- =========================================================

CREATE TABLE rol (
    id_rol           INTEGER PRIMARY KEY,
    nombre           TEXT NOT NULL UNIQUE,
    descripcion      TEXT
);

CREATE TABLE usuario (
    id_usuario       INTEGER PRIMARY KEY,
    id_rol           INTEGER NOT NULL,
    rut              TEXT NOT NULL UNIQUE,
    nombres          TEXT NOT NULL,
    apellidos        TEXT NOT NULL,
    correo           TEXT NOT NULL UNIQUE,
    contrasena       TEXT NOT NULL,
    telefono         TEXT,
    idioma           TEXT NOT NULL,
    estado           TEXT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

CREATE TABLE cliente (
    id_cliente       INTEGER PRIMARY KEY,
    id_usuario       INTEGER NOT NULL UNIQUE,
    fecha_registro   TEXT NOT NULL,
    estado_cliente   TEXT NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE tipo_habitacion (
    id_tipo_habitacion  INTEGER PRIMARY KEY,
    nombre              TEXT NOT NULL UNIQUE,
    descripcion         TEXT,
    capacidad_maxima    INTEGER NOT NULL,
    cantidad_camas      INTEGER NOT NULL,
    precio_base         REAL NOT NULL,
    estado              TEXT NOT NULL
);

CREATE TABLE habitacion (
    id_habitacion       INTEGER PRIMARY KEY,
    id_tipo_habitacion  INTEGER NOT NULL,
    numero              TEXT NOT NULL UNIQUE,
    piso                INTEGER NOT NULL,
    capacidad           INTEGER NOT NULL,
    descripcion         TEXT,
    estado              TEXT NOT NULL,
    FOREIGN KEY (id_tipo_habitacion) REFERENCES tipo_habitacion(id_tipo_habitacion)
);

CREATE TABLE tarifa (
    id_tarifa           INTEGER PRIMARY KEY,
    id_tipo_habitacion  INTEGER NOT NULL,
    fecha_inicio        TEXT NOT NULL,
    fecha_termino       TEXT NOT NULL,
    precio_noche        REAL NOT NULL,
    estado              TEXT NOT NULL,
    FOREIGN KEY (id_tipo_habitacion) REFERENCES tipo_habitacion(id_tipo_habitacion)
);

CREATE TABLE reserva (
    id_reserva          INTEGER PRIMARY KEY,
    id_cliente          INTEGER NOT NULL,
    id_habitacion       INTEGER NOT NULL,
    fecha_reserva       TEXT NOT NULL,
    fecha_check_in      TEXT NOT NULL,
    fecha_check_out     TEXT NOT NULL,
    cantidad_huespedes  INTEGER NOT NULL,
    estado_reserva      TEXT NOT NULL,
    total_reserva       REAL NOT NULL,
    abono_requerido     REAL NOT NULL,
    saldo_pendiente     REAL NOT NULL,
    codigo_reserva      TEXT NOT NULL UNIQUE,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id_habitacion)
);

CREATE TABLE pago (
    id_pago             INTEGER PRIMARY KEY,
    id_reserva          INTEGER NOT NULL,
    fecha_pago          TEXT NOT NULL,
    monto               REAL NOT NULL,
    metodo_pago         TEXT NOT NULL,
    estado_pago         TEXT NOT NULL,
    referencia_pago     TEXT,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

CREATE TABLE ticket_qr (
    id_ticket           INTEGER PRIMARY KEY,
    id_reserva          INTEGER NOT NULL UNIQUE,
    codigo_qr           TEXT NOT NULL UNIQUE,
    fecha_emision       TEXT NOT NULL,
    url_qr              TEXT,
    estado              TEXT NOT NULL,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);