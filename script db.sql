CREATE TABLE usuario (
  id_usuario SERIAL PRIMARY KEY,
  cedula_identidad NUMERIC,
  nombre TEXT,
  primer_apellido TEXT,
  segundo_apellido TEXT,
  fecha_nacimiento DATE
);

INSERT INTO usuario (cedula_identidad, nombre, primer_apellido, segundo_apellido, fecha_nacimiento)
VALUES
  (1456789, 'Juan', 'Perez', 'Gomez', '1990-05-12'),
  (9874321, 'Maria', 'Lopez', 'Garcia', '1985-10-25'),
  (4567823, 'Pedro', 'Gonzalez', 'Sanchez', '1995-03-07'),
  (6543219, 'Ana', 'Martinez', 'Rodriguez', '1988-12-18'),
  (7946652, 'Roger', 'Mencia', 'Rojas', '1991-09-21');
