
truncate table paradas_complemento;

CREATE TABLE paradas_complemento
(
  linea text,
  ramal text,
  sentido text,
  clusterord double precision,
	departamento character varying(50),
	barrio character varying(50)
);

COPY paradas_complemento FROM 'E:\Pruebas\ParadasDeptosBarrios.csv' CSV  DELIMITER ';'  HEADER;

SELECT * FROM paradas_complemento;

--PEGO LAS ZONAS

ALTER TABLE PARADAS
ADD ZONA CHARACTER VARYING (10);

UPDATE PARADAS A
SET DEPARTAMENTO = B.DEPARTAMENTO, BARRIO = B.BARRIO
FROM paradas_complemento B
WHERE A.LINEA = B.LINEA
  AND A.RAMAL = B.RAMAL
  AND A.SENTIDO = B.SENTIDO
  AND A.CLUSTERORD = B.CLUSTERORD;

UPDATE PARADAS
SET BARRIO = 'NUNEZ'
WHERE BARRIO = 'NUÑEZ';

UPDATE PARADAS A
SET ZONA = (SELECT ZONA FROM DEPARTAMENTOS B WHERE A.BARRIO = B.BARRIO);

UPDATE PARADAS A
SET ZONA = (SELECT ZONA FROM DEPARTAMENTOS B WHERE A.DEPARTAMENTO = B.PARTIDO AND B.PARTIDO <> 'CAPITAL FEDERAL.')
WHERE A.BARRIO IS NULL;


/***************** correccion de nombres de zonas *********************/
UPDATE DEPARTAMENTOS SET ZONA = 'noroeste' where zona = 'nordeste';
UPDATE DEPARTAMENTOS SET ZONA = 'sudeste' where zona = 'sureste';
update paradas set zona = 'noroeste' where zona = 'nordeste';
update paradas set zona = 'noroeste' where zona = ' noroeste';
update paradas set zona = 'sudeste' where zona = 'sureste';

select * from matrizod_agregada;
update matrizod_agregada set origen_zona = 'noroeste' where origen_zona = 'nordeste'; 
update matrizod_agregada set destino_zona = 'noroeste' where destino_zona = 'nordeste'; 
update matrizod_agregada set origen_zona = 'sudeste' where origen_zona = 'sureste'; 
update matrizod_agregada set destino_zona = 'sudeste' where destino_zona = 'sureste'; 

update matrizod_agregada set origen_zona = 'noroeste' where origen_zona = ' noroeste'; 
update matrizod_agregada set destino_zona = 'noroeste' where destino_zona = ' noroeste'; 

select distinct zona from paradas; 

/************************************************************************/

select * from DEPARTAMENTOS;

select * from PARADAS WHERE DEPARTAMENTO IS NULL; -- los paradas con departamentos en null estan fuera del amba

select * from PARADAS WHERE barrio is null and DEPARTAMENTO = 'CAPITAL FEDERAL.'; -- solo son 16

select * from PARADAS WHERE barrio is not null and DEPARTAMENTO = 'CAPITAL FEDERAL.' and zona is null; -- 0, todos los barrios porteños tienen zona

