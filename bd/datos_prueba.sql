-- =========================================================
-- Proyecto: Sistema de Gestión de Reserva Hotelera
-- Hotel: Pacific Reef
-- Archivo: datos_prueba.sql
-- Ejecutar después de schema.sql
-- =========================================================

INSERT INTO rol (id_rol, nombre, descripcion) VALUES
(1, 'Cliente', 'Usuario final que realiza reservas'),
(2, 'Administrador', 'Usuario con control operativo y administrativo'),
(3, 'Recepcionista', 'Usuario interno para apoyo operativo');

INSERT INTO usuario (
    id_usuario, id_rol, rut, nombres, apellidos, correo, contrasena, telefono, idioma, estado
) VALUES
(1, 1, '11111111-1', 'Pablo',   'Higueras', 'pablo.cliente@example.com',   'Clave1234', '56911111111', 'ES', 'Activo'),
(2, 1, '22222222-2', 'Jesus',   'Vera',     'jesus.cliente@example.com',   'Clave1234', '56922222222', 'ES', 'Activo'),
(3, 1, '33333333-3', 'Bastian', 'Carrillo', 'bastian.cliente@example.com', 'Clave1234', '56933333333', 'ES', 'Activo'),
(4, 2, '44444444-4', 'Camila',  'Soto',     'camila.admin@example.com',    'Admin1234', '56944444444', 'ES', 'Activo'),
(5, 3, '55555555-5', 'Matias',  'Rojas',    'matias.recepcion@example.com','Recep1234', '56955555555', 'ES', 'Activo');

INSERT INTO cliente (
    id_cliente, id_usuario, fecha_registro, estado_cliente
) VALUES
(1, 1, '2026-05-20', 'Activo'),
(2, 2, '2026-05-22', 'Activo'),
(3, 3, '2026-05-25', 'Activo');

INSERT INTO tipo_habitacion (
    id_tipo_habitacion, nombre, descripcion, capacidad_maxima, cantidad_camas, precio_base, estado
) VALUES
(1, 'Estandar',     'Habitacion comoda para estadias breves',           2, 1,  60000.00, 'Activa'),
(2, 'Doble',        'Habitacion para grupos pequenos o familias',       4, 2,  90000.00, 'Activa'),
(3, 'Suite Deluxe', 'Habitacion premium con vista preferencial al mar', 2, 1, 140000.00, 'Activa');

INSERT INTO habitacion (
    id_habitacion, id_tipo_habitacion, numero, piso, capacidad, descripcion, estado
) VALUES
(101, 1, '101', 1, 2, 'Habitacion estandar ubicada en el primer piso', 'Disponible'),
(102, 1, '102', 1, 2, 'Habitacion estandar ubicada en el primer piso', 'Disponible'),
(201, 2, '201', 2, 4, 'Habitacion doble ubicada en el segundo piso',   'Disponible'),
(202, 2, '202', 2, 4, 'Habitacion doble ubicada en el segundo piso',   'Disponible'),
(301, 3, '301', 3, 2, 'Suite deluxe ubicada en el tercer piso',        'Disponible');

INSERT INTO tarifa (
    id_tarifa, id_tipo_habitacion, fecha_inicio, fecha_termino, precio_noche, estado
) VALUES
(1, 1, '2026-06-01', '2026-06-30',  60000.00, 'Activa'),
(2, 2, '2026-06-01', '2026-06-30',  90000.00, 'Activa'),
(3, 3, '2026-06-01', '2026-06-30', 140000.00, 'Activa'),
(4, 3, '2026-07-01', '2026-07-31', 155000.00, 'Programada');

INSERT INTO reserva (
    id_reserva, id_cliente, id_habitacion, fecha_reserva, fecha_check_in, fecha_check_out,
    cantidad_huespedes, estado_reserva, total_reserva, abono_requerido, saldo_pendiente, codigo_reserva
) VALUES
(1, 1, 201, '2026-06-01', '2026-06-10', '2026-06-12', 2, 'Confirmada', 180000.00,  54000.00, 126000.00, 'PR-20260610-001'),
(2, 2, 301, '2026-06-02', '2026-06-15', '2026-06-18', 2, 'Pendiente',  420000.00, 126000.00, 420000.00, 'PR-20260615-002'),
(3, 3, 101, '2026-06-03', '2026-06-20', '2026-06-22', 1, 'Cancelada',  120000.00,  36000.00, 120000.00, 'PR-20260620-003');

INSERT INTO pago (
    id_pago, id_reserva, fecha_pago, monto, metodo_pago, estado_pago, referencia_pago
) VALUES
(1, 1, '2026-06-01',  54000.00, 'Tarjeta', 'Aprobado',  'TXN-OK-0001'),
(2, 2, '2026-06-02', 126000.00, 'Tarjeta', 'Rechazado', 'TXN-ERR-0002');

INSERT INTO ticket_qr (
    id_ticket, id_reserva, codigo_qr, fecha_emision, url_qr, estado
) VALUES
(1, 1, 'QR-PR-20260610-001', '2026-06-01', 'https://hotelpacificreef.example.com/qr/PR-20260610-001', 'Activo');