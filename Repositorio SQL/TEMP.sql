
SELECT COUNT(*) FROM THE_VIAJES;

SELECT COUNT(*) FROM PTOCONTROL201505;

SELECT minfechaingreso, sentido, count(*)
FROM PTOCONTROL201505
group by minfechaingreso, sentido
order by minfechaingreso;

select * from lineastrxgeo;

SELECT count(*	) FROM the_lotes where selectted = 'S';

select count(*)
from sentido ;

select corrida, lineamt, ramalmt, sentido 
from clusters 
group by corrida, lineamt, ramalmt, sentido
order by corrida, lineamt, ramalmt, sentido;

select * from clusters where lineamt = '145' ;


SELECT minfechaingreso, selectted, procesado, count(*)
FROM the_lotes, 
group by minfechaingreso, selectted, procesado
order by minfechaingreso, selectted, procesado;

SELECT * 
FROM the_lotes
where minfechaingreso = to_date('20150506','yyyymmdd');

select * from sentido where file_id = 38935708;

select count(distinct file_id)  from sentido where sentido is not null;

select count(*)  from sentido where sentido is not null;

select count(*) from sentidoag;


SELECT sentido, count(*) 
FROM PTOCONTROL201505 
group by sentido;

SELECT B.NROTARJETAEXTERNO, A.LONGITUD longitudpto1, A.LATITUD latitudpto1, B.PORC_RECORRIDO, A.SENTIDO  
FROM  PTOCONTROL201505 A, 
     (SELECT * FROM THE_VIAJES WHERE  CODIGOLINEA = 388 AND RAMAL = '2552' AND (PORC_RECORRIDO < 0.1 OR PORC_RECORRIDO > 0.9)   ) B
WHERE A.FILE_ID = B.FILE_ID   
AND A.C_CONTROL_POINT = B.C_CONTROL_POINT1    
--AND a.SENTIDO = 'I' 
ORDER BY B.FECHATRX ;


SELECT * FROM THE_VIAJES WHERE  CODIGOLINEA = 388 AND RAMAL = '2552' AND (PORC_RECORRIDO < 0.1 OR PORC_RECORRIDO > 0.9);

SELECT B.NROTARJETAEXTERNO, A.LONGITUD longitudpto1, A.LATITUD latitudpto1, C.LONGITUD longitudpto2, C.LATITUD latitudpto2, B.PORC_RECORRIDO, A.SENTIDO  
FROM  PTOCONTROL201505 A, 
     (SELECT * FROM THE_VIAJES WHERE  CODIGOLINEA = 388 AND RAMAL = '2552' AND (PORC_RECORRIDO < 0.1 OR PORC_RECORRIDO > 0.9)   ) B  ,
PTOCONTROL201505 C  
WHERE A.FILE_ID = B.FILE_ID   
AND A.C_CONTROL_POINT = B.C_CONTROL_POINT1    
AND a.SENTIDO = 'I' 
AND C.FILE_ID = B.FILE_ID   
AND C.C_CONTROL_POINT = B.C_CONTROL_POINT2
ORDER BY B.FECHATRX ;



SELECT B.*, (SELECT A.LONGITUD longitudpto1 FROM PTOCONTROL201505 A WHERE A.FILE_ID = B.FILE_ID AND A.C_CONTROL_POINT = B.C_CONTROL_POINT1    AND A.SENTIDO = 'I' ) ALGO
FROM THE_VIAJES  B
WHERE  CODIGOLINEA = 388 AND RAMAL = '2552' AND (PORC_RECORRIDO < 0.1 OR PORC_RECORRIDO > 0.9) ;


SELECT B.*, (SELECT A.LONGITUD longitudpto1 FROM PTOCONTROL201505 A WHERE A.FILE_ID = B.FILE_ID AND A.C_CONTROL_POINT = B.C_CONTROL_POINT1    AND A.SENTIDO = 'I' ) ALGO
FROM THE_VIAJES  B
WHERE  CODIGOLINEA = 388 AND RAMAL = '2552' AND PORC_RECORRIDO < 0.1  ;


SELECT A.LONGITUD longitudpto1 FROM PTOCONTROL201505 A WHERE A.FILE_ID = 39147181 AND A.C_CONTROL_POINT = '4' AND A.SENTIDO = 'V';

SELECT B.*
FROM THE_VIAJES  B
WHERE  CODIGOLINEA = 388 AND RAMAL = '2552' AND (PORC_RECORRIDO < 0.1 OR PORC_RECORRIDO > 0.9) ;


select * from lineastrxgeo order by lineageo;

select count(*) from proyeccionruta;

select count(*) from the_viajes;

select * from the_viajes;

select count(*) from the_viajes where distancia is not null;

SELECT * FROM THE_VIAJES;


SELECT NROTARJETAEXTERNO, DISTANCIA
 FROM THE_VIAJES A, PTOCONTROL201505 B
 WHERE A.C_CONTROL_POINT1 = B.C_CONTROL_POINT
   AND A.FILE_ID = B.FILE_ID
	 AND A.CODIGOLINEA = 233
	 AND A.RAMAL = '785'
	 AND (PORC_RECORRIDO < 0.1 OR PORC_RECORRIDO > 0.9)
	 AND SENTIDO = 'I'
 ORDER BY A.FECHATRX;
 
select * 
from the_viajes; 

select * from paradas order by linea, ramal, sentido, clusterord;

SELECT a.linea, a.ramal, a.sentido, count(*) 
FROM paradas a, the_viajes b
where a.linea = to_char(b.codigolinea, '999')
  and a.ramal = b.ramal
  and b.porc_recorrido > 0.9 or b.porc_recorrido < 0.1
  and b.distancia is not null 
group by linea, a.ramal, a.sentido
order by linea, a.ramal, a.sentido;

WITH viajes as (
	SELECT a.codigolinea, a.ramal, count(*) cantviajes
	FROM THE_VIAJES A, PTOCONTROL201505 B 
	WHERE A.C_CONTROL_POINT1 = B.C_CONTROL_POINT 
	 AND A.FILE_ID = B.FILE_ID 
	AND (PORC_RECORRIDO < 0.1 OR PORC_RECORRIDO > 0.9) 
	AND SENTIDO IS NOT NULL
	GROUP BY a.codigolinea, a.ramal
)
SELECT a.codigolinea, a.ramal, cantviajes, diferencia
FROM viajes a, (select linea, ramal, count(*) cantparadas,  abs(  sum(case when sentido = 'I' then 1 else 0 end) - sum(case when sentido = 'V' then 1 else 0 end)) diferencia from paradas group by linea, ramal ) b
where a.codigolinea = to_number(b.linea, '999')
  and a.ramal = b.ramal
order by a.codigolinea, a.ramal;



select * from lineastrxgeo where lineageo = '202';


select count(*) from ptocontrol201505 where sentido is not null ;
--2.573.886

select count(*) from sentido;
--2.573.886

select * from sentido;

select * from ptocontrol201505;

SELECT * FROM THE_VIAJES;

SELECT COUNT(*) FROM PTOCONTROL201505;

SELECT * FROM LINEASTRXGEO;

WITH JUNTA AS (
					SELECT  A.CODIGOLINEA, A.RAMAL, B.SENTIDO, 
					COUNT(*) CANTIDAD,
					SUM(CASE WHEN (PORC_RECORRIDO < 0.04 OR PORC_RECORRIDO > 0.96) THEN 1 ELSE 0 END) CANT004,
					SUM(CASE WHEN  DISTRUTA > 0 AND DISTRUTA < 60 THEN 1 ELSE 0 END) CANT060,
					SUM(CASE WHEN (PORC_RECORRIDO < 0.04 OR PORC_RECORRIDO > 0.96) AND DISTRUTA > 0 AND DISTRUTA < 60 THEN 1 ELSE 0 END) CANTRESTRIC
					 FROM  THE_VIAJES A, PTOCONTROL201505 B 
					 WHERE A.C_CONTROL_POINT1 = B.C_CONTROL_POINT 
					   AND A.FILE_ID = B.FILE_ID 
					GROUP BY A.CODIGOLINEA, A.RAMAL, B.SENTIDO
					ORDER BY to_char(A.codigolinea, '999'), A.RAMAL, B.SENTIDO
					),
LINEA AS (
				SELECT TO_NUMBER(a.LINEAMT, '999') LINEAMT, A.RAMALMT, B.sentido, AVGRMSE, DESVRMSE
				FROM lineastrxgeo a, lineascole b 
				where a.lineageo = b.linea2 and a.ramalgeo = ramal and a.baja is null 
				ORDER BY a.LINEAMT, A.RAMALMT, B.sentido
			),
PARADAS AS (
				select linea, ramal, count(*) cantparadas,  
								abs(  sum(case when sentido = 'I' then 1 else 0 end) - sum(case when sentido = 'V' then 1 else 0 end)) diferencia 
								from paradas 
								group by linea, ramal
			)
SELECT A.LINEAMT, A.RAMALMT, A.SENTIDO, A.AVGRMSE, A.DESVRMSE, B.CANTIDAD, CANT004, CANT060, CANTRESTRIC, C.DIFERENCIA
FROM LINEA A LEFT JOIN JUNTA B ON A.LINEAMT = B.CODIGOLINEA AND A.RAMALMT = B.RAMAL AND A.SENTIDO = B.SENTIDO
LEFT JOIN PARADAS C ON A.LINEAMT = TO_NUMBER(C.LINEA, '999') AND A.RAMALMT = C.RAMAL
ORDER BY CANTIDAD
;

SELECT * FROM PARADAS;

create table paradas1090 as
select * from paradas;

create table paradas00496 as
select * from paradas;


--truncate table paradas;
with lote004 as 
(
	select b.file_id, rmse
	from lineastrxgeo a , distanciacuadrado b
	where a.lineamt = b.lineamt 
	  and a.ramalmt = b.ramalmt
	  and a.ramalgeo = b.ramalgeo
		and a.baja is null
		and rmse < 0.04
--	order by a.lineamt, a.ramalmt, a.lineageo, a.ramalgeo
)
select distruta
from ptocontrol201505 a, lote004 b
where a.file_id = b.file_id;

select * from distanciacuadrado;

select selectted, procesado, count(*)
from the_lotes
group by selectted, procesado;


		1164807
S	S	17605
S	2	10690
D	1	30
2	S	46726
2	2	24270
2	4	117
2	T	13
S	4	23
S	T	2
2	1	328
D	2	3664
S	1	133
D	S	16049
S	3	3

UPDATE THE_LOTES SET PROCESADO = NULL WHERE PROCESADO IN ('T','1','2','3','4')


select codigolinea, count(*)
from the_lotes
where selectted is not null
group by codigolinea
order by codigolinea;




update ptocontrol201505
set sentido = null,
		distruta =null
 WHERE  CODIGOLINEA = '145';


select * from lineastrxgeo where lineamt = '466';

SELECT * FROM PTOCONTROL201505 WHERE  CODIGOLINEA = '41' AND RAMAL = '327' ORDER BY FILE_ID, c_control_point;



SELECT * FROM THE_LOTES where CODIGOLINEA ='145' AND SELECTTED IS NOT NULL;
--297

SELECT COUNT(DISTINCT FILE_ID) FROM SENTIDO WHERE LINEA = '145';
--234

SELECT COUNT(DISTINCT FILE_ID) FROM PTOCONTROL201505 where CODIGOLINEA='145' AND SENTIDO IS NOT NULL;
--282

SELECT COUNT(DISTINCT FILE_ID) FROM PTOCONTROL201505 where CODIGOLINEA='145' AND SENTIDO IS NULL;
--40

TRUNCATE TABLE SENTIDO;

UPDATE THE_LOTES SET PROCESADO = NULL WHERE CODIGOLINEA = 145;

UPDATE THE_LOTES SET PROCESADO = NULL WHERE CODIGOLINEA  in (41,70,159,182,138,142,150,151,42,53,66,71, 87,
101,119,147,190,191,265,619,85,100,106,110,123,127,130,141,154,
156,170,179,180,184,257,330,43,63,103,133,153,155,165,172,193,
385,35,55,67,76,79,143,278,50,57,107,220,224,310,315);


select count(*) from THE_LOTES WHERE CODIGOLINEA  in (41,70,159,182,138,142,150,151,42,53,66,71, 87,
101,119,147,190,191,265,619,85,100,106,110,123,127,130,141,154,
156,170,179,180,184,257,330,43,63,103,133,153,155,165,172,193,
385,35,55,67,76,79,143,278,50,57,107,220,224,310,315)
and selectted is not null;

SELECT * FROM THE_VIAJES where CODIGOLINEA = '145' order by file_id, c_control_point1;

SELECT count(*) FROM THE_VIAJES where CODIGOLINEA = '145' and distancia IS NULL;

select * from the_lotes where file_id = '38705695';



select * from sentido;

select * from ptocontrol201505 where file_id   = '38705695';

SELECT * FROM THE_LOTES WHERE codigolinea = 145 and selectted is not null; 

select * from ptocontrol201505 where file_id   = '39777895';



SELECT FECHAINGRESO, COUNT(*)
FROM THE_VIAJES 
GROUP BY FECHAINGRESO
ORDER BY FECHAINGRESO;


SELECT * FROM THE_VIAJES where  CODIGOLINEA = '145' AND PORC_RECORRIDO IS NULL;

SELECT * FROM THE_VIAJES where  CODIGOLINEA = '145';


SELECT * FROM PROYECCIONRUTA;

--truncate table proyeccionruta;

UPDATE THE_VIAJES
SET DISTANCIA = NULL
WHERE DISTANCIA = 0;

SELECT * FROM PARADAS;

--truncate table clusters;

select * from clusters;

select codigolinea, selectted, procesado,count(*)
from the_lotes 
where selectted is not null and procesado is null and
codigolinea in (41,70,145, 159,182,138,142,150,151,42,53,66,71, 87,
101,119,147,190,191,265,619,85,100,106,110,123,127,130,141,154,
156,170,179,180,184,257,330,43,63,103,133,153,155,165,172,193,
385,35,55,67,76,79,143,278,50,57,107,220,224,310,315)
group by codigolinea, selectted, procesado
order by codigolinea, selectted, procesado;

select count(*)
from the_lotes 
where selectted is not null and procesado is null and
codigolinea in (41,70,145, 159,182,138,142,150,151,42,53,66,71, 87,
101,119,147,190,191,265,619,85,100,106,110,123,127,130,141,154,
156,170,179,180,184,257,330,43,63,103,133,153,155,165,172,193,
385,35,55,67,76,79,143,278,50,57,107,220,224,310,315)
;

SELECT DISTINCT CODIGOLINEA FROM PTOCONTROL201505 WHERE SENTIDO IS NOT NULL ORDER BY CODIGOLINEA;

select * from the_lotes where file_id = 40119327;
 
select * from sentido;


select * from paradas;

select *, lag(segundospto, 1) over(order by file_id, c_control_point) - segundospto
from ptocontrol201505 
where codigolinea = '145'
order by file_id, c_control_point;

select * from  sentidoag;

truncate table  sentidoag;


SELECT codigolinea, ramal, segundospto, segundospto - 483000000
FROM PTOCONTROL201505 
WHERE CODIGOLINEA = '145' and ramal = '325' 
ORDER BY CODIGOLINEA, RAMAL, FILE_ID, C_CONTROL_POINT ;


SELECT *
FROM PTOCONTROL201505 
where to_number(codigolinea,'999')  IN (41,70,145, 159,182,138,142,150,151,42,53,66,71, 87, 
			101,119,147,190,191,265,619,85,100,106,110,123,127,130,141,154,
			156,170,179,180,184,257,330,43,63,103,133,153,155,165,172,193,
			385,35,55,67,76,79,143,278,50,57,107,220,224,310,315)
ORDER BY FILE_ID, C_CONTROL_POINT ;

SELECT *
FROM PTOCONTROL201505 
where codigolinea = '106'
ORDER BY FILE_ID, C_CONTROL_POINT ;


select * from lineascole;

select * from largos;

select * from sentidoag;

--truncate table sentidoag;

select * from lineastrxgeo;

select a.codigolinea, a.ramal, a.sentido, 	min(c.largokm) largokm,
	PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY difmin) extremosup,
	PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY difmin) extremoinf,
	PERCENTILE_DISC(0.50) WITHIN GROUP (ORDER BY difmin) median,
	min(c.largokm) / (PERCENTILE_DISC(0.50) WITHIN GROUP (ORDER BY difmin) / 60) velkmh
from sentidoag a, lineastrxgeo b, lineascole c
where difmin > 20 and difmin < 200 
  and a.codigolinea = b.lineamt
  and a.ramal = b.ramalmt
  and b.lineageo = c.linea2
  and b.ramalgeo = c.ramal
  and a.sentido = c.sentido
group by a.codigolinea, a.ramal, a.sentido 
order by a.codigolinea, a.ramal, a.sentido;

	select a.lineamt, a.ramalmt, a.sentido, max(a.k) k
	from clusters a,
		(select lineamt, ramalmt, sentido, corrida, max(shilo) maxshilo
		from clusters
		group by lineamt, ramalmt, sentido, corrida) b
	where a.lineamt = b.lineamt
	  and a.ramalmt = b.ramalmt
	  and a.sentido = b.sentido
	  and a.shilo = b.maxshilo
	group by a.lineamt, a.ramalmt, a.sentido;	


									select distinct linea
									from paradas
									group by linea, ramal, sentido, clusterord
									having count(*) > 1;

select distinct lineageo from lineastrxgeo 
where lineamt in (
'153',
'154',
'119',
'155',
'43',
'110')
order by lineageo;

select count(*)  from paradas 
where linea in  (
'153',
'154',
'119',
'155',
'43',
'110');

delete from paradas 
where linea in  (
'153',
'154',
'119',
'155',
'43',
'110');



select * 
from paradas a , (
									select distinct linea, ramal, sentido
									from paradas
									group by linea, ramal, sentido, clusterord
									having count(*) > 1) b
where a.linea = b.linea
  and a.ramal = b.ramal
  and a.sentido = b.sentido
order by a.linea, a.ramal, a.sentido, a.clusterord
;

select * from paradas;

--truncate table paradas;

select * from clusters where lineamt = '103' and ramalmt = '391' and sentido = 'I';
103	391	I	32.0


select a.codigolinea, a.ramal, a.sentido, 	min(c.largokm) largokm,
	PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY difmin) extremosup,
	PERCENTILE_DISC(0.25) WITHIN GROUP (ORDER BY difmin) extremoinf,
	PERCENTILE_DISC(0.50) WITHIN GROUP (ORDER BY difmin) median,
	min(c.largokm) / (PERCENTILE_DISC(0.50) WITHIN GROUP (ORDER BY difmin) / 60) velkmh
from sentidoag a, lineastrxgeo b, lineascole c
where difmin > 20 and difmin < 200 
  and a.codigolinea = b.lineamt
  and a.ramal = b.ramalmt
  and b.lineageo = c.linea2
  and b.ramalgeo = c.ramal
  and a.sentido = c.sentido
group by a.codigolinea, a.ramal, a.sentido 
order by a.codigolinea, a.ramal, a.sentido;




select a.linea, a.ramal, a.sentido, count(*) cantidad, min(c.largokm) largokm
from paradas a, lineastrxgeo b, lineascole c
where   a.linea = b.lineamt
  and a.ramal = b.ramalmt
  and b.lineageo = c.linea2
  and b.ramalgeo = c.ramal
  and a.sentido = c.sentido
group by a.linea, a.ramal, a.sentido
;
