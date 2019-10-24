truncate table the_viajesmayo_cruce;

CREATE TABLE the_viajesmayo_cruce
(
	clave1 character varying(20),
	clave2 character varying(20),
	nrotarjetaexterno character varying(16),
  codigotrxtarjeta numeric,
  codigolinea numeric,
  ramal character varying(5),
  fechatrx timestamp without time zone,
  file_id numeric,
  c_control_point1 numeric,
  distancia numeric,
  sentido character varying(2)
);

CREATE TABLE the_viajesmayo_cruce2
(
	clave1 character varying(20),
	clave2 character varying(20),
	nrotarjetaexterno character varying(16),
  codigotrxtarjeta numeric,
  codigolinea numeric,
  ramal character varying(5),
  fechatrx timestamp without time zone,
  file_id numeric,
  c_control_point1 numeric,
  distancia numeric,
  sentido character varying(2)
);

CREATE TABLE the_viajesmayo_cruce3
(
	clave1 character varying(20),
	clave2 character varying(20),
	nrotarjetaexterno character varying(16),
  codigotrxtarjeta numeric,
  codigolinea numeric,
  ramal character varying(5),
  fechatrx timestamp without time zone,
  file_id numeric,
  c_control_point1 numeric,
  distancia numeric,
  sentido character varying(2)
);

CREATE TABLE the_viajesmayo_cruce4
(
	clave1 character varying(20),
	clave2 character varying(20),
	nrotarjetaexterno character varying(16),
  codigotrxtarjeta numeric,
  codigolinea numeric,
  ramal character varying(5),
  fechatrx timestamp without time zone,
  file_id numeric,
  c_control_point1 numeric,
  distancia numeric,
  sentido character varying(2)
);

CREATE TABLE the_viajesmayo_cruce5
(
	clave1 character varying(20),
	clave2 character varying(20),
	nrotarjetaexterno character varying(16),
  codigotrxtarjeta numeric,
  codigolinea numeric,
  ramal character varying(5),
  fechatrx timestamp without time zone,
  file_id numeric,
  c_control_point1 numeric,
  distancia numeric,
  sentido character varying(2)
);

CREATE TABLE the_viajesmayo_cruce6
(
	clave1 character varying(20),
	clave2 character varying(20),
	nrotarjetaexterno character varying(16),
  codigotrxtarjeta numeric,
  codigolinea numeric,
  ramal character varying(5),
  fechatrx timestamp without time zone,
  file_id numeric,
  c_control_point1 numeric,
  distancia numeric,
  sentido character varying(2)
);

CREATE TABLE the_viajesmayo_cruce7
(
	clave1 character varying(20),
	clave2 character varying(20),
	nrotarjetaexterno character varying(16),
  codigotrxtarjeta numeric,
  codigolinea numeric,
  ramal character varying(5),
  fechatrx timestamp without time zone,
  file_id numeric,
  c_control_point1 numeric,
  distancia numeric,
  sentido character varying(2)
);

CREATE TABLE the_viajesmayo_cruce8
(
	clave1 character varying(20),
	clave2 character varying(20),
	nrotarjetaexterno character varying(16),
  codigotrxtarjeta numeric,
  codigolinea numeric,
  ramal character varying(5),
  fechatrx timestamp without time zone,
  file_id numeric,
  c_control_point1 numeric,
  distancia numeric,
  sentido character varying(2)
);

SET datestyle = "ISO, DMY";

COPY the_viajesmayo_cruce (clave1, clave2,  nrotarjetaexterno, codigotrxtarjeta ,  codigolinea ,  ramal  ,  fechatrx    ,  file_id ,  c_control_point1 ,  distancia ,  sentido  ) 
FROM 'E:\pruebas\PROYECVIAJES20150501.CSV' CSV  DELIMITER ';'  HEADER;

COPY the_viajesmayo_cruce2 (clave1, clave2,  nrotarjetaexterno, codigotrxtarjeta ,  codigolinea ,  ramal  ,  fechatrx    ,  file_id ,  c_control_point1 ,  distancia ,  sentido  ) 
FROM 'E:\pruebas\PROYECVIAJES20150502.CSV' CSV  DELIMITER ';'  HEADER;

COPY the_viajesmayo_cruce3 (clave1, clave2,  nrotarjetaexterno, codigotrxtarjeta ,  codigolinea ,  ramal  ,  fechatrx    ,  file_id ,  c_control_point1 ,  distancia ,  sentido  ) 
FROM 'E:\pruebas\PROYECVIAJES20150503.CSV' CSV  DELIMITER ';'  HEADER;

COPY the_viajesmayo_cruce4 (clave1, clave2,  nrotarjetaexterno, codigotrxtarjeta ,  codigolinea ,  ramal  ,  fechatrx    ,  file_id ,  c_control_point1 ,  distancia ,  sentido  ) 
FROM 'E:\pruebas\PROYECVIAJES20150504.CSV' CSV  DELIMITER ';'  HEADER;

COPY the_viajesmayo_cruce5 (clave1, clave2,  nrotarjetaexterno, codigotrxtarjeta ,  codigolinea ,  ramal  ,  fechatrx    ,  file_id ,  c_control_point1 ,  distancia ,  sentido  ) 
FROM 'E:\pruebas\PROYECVIAJES20150505.CSV' CSV  DELIMITER ';'  HEADER;

COPY the_viajesmayo_cruce6 (clave1, clave2,  nrotarjetaexterno, codigotrxtarjeta ,  codigolinea ,  ramal  ,  fechatrx    ,  file_id ,  c_control_point1 ,  distancia ,  sentido  ) 
FROM 'E:\pruebas\PROYECVIAJES20150506.CSV' CSV  DELIMITER ';'  HEADER;

COPY the_viajesmayo_cruce7 (clave1, clave2,  nrotarjetaexterno, codigotrxtarjeta ,  codigolinea ,  ramal  ,  fechatrx    ,  file_id ,  c_control_point1 ,  distancia ,  sentido  ) 
FROM 'E:\pruebas\PROYECVIAJES20150507.CSV' CSV  DELIMITER ';'  HEADER;

COPY the_viajesmayo_cruce8 (clave1, clave2,  nrotarjetaexterno, codigotrxtarjeta ,  codigolinea ,  ramal  ,  fechatrx    ,  file_id ,  c_control_point1 ,  distancia ,  sentido  ) 
FROM 'E:\pruebas\PROYECVIAJES20150508.CSV' CSV  DELIMITER ';'  HEADER;

ALTER TABLE the_viajesmayo_cruce
ADD paradaorigen NUMERIC;

ALTER TABLE the_viajesmayo_cruce2
ADD paradaorigen NUMERIC;

ALTER TABLE the_viajesmayo_cruce3
ADD paradaorigen NUMERIC;

ALTER TABLE the_viajesmayo_cruce4
ADD paradaorigen NUMERIC;

ALTER TABLE the_viajesmayo_cruce5
ADD paradaorigen NUMERIC;

ALTER TABLE the_viajesmayo_cruce6
ADD paradaorigen NUMERIC;

ALTER TABLE the_viajesmayo_cruce7
ADD paradaorigen NUMERIC;

ALTER TABLE the_viajesmayo_cruce8
ADD paradaorigen NUMERIC;

UPDATE the_viajesmayo_cruce A
SET paradaorigen = clusterord
FROM PARADAS B
WHERE  A.CODIGOLINEA = CAST(B.LINEA AS NUMERIC)
  AND A.RAMAL = B.RAMAL
  AND A.SENTIDO = B.SENTIDO
  AND A.DISTANCIA >= B.LIMITEINF
  AND A.DISTANCIA < B.LIMITESUP ;
  
UPDATE the_viajesmayo_cruce2 A
SET paradaorigen = clusterord
FROM PARADAS B
WHERE  A.CODIGOLINEA = CAST(B.LINEA AS NUMERIC)
  AND A.RAMAL = B.RAMAL
  AND A.SENTIDO = B.SENTIDO
  AND A.DISTANCIA >= B.LIMITEINF
  AND A.DISTANCIA < B.LIMITESUP ;

UPDATE the_viajesmayo_cruce3 A
SET paradaorigen = clusterord
FROM PARADAS B
WHERE  A.CODIGOLINEA = CAST(B.LINEA AS NUMERIC)
  AND A.RAMAL = B.RAMAL
  AND A.SENTIDO = B.SENTIDO
  AND A.DISTANCIA >= B.LIMITEINF
  AND A.DISTANCIA < B.LIMITESUP ;

UPDATE the_viajesmayo_cruce4 A
SET paradaorigen = clusterord
FROM PARADAS B
WHERE  A.CODIGOLINEA = CAST(B.LINEA AS NUMERIC)
  AND A.RAMAL = B.RAMAL
  AND A.SENTIDO = B.SENTIDO
  AND A.DISTANCIA >= B.LIMITEINF
  AND A.DISTANCIA < B.LIMITESUP ;

UPDATE the_viajesmayo_cruce5 A
SET paradaorigen = clusterord
FROM PARADAS B
WHERE  A.CODIGOLINEA = CAST(B.LINEA AS NUMERIC)
  AND A.RAMAL = B.RAMAL
  AND A.SENTIDO = B.SENTIDO
  AND A.DISTANCIA >= B.LIMITEINF
  AND A.DISTANCIA < B.LIMITESUP ;

UPDATE the_viajesmayo_cruce6 A
SET paradaorigen = clusterord
FROM PARADAS B
WHERE  A.CODIGOLINEA = CAST(B.LINEA AS NUMERIC)
  AND A.RAMAL = B.RAMAL
  AND A.SENTIDO = B.SENTIDO
  AND A.DISTANCIA >= B.LIMITEINF
  AND A.DISTANCIA < B.LIMITESUP ;

UPDATE the_viajesmayo_cruce7 A
SET paradaorigen = clusterord
FROM PARADAS B
WHERE  A.CODIGOLINEA = CAST(B.LINEA AS NUMERIC)
  AND A.RAMAL = B.RAMAL
  AND A.SENTIDO = B.SENTIDO
  AND A.DISTANCIA >= B.LIMITEINF
  AND A.DISTANCIA < B.LIMITESUP ;

UPDATE the_viajesmayo_cruce8 A
SET paradaorigen = clusterord
FROM PARADAS B
WHERE  A.CODIGOLINEA = CAST(B.LINEA AS NUMERIC)
  AND A.RAMAL = B.RAMAL
  AND A.SENTIDO = B.SENTIDO
  AND A.DISTANCIA >= B.LIMITEINF
  AND A.DISTANCIA < B.LIMITESUP ;

ALTER TABLE the_viajesmayo_cruce
ADD paradadestin NUMERIC,
add			procesado character varying(5);

ALTER TABLE the_viajesmayo_cruce2
ADD paradadestin NUMERIC,
add	procesado character varying(5);

ALTER TABLE the_viajesmayo_cruce3
ADD paradadestin NUMERIC,
add	procesado character varying(5);

ALTER TABLE the_viajesmayo_cruce4
ADD paradadestin NUMERIC,
add	procesado character varying(5);

ALTER TABLE the_viajesmayo_cruce5
ADD paradadestin NUMERIC,
add	procesado character varying(5);

ALTER TABLE the_viajesmayo_cruce6
ADD paradadestin NUMERIC,
add	procesado character varying(5);

ALTER TABLE the_viajesmayo_cruce7
ADD paradadestin NUMERIC,
add	procesado character varying(5);

ALTER TABLE the_viajesmayo_cruce8
ADD paradadestin NUMERIC,
add	procesado character varying(5);

create index the_viajesmayo_cruce_idx1
on the_viajesmayo_cruce(nrotarjetaexterno);

create index the_viajesmayo_cruce2_idx1
on the_viajesmayo_cruce2(nrotarjetaexterno);

create index the_viajesmayo_cruce3_idx1
on the_viajesmayo_cruce3(nrotarjetaexterno);

create index the_viajesmayo_cruce4_idx1
on the_viajesmayo_cruce4(nrotarjetaexterno);

create index the_viajesmayo_cruce5_idx1
on the_viajesmayo_cruce5(nrotarjetaexterno);

create index the_viajesmayo_cruce6_idx1
on the_viajesmayo_cruce6(nrotarjetaexterno);

create index the_viajesmayo_cruce7_idx1
on the_viajesmayo_cruce7(nrotarjetaexterno);

create index the_viajesmayo_cruce8_idx1
on the_viajesmayo_cruce8(nrotarjetaexterno);

SELECT count(*) from  the_viajesmayo_cruce ;where procesado is not null;
SELECT count(*) from  the_viajesmayo_cruce2 where procesado is not null;
SELECT count(*) from  the_viajesmayo_cruce3 where procesado is not null;
SELECT count(*) from  the_viajesmayo_cruce4 where procesado is not null;
SELECT count(*) from  the_viajesmayo_cruce5 where procesado is not null;
SELECT count(*) from  the_viajesmayo_cruce6 where procesado is not null;
SELECT count(*) from  the_viajesmayo_cruce7 where procesado is not null;
SELECT count(*) from  the_viajesmayo_cruce8 where procesado is not null;
