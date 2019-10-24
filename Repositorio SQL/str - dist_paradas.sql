select count(*) from (select linea, ramal, sentido from paradas group by linea, ramal, sentido) a; 
--392

select count(*) from (SELECT linea_origen, ramal_origen, sentido_origen FROM dist_paradas group by  linea_origen, ramal_origen, sentido_origen) a;
--91 

SELECT linea_origen, ramal_origen, sentido_origen, avg(distancia_metros) FROM dist_paradas group by  linea_origen, ramal_origen, sentido_origen order by 1,2,3;

select count(*) from dist_paradas;

select * from dist_paradas;

select count(*) from (SELECT linea_origen, ramal_origen, sentido_origen FROM dist_paradas group by  linea_origen, ramal_origen, sentido_origen order by linea_origen, ramal_origen, sentido_origen) a;
--392

--drop table dist_paradas;
;
TRUNCATE TABLE dist_paradas;

CREATE TABLE dist_paradas
(
  linea_origen text,
  ramal_origen text,
  sentido_origen text,
  parada_origen numeric,
  linea_destino text,
  ramal_destino text,
  sentido_destino text,
  parada_destino numeric,
  distancia_grados double precision,
  distancia_metros double precision
);

CREATE INDEX DIST_PARADAS_IDX1 ON DIST_PARADAS 
(LINEA_ORIGEN, RAMAL_ORIGEN, SENTIDO_ORIGEN, PARADA_ORIGEN, LINEA_DESTINO, RAMAL_DESTINO, SENTIDO_DESTINO);


SELECT DISTINCT linea, ramal, sentido FROM PARADAS ORDER BY LINEA, RAMAL, SENTIDO;

SELECT count(*) FROM PARADAS ;


ALTER TABLE dist_paradas
ADD parada_destino NUMERIC;

DROP INDEX  dist_paradas_idx1;

CREATE INDEX dist_paradas_idx1
  ON dist_paradas
  USING btree
  (linea_origen COLLATE pg_catalog."default", ramal_origen COLLATE pg_catalog."default", sentido_origen COLLATE pg_catalog."default", parada_origen);



select count(*) from paradas;

select count(*) from dist_paradas;

select * from dist_paradas order by linea_origen, ramal_origen, sentido_origen, parada_origen, linea_destino, ramal_destino, sentido_destino;

select * from dist_paradas 
where linea_origen = '100' and linea_destino = '100'
order by linea_origen, ramal_origen, sentido_origen, parada_origen, linea_destino, ramal_destino, sentido_destino;

select * from dist_paradas A WHERE  A.LINEA_ORIGEN = '100' AND A.RAMAL_ORIGEN = '202' AND A.SENTIDO_ORIGEN = 'I';

SELECT LINEA_ORIGEN, RAMAL_ORIGEN, SENTIDO_ORIGEN, PARADA_ORIDEN, LINEA_DESTINO, RAMAL_DESTINO, SENTIDO_DESTINO, PARADA_DESTINO, 
	(ST_DISTANCE( 
				ST_Transform(
						ST_GEOMFROMTEXT('POINT (' || P1LONGITUD || ' ' || P1LATITUD || ')',4326), 22182)
						, 
				ST_Transform(
						ST_GEOMFROMTEXT('POINT (' || P2LONGITUD || ' ' || P2LATITUD || ')',4326), 22182)
						) ) distancia
FROM (
	SELECT P1.LINEA LINEA_ORIGEN, P1.RAMAL RAMAL_ORIGEN, P1.SENTIDO SENTIDO_ORIGEN, P1.CLUSTERORD PARADA_ORIDEN, P2.LINEA  LINEA_DESTINO, P2.RAMAL RAMAL_DESTINO, P2.SENTIDO SENTIDO_DESTINO, P2.CLUSTERORD PARADA_DESTINO,
				 P1.LONGITUD P1LONGITUD, P1.LATITUD P1LATITUD, P2.LONGITUD P2LONGITUD, P2.LATITUD P2LATITUD,
				(ST_DISTANCE(ST_GEOMFROMTEXT('POINT (' || P1.LONGITUD || ' ' || P1.LATITUD || ')',4326), ST_GEOMFROMTEXT('POINT (' || P2.LONGITUD || ' ' || P2.LATITUD || ')',4326) ) )  DIST,
				 MIN(ST_DISTANCE(ST_GEOMFROMTEXT('POINT (' || P1.LONGITUD || ' ' || P1.LATITUD || ')',4326), ST_GEOMFROMTEXT('POINT (' || P2.LONGITUD || ' ' || P2.LATITUD || ')',4326) ) ) OVER (PARTITION BY  P1.LINEA, P1.RAMAL, P1.SENTIDO, P1.CLUSTERORD)  MINDIST
	 FROM PARADAS P1, PARADAS P2 
	 WHERE (LPAD(P1.LINEA, 5, '0') || LPAD(P1.RAMAL,5,'0') || P1.SENTIDO) <> (LPAD(P2.LINEA, 5, '0') || LPAD(P2.RAMAL,5,'0') || P2.SENTIDO) 
	 	AND P1.LINEA = '100' AND P1.RAMAL = '202' AND P1.SENTIDO = 'I' 
	) A
WHERE DIST = MINDIST	;

22182;






select * from THE_VIAJESMAYO ORDER BY NROTARJETAEXTERNO, CODIGOTRXTARJETA;

select * from paradas order by linea, ramal, sentido, clusterord;

select count(distinct linea || ramal) from paradas;
--202

--truncate table paradas;

select count(distinct linea || ramal) from paradas order by linea, ramal, sentido, clusterord;


select count(*) from paradas;

CREATE EXTENSION postgis;

select p1.linea, p1.ramal, p1.sentido, p1.clusterord, p2.linea, p2.ramal, p2.sentido, p2.clusterord, ST_Distance(ST_GeomFromText('POINT (' || p1.longitud || ' ' || p1.latitud || ')',4326), ST_GeomFromText('POINT (' || p2.longitud || ' ' || p2.latitud || ')',4326) ) 
from paradas p1, paradas p2
where (lpad(p1.linea, 5, '0') || lpad(p1.ramal,5,'0') || p1.sentido) =  (lpad(p2.linea, 5, '0') || lpad(p2.ramal,5,'0') || p2.sentido)
  and p1.clusterord <> p2.clusterord
order by p1.linea, p1.ramal, p1.sentido, p1.clusterord, p2.linea, p2.ramal, p2.sentido, p2.clusterord;


SELECT DISTINCT LINEA, RAMAL, SENTIDO FROM PARADAS ORDER BY LINEA, RAMAL, SENTIDO;

CREATE TABLE dist_paradas as
select p1.linea linea_origen, p1.ramal ramal_origen, p1.sentido sentido_origen, p1.clusterord parada_oriden, p2.linea  linea_destino, p2.ramal ramal_destino, p2.sentido sentido_destino,  
			 MIN(ST_Distance(ST_GeomFromText('POINT (' || p1.longitud || ' ' || p1.latitud || ')',4326), ST_GeomFromText('POINT (' || p2.longitud || ' ' || p2.latitud || ')',4326) ) )
from paradas p1, paradas p2
where (lpad(p1.linea, 5, '0') || lpad(p1.ramal,5,'0') || p1.sentido) <> (lpad(p2.linea, 5, '0') || lpad(p2.ramal,5,'0') || p2.sentido)
	--and p1.linea = '100' and p1.ramal = '202' and p1.sentido = 'I'
group by p1.linea, p1.ramal, p1.sentido, p1.clusterord, p2.linea, p2.ramal, p2.sentido;

--truncate table dist_paradas;

CREATE TABLE DIST_PARADAS AS
SELECT P1.LINEA LINEA_ORIGEN, P1.RAMAL RAMAL_ORIGEN, P1.SENTIDO SENTIDO_ORIGEN, P1.CLUSTERORD PARADA_ORIDEN, P2.LINEA  LINEA_DESTINO, P2.RAMAL RAMAL_DESTINO, P2.SENTIDO SENTIDO_DESTINO,  
			 MIN(ST_DISTANCE(ST_GEOMFROMTEXT('POINT (' || P1.LONGITUD || ' ' || P1.LATITUD || ')',4326), ST_GEOMFROMTEXT('POINT (' || P2.LONGITUD || ' ' || P2.LATITUD || ')',4326) ) ) distancia_grados
FROM PARADAS P1, PARADAS P2
WHERE (LPAD(P1.LINEA, 5, '0') || LPAD(P1.RAMAL,5,'0') || P1.SENTIDO) <> (LPAD(P2.LINEA, 5, '0') || LPAD(P2.RAMAL,5,'0') || P2.SENTIDO)
	AND P1.LINEA = '100' AND P1.RAMAL = '202' AND P1.SENTIDO = 'I'
GROUP BY P1.LINEA, P1.RAMAL, P1.SENTIDO, P1.CLUSTERORD, P2.LINEA, P2.RAMAL, P2.SENTIDO;

SELECT count(*) FROM DIST_PARADAS; 

select lpad(linea, 5, '0') || lpad(ramal,5,'0') || sentido from paradas p1;

select lpad('a', 3, '0'); 


SELECT ST_Distance(
		ST_GeomFromText('POINT(-72.1235 42.3521)',4326),
		ST_GeomFromText('LINESTRING(-72.1260 42.45, -72.123 42.1546)', 4326)
	);

SELECT ST_GeomFromText('POINT(-72.1235 42.3521)',4326);

select * from sentido;

select selectted, procesado, count(*) from the_lotes group by selectted, procesado;

select * from the_lotes;



select distinct minfechatrx from the_lotes;

select COUNT(*) from the_lotes WHERE SELECTTED = 'P';

select idarchivointercambio, count(*) from the_lotes WHERE SELECTTED = 'P' group by  idarchivointercambio having count(*) > 1 order by count(*) desc;


select count(*) 
from (
	select idarchivointercambio
	from the_lotes
	where selectted = 'P'  
	group by idarchivointercambio
	having count(*) > 1
) a;
--224 486

select count(*) 
from (
	select idarchivointercambio
	from the_lotes  
	where selectted = 'P'
	group by idarchivointercambio
	having count(*) = 1
) a;
--771 206

select * from the_lotes where idarchivointercambio = 59467624;


select minfechaingreso, count(*) from the_lotes group by minfechaingreso order by minfechaingreso;

select count(distinct idarchivointercambio) from the_viajesmayo;
--16.870


 

