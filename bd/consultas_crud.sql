-- =========================================================
-- Proyecto: Sistema de Gestión de Reserva Hotelera
-- Hotel: Pacific Reef
-- Archivo: consultas_crud.sql
-- Objetivo: evidenciar operaciones CRUD mínimas
-- =========================================================

-- =========================================================
-- CRUD 1: CLIENTES
-- =========================================================

-- CREATE: crear nuevo usuario cliente
INSERT INTO usuario (
    id_usuario, id_rol, rut, nombres, apellidos, correo, contrasena, telefono, idioma, estado
) VALUES
(6, 1, '66666666-6', 'Valentina', 'Munoz', 'valentina.cliente@example.com', 'Clave1234', '56966666666', 'ES', 'Activo');

INSERT INTO cliente (
    id_cliente, id_usuario, fecha_registro, estado_cliente
) VALUES
(4, 6, '2026-06-05', 'Activo');

-- READ: consultar cliente creado
SELECT
    c.id_cliente,
    u.nombres,
    u.apellidos,
    u.correo,
    u.telefono,
    c.estado_cliente
FROM cliente c
JOIN usuario u ON c.id_usuario = u.id_usuario
WHERE c.id_cliente = 4;

-- UPDATE: actualizar telefono y estado del cliente
UPDATE usuario
SET telefono = '56999999999'
WHERE id_usuario = 6;

UPDATE cliente
SET estado_cliente = 'Inactivo'
WHERE id_cliente = 4;

-- READ final: verificar resultado
SELECT
    c.id_cliente,
    u.nombres,
    u.apellidos,
    u.correo,
    u.telefono,
    c.estado_cliente
FROM cliente c
JOIN usuario u ON c.id_usuario = u.id_usuario
WHERE c.id_cliente = 4;


-- =========================================================
-- CRUD 2: RESERVAS
-- =========================================================

-- CREATE: registrar nueva reserva
INSERT INTO reserva (
    id_reserva, id_cliente, id_habitacion, fecha_reserva, fecha_check_in, fecha_check_out,
    cantidad_huespedes, estado_reserva, total_reserva, abono_requerido, saldo_pendiente, codigo_reserva
) VALUES
(4, 1, 102, '2026-06-05', '2026-06-25', '2026-06-27', 2, 'Pendiente', 120000.00, 36000.00, 120000.00, 'PR-20260625-004');

-- READ: consultar reserva por codigo
SELECT
    id_reserva,
    codigo_reserva,
    fecha_check_in,
    fecha_check_out,
    cantidad_huespedes,
    estado_reserva,
    total_reserva,
    abono_requerido,
    saldo_pendiente
FROM reserva
WHERE codigo_reserva = 'PR-20260625-004';

-- UPDATE: confirmar reserva y actualizar saldo
UPDATE reserva
SET estado_reserva = 'Confirmada',
    saldo_pendiente = 84000.00
WHERE id_reserva = 4;

-- DELETE logico: cancelar reserva
UPDATE reserva
SET estado_reserva = 'Cancelada'
WHERE id_reserva = 4;

-- READ final: verificar resultado
SELECT
    id_reserva,
    codigo_reserva,
    estado_reserva,
    saldo_pendiente
FROM reserva
WHERE id_reserva = 4;


-- =========================================================
-- CRUD 3: TARIFAS
-- =========================================================

-- CREATE: crear nueva tarifa
INSERT INTO tarifa (
    id_tarifa, id_tipo_habitacion, fecha_inicio, fecha_termino, precio_noche, estado
) VALUES
(5, 2, '2026-08-01', '2026-08-31', 95000.00, 'Activa');

-- READ: consultar tarifa creada
SELECT
    id_tarifa,
    id_tipo_habitacion,
    fecha_inicio,
    fecha_termino,
    precio_noche,
    estado
FROM tarifa
WHERE id_tarifa = 5;

-- UPDATE: actualizar precio
UPDATE tarifa
SET precio_noche = 98000.00
WHERE id_tarifa = 5;

-- DELETE logico: desactivar tarifa
UPDATE tarifa
SET estado = 'Inactiva'
WHERE id_tarifa = 5;

-- READ final: verificar resultado
SELECT
    id_tarifa,
    id_tipo_habitacion,
    precio_noche,
    estado
FROM tarifa
WHERE id_tarifa = 5;