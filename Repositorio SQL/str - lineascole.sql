

////////////////////////////////////////////////////////////////////////////////
////////////// THE RAMALES //////////////////////////////////////////////////////

CREATE TABLE THE_RAMALES
(
  LINEA           CHARACTER varying(50),
  RAMAL           CHARACTER varying(5),
  DESCRIPCION     CHARACTER varying(35),
  ID_EMPRESA      NUMERIC(10),
  CODIGOLINEA     NUMERIC(10),
  AREAGEOGRAFICA  NUMERIC(2),
  CANTIDAD_TRX    NUMERIC
);

alter table the_ramales
add linea2 character varying(50);

update the_ramales
set linea2 =  TRIM(TO_CHAR(CASE WHEN substring(LINEA FROM '[0-9]*') != '' THEN TO_NUMBER(substring(LINEA FROM '[0-9]*'),'999') END,'999'));

COPY THE_RAMALES FROM 'E:\pruebas\THERAMALES.CSV' CSV  DELIMITER ';'  HEADER;


////////////////////////////////////////////////////////////////////////////////
////////////// LINEASCOLE //////////////////////////////////////////////////////
LINEASCOLE -- TABLA QUE CONTIENE TODAS LAS LINEAS / RAMAL DEL ARCHIVO GEOGRÁFICO

CREATE TABLE lineascole
(
  first_idno bigint,
  idruta bigint,
  linea text,
  linearamal text,
  ramal text,
  route_id bigint,
  route_name text,
  sentido text,
  geom text
);

ALTER TABLE lineascole
ADD BAJA int;

select CASE WHEN substring(LINEA FROM '[0-9]*') != '' THEN TO_NUMBER(substring(LINEA FROM '[0-9]*'),'999') END linea2, LINEA, ramal, sentido, geom 
from lineascole 
order by linea, ramal, sentido;


SELECT distinct trim(to_char(CASE WHEN substring(LINEA FROM '[0-9]*') != '' THEN TO_NUMBER(substring(LINEA FROM '[0-9]*'),'999') END, '999'))
FROM lineascole a left join
	   (select lineageo from distancias group by lineageo) b
on trim(to_char(CASE WHEN substring(a.LINEA FROM '[0-9]*') != '' THEN TO_NUMBER(substring(a.LINEA FROM '[0-9]*'),'999') END, '999')) = b.lineageo
where b.lineageo is null;


///////////////////////////////////////////////////////////////////////////////////////
//// depuracion de lineas cole

--primero elimino todas las lineas que pueden tener un solo recorrido o mas de dos.
--solo queremos rutas que tengan ida i vuleta


--vamos a mrcarlos como baja
UPDATE lineascole 
set baja = 1
WHERE linea || '-' || ramal IN 
																(
																	SELECT linea || '-' || ramal
																	from lineascole
																	group by linea || '-' || ramal 
																	having count(*) = 1
																);
																

UPDATE lineascole 
set baja = 1
WHERE linea || '-' || ramal IN 
																(
																	SELECT linea || '-' || ramal
																	from lineascole
																	group by linea || '-' || ramal 
																	having count(*) > 2
																);
																
UPDATE lineascole 
set baja = 1
WHERE linea || '-' || ramal || '-' || sentido IN 
																(
																	SELECT linea || '-' || ramal || '-' || sentido
																	from lineascole
																	group by linea || '-' || ramal || '-' || sentido
																	having count(*) > 1
																);


SELECT * FROM lineascole where linea = '180';

///////////////////////////////////////////////////////////////////////////////////////
//// generacion de linea2;

ALTER TABLE lineascole
add linea2 character varying(50);

UPDATE lineascole
SET LINEA2 = trim(to_char(CASE WHEN substring(LINEA FROM '[0-9]*') != '' THEN TO_NUMBER(substring(LINEA FROM '[0-9]*'),'999') END, '999'));

select * from lineascole;
