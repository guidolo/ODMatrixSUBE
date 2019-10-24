

SELECT COUNT(*) FROM
(SELECT LINEA FROM LINEASCOLE GROUP BY LINEA) A
;
--277

SELECT COUNT(*) FROM
(SELECT LINEA FROM LINEASCOLE GROUP BY LINEA, RAMAL) A
;
--1037


SELECT COUNT(*) FROM (
SELECT id_empresa FROM THE_RAMALES WHERE CANTIDAD_TRX > 1000 AND LINEA2 IS NOT NULL GROUP BY id_empresa) A;
--173 


SELECT COUNT(*) FROM (
SELECT LINEA2 FROM THE_RAMALES WHERE CANTIDAD_TRX > 1000 AND LINEA2 IS NOT NULL GROUP BY LINEA2) A;
--354

SELECT COUNT(*) FROM (
SELECT LINEA2 FROM THE_RAMALES WHERE CANTIDAD_TRX > 1000 AND LINEA2 IS NOT NULL GROUP BY LINEA2, RAMAL) A;
--1199

WITH LINEASSHP AS (SELECT LINEA FROM LINEASCOLE GROUP BY LINEA),
LINEASSUBE AS (SELECT LINEA2 AS LINEA FROM THE_RAMALES WHERE CANTIDAD_TRX > 1000 AND LINEA2 IS NOT NULL GROUP BY LINEA2)
SELECT COUNT(*)
FROM LINEASSHP A, LINEASSUBE B
WHERE A.LINEA = B.LINEA;
--266

select count(*) from
(SELECT lineamt FROM RMSE group by lineamt) a;
--168

WITH LINEASSHP AS (SELECT linea FROM LINEASCOLE GROUP BY LINEA),
LINEASSUBE AS (SELECT LINEA2 AS LINEA FROM THE_RAMALES WHERE CANTIDAD_TRX > 1000 AND LINEA2 IS NOT NULL GROUP BY LINEA2)
SELECT *
FROM LINEASSHP A right outer join LINEASSUBE B on A.LINEA = B.LINEA
WHERE a.linea is null;
--88 estas son las 88 que no cruzaron con shape

WITH LINEASSHP AS (SELECT linea FROM LINEASCOLE GROUP BY LINEA),
LINEASSUBE AS (SELECT LINEA2 AS LINEA FROM THE_RAMALES WHERE CANTIDAD_TRX > 1000 AND LINEA2 IS NOT NULL GROUP BY LINEA2),
LAS88MASODIADAS AS ( SELECT b.linea FROM LINEASSHP A right outer join LINEASSUBE B on A.LINEA = B.LINEA WHERE a.linea is null),
TABLA AS (SELECT B.LINEAMT, B.RAMALMT, B.LINEA, B.RAMAL, B.SENTIDO, COUNT(*) CANTIDAD, 
				 				 (SELECT COUNT(*) FROM RMSE C WHERE B.LINEAMT = C.LINEAMT AND B.RAMALMT = C.RAMALMT) CANTTOT,
				 				 AVG(RMSE) RMSE_PROM
					FROM LAS88MASODIADAS A, rmse B 
					WHERE A.LINEA = B.LINEAmt
						AND  RMSE < 3
					GROUP BY B.LINEAMT, B.RAMALMT, B.LINEA, B.RAMAL, B.SENTIDO
					HAVING COUNT(*) > 2
					)
SELECT *, CANTIDAD *100 / CANTTOT AS PORC
FROM TABLA
WHERE CANTIDAD *100 / CANTTOT > 40
ORDER BY LINEAMT, RAMALMT, LINEA, RAMAL, SENTIDO;

ALTER TABLE LINEASTRXGEO 
ADD ETAPA INTEGER;

UPDATE LINEASTRXGEO 
SET ETAPA = 1;

ALTER TABLE LINEASTRXGEO 
ADD porc_votos_pos NUMERIC;

INSERT INTO LINEASTRXGEO (lineamt,  ramalmt,  lineageo,  ramalgeo, cantidadlotes,  avgrmse,  porc_votos_pos, etapa)
WITH LINEASSHP AS (SELECT linea FROM LINEASCOLE GROUP BY LINEA),
LINEASSUBE AS (SELECT LINEA2 AS LINEA FROM THE_RAMALES WHERE CANTIDAD_TRX > 1000 AND LINEA2 IS NOT NULL GROUP BY LINEA2),
LAS88MASODIADAS AS ( SELECT b.linea FROM LINEASSHP A right outer join LINEASSUBE B on A.LINEA = B.LINEA WHERE a.linea is null),
TABLA AS (SELECT B.LINEAMT, B.RAMALMT, B.LINEA, B.RAMAL, B.SENTIDO, COUNT(*) CANTIDAD, 
				 				 (SELECT COUNT(*) FROM RMSE C WHERE B.LINEAMT = C.LINEAMT AND B.RAMALMT = C.RAMALMT) CANTTOT,
				 				 AVG(RMSE) RMSE_PROM
					FROM LAS88MASODIADAS A, rmse B 
					WHERE A.LINEA = B.LINEAmt
						AND  RMSE < 3
					GROUP BY B.LINEAMT, B.RAMALMT, B.LINEA, B.RAMAL, B.SENTIDO
					HAVING COUNT(*) > 2
					)
SELECT lineamt, ramalmt, linea,ramal,cantidad, rmse_prom, CANTIDAD *100 / CANTTOT AS PORC, 2
FROM TABLA
WHERE CANTIDAD *100 / CANTTOT > 40
ORDER BY LINEAMT, RAMALMT, LINEA, RAMAL, SENTIDO;

SELECT * FROM LINEASTRXGEO ORDER BY LINEAMT, RAMALMT, RAMALGEO;

--cuantos ramales quedaron
select * from LINEASTRXGEO where baja is null; and RMSE < 3;
