CREATE TABLE departamentos
(
  partido         			character varying(30),
  barrio         				character varying(30),
  zona         				character varying(30)
);

SET datestyle = "ISO, DMY";

COPY departamentos FROM 'E:\pruebas\ZonasIntrapuba.csv' CSV  DELIMITER ';'  HEADER;

SELECT * FROM DEPARTAMENTOS;

TRUNCATE TABLE DEPARTAMENTOS;
