
-- proporci�n de viajes 

SELECT (CASE WHEN LT_CODE = 'COL' THEN 'COL' ELSE CASE WHEN ID_LINEA between 440 and 446 THEN 'SUB' ELSE CASE WHEN ID_EMPRESA IN  (1, 94, 167, 168, 169, 178, 204, 9994,213) THEN 'TREN' ELSE LT_CODE END END END) TIPOTRANS,        
       SUM(CANTIDAD)  
FROM EXP_GRUPO_TRXS A, LINEMT B
WHERE DIA_TRX >= TO_DATE('20140801','YYYYMMDD')
  AND DIA_TRX < TO_DATE('20140901','YYYYMMDD')
  AND DIA_INGRESO >= TO_DATE('20140801','YYYYMMDD')
  AND DIA_INGRESO < TO_DATE('20140901','YYYYMMDD')
  AND A.ID_LINEA = B.LM_ID
  AND CATEGORIA IN ('USO','VENTA','VENTA_ABONO')
  AND LT_CODE  NOT IN ('MIC','PEA')  
GROUP BY  ( CASE WHEN LT_CODE = 'COL' THEN 'COL' ELSE CASE WHEN ID_LINEA between 440 and 446 THEN 'SUB' ELSE CASE WHEN ID_EMPRESA IN  (1, 94, 167, 168, 169, 178, 204, 9994,213) THEN 'TREN' ELSE LT_CODE END END END )  

SUB    18459562
COL    279822726
TREN    16728495  


SELECT SUM(CASE WHEN LT_CODE = 'COL' AND AREAGEOGRAFICA = 1 THEN CANTIDAD ELSE 0 END) COLECTIVO_CAPI, 
       SUM(CASE WHEN LT_CODE = 'COL' AND AREAGEOGRAFICA <> 1 THEN CANTIDAD ELSE 0 END) COLECTIVO_NO_CAPI      
FROM EXP_GRUPO_TRXS A, LINEMT B, LINEA C
WHERE DIA_TRX >= TO_DATE('20140801','YYYYMMDD')
  AND DIA_TRX < TO_DATE('20140901','YYYYMMDD')
  AND DIA_INGRESO >= TO_DATE('20140801','YYYYMMDD')
  AND DIA_INGRESO < TO_DATE('20140901','YYYYMMDD')
  AND A.ID_LINEA = B.LM_ID
  AND A.ID_LINEA = C.IDLINEA
  AND CATEGORIA IN ('USO','VENTA','VENTA_ABONO')
  AND LT_CODE  NOT IN ('MIC','PEA')  
  AND LT_CODE = 'COL' 
 
--distribuci�n diaria
SELECT DIA_TRX,
       SUM(CASE WHEN LT_CODE = 'COL' AND AREAGEOGRAFICA = 1 THEN CANTIDAD ELSE 0 END) COLECTIVO_CAPI, 
       SUM(CASE WHEN LT_CODE = 'COL' AND AREAGEOGRAFICA <> 1 THEN CANTIDAD ELSE 0 END) COLECTIVO_NO_CAPI,
       SUM(CASE WHEN ID_EMPRESA = 1 AND ID_LINEA between 440 and 446 OR  ID_LINEA between 9000 and 9006 THEN CANTIDAD ELSE 0 END) SUBTE,
       SUM(CASE WHEN ID_EMPRESA IN  (1, 94, 167, 168, 169, 178, 204, 9994,213) AND NOT (ID_LINEA between 440 and 446 OR  ID_LINEA between 9000 and 9006 ) THEN CANTIDAD ELSE 0 END ) TREN,
       SUM(CANTIDAD) CANTIDAD         
FROM EXP_GRUPO_TRXS A, LINEMT B, LINEA C
WHERE DIA_TRX >= TO_DATE('20140801','YYYYMMDD')
  AND DIA_TRX < TO_DATE('20140901','YYYYMMDD')
  AND A.ID_LINEA = B.LM_ID
  AND A.ID_LINEA = C.IDLINEA
  AND CATEGORIA IN ('USO','VENTA','VENTA_ABONO')
  AND LT_CODE  NOT IN ('MIC','PEA')  
GROUP BY DIA_TRX  
ORDER BY DIA_TRX


--proporcion de usos de colectivo en 
SELECT DIA_TRX,
       SUM(CASE WHEN LT_CODE = 'COL' AND AREAGEOGRAFICA = 1 THEN CANTIDAD ELSE 0 END) COLECTIVO_CAPI, 
       SUM(CASE WHEN LT_CODE = 'COL' AND AREAGEOGRAFICA <> 1 THEN CANTIDAD ELSE 0 END) COLECTIVO_NO_CAPI,
       SUM(CANTIDAD) CANTIDAD         
FROM EXP_GRUPO_TRXS A, LINEMT B, LINEA C
WHERE DIA_TRX >= TO_DATE('20140801','YYYYMMDD')
  AND DIA_TRX < TO_DATE('20140901','YYYYMMDD')
  AND A.ID_LINEA = B.LM_ID
  AND A.ID_LINEA = C.IDLINEA
  AND A.CATEGORIA IN ('USO','VENTA','VENTA_ABONO')
  AND LT_CODE  NOT IN ('MIC','PEA')  
GROUP BY DIA_TRX  
ORDER BY DIA_TRX


--cuantos solo se toman colectivos de capital y subte
SELECT cantidad_usos, count(*) "cantidad de trj" 
FROM EXP_TARJETA_INFO_MENSUAL
WHERE ANO = 2014  AND MES = 08
GROUP BY cantidad_usos
ORDER BY cantidad_usos

DROP TABLE TEMP_TEMP39 

CREATE TABLE TEMP_TEMP39 AS
SELECT TRUNC(FECHATRX) DIATRX, NROTARJETAEXTERNO, AREAGEOGRAFICA, COUNT(*) CANTIDAD
FROM USRNSSA.EXP_MOVIMIENTOTARJETA mov,
    USRNSSA.LINEMT,
    LINEA
WHERE mov.CODIGOLINEA = LM_ID
 AND IDLINEA = MOV.CODIGOLINEA
 --AND linea.AREAGEOGRAFICA IN (1,11,12,13,16) -- Que sean l�neas de colectivos
 AND LT_CODE = 'COL' -- Que sean l�neas de colectivos
 AND mov.CODIGOTIPOTRX = 19          -- Que sean usos 
 AND mov.CODIGOSUBTIPOTRX IS NULL -- Que sean usos 
 AND mov.FECHAINGRESO >= TO_DATE('20140804','YYYYMMDD')
 AND mov.FECHAINGRESO < TO_DATE('20140817','YYYYMMDD')
 AND mov.FECHATRX >= TO_DATE('20140804','YYYYMMDD')
 AND mov.FECHATRX < TO_DATE('20140811','YYYYMMDD')
GROUP BY TRUNC(FECHATRX), NROTARJETAEXTERNO, AREAGEOGRAFICA    


DROP TABLE TEMP_TEMP40

CREATE TABLE TEMP_TEMP40 AS
  SELECT TRUNC(FECHATRX) DIATRX,NROTARJETAEXTERNO, (CASE WHEN CODIGOLINEA between 440 and 446 OR  CODIGOLINEA between  9000 and 9006  THEN 'S' ELSE 'T' END) TIPO, COUNT(*) CANTIDAD
  FROM EXP_MOVIMIENTOTARJETA mov
  WHERE mov.CODIGOENTIDAD in (1, 94, 167, 168, 169, 178, 204, 9994,213) -- entidades de trenes y subtes 
    AND mov.CODIGOTIPOTRX in (19,12)                                  -- Que sean checkout raros, usos, y check out/anulaciones (de trenes) 
    AND mov.FECHAINGRESO >= TO_DATE('20140804','YYYYMMDD') 
    AND mov.FECHAINGRESO <  TO_DATE('20140817','YYYYMMDD')
    AND mov.FECHATRX >= TO_DATE('20140804','YYYYMMDD') 
    AND mov.FECHATRX <  TO_DATE('20140811','YYYYMMDD')
  GROUP BY TRUNC(FECHATRX), NROTARJETAEXTERNO,  (CASE WHEN CODIGOLINEA between 440 and 446 OR  CODIGOLINEA between  9000 and 9006 THEN 'S' ELSE 'T' END)
  


DROP TABLE  TEMP_TEMP41

CREATE TABLE TEMP_TEMP41 AS 
SELECT (CASE WHEN A.DIATRX IS NULL THEN B.DIATRX ELSE A.DIATRX END) DIATRX, 
       (CASE WHEN A.NROTARJETAEXTERNO IS NULL THEN B.NROTARJETAEXTERNO ELSE A.NROTARJETAEXTERNO END) NROTARJETAEXTERNO, 
       COLE_CAPITAL,
       COLE_NO_CAPITAL,
       SUBTE,
       TREN 
FROM (SELECT NROTARJETAEXTERNO, DIATRX, 
       SUM(CASE WHEN AREAGEOGRAFICA = 1 THEN CANTIDAD ELSE 0 END) COLE_CAPITAL, 
       SUM(CASE WHEN AREAGEOGRAFICA <> 1 THEN CANTIDAD ELSE 0 END) COLE_NO_CAPITAL
        FROM TEMP_TEMP39
        GROUP BY NROTARJETAEXTERNO, DIATRX) A FULL OUTER JOIN 
      (SELECT NROTARJETAEXTERNO, DIATRX, 
       SUM(CASE WHEN TIPO = 'S' THEN CANTIDAD ELSE 0 END) SUBTE, 
       SUM(CASE WHEN TIPO = 'T' THEN CANTIDAD ELSE 0 END) TREN
        FROM TEMP_TEMP40
        GROUP BY NROTARJETAEXTERNO, DIATRX) B
ON A.NROTARJETAEXTERNO = B.NROTARJETAEXTERNO
 AND  A.DIATRX = B.DIATRX
 
 
SELECT DIATRX, COUNT(*), SUM(NVL(COLE_CAPITAL,0) + NVL(COLE_NO_CAPITAL,0) + NVL(SUBTE,0) + NVL(TREN,0))
FROM TEMP_TEMP41
GROUP BY DIATRX
ORDER BY DIATRX



--cantidad de viajes por dia total dias de sem
SELECT NVL(COLE_CAPITAL,0) + NVL(COLE_NO_CAPITAL,0) + NVL(SUBTE,0) + NVL(TREN,0) cantidad, COUNT(*)
FROM TEMP_TEMP41
WHERE DIATRX >= TO_DATE('20140804','YYYYMMDD') AND DIATRX <= TO_DATE('20140808','YYYYMMDD') 
GROUP BY NVL(COLE_CAPITAL,0) + NVL(COLE_NO_CAPITAL,0) + NVL(SUBTE,0) + NVL(TREN,0)
ORDER BY NVL(COLE_CAPITAL,0) + NVL(COLE_NO_CAPITAL,0) + NVL(SUBTE,0) + NVL(TREN,0)

--cantidad de viajes por dia capital dias de sem
SELECT NVL(COLE_CAPITAL,0) + NVL(SUBTE,0) cantidad, COUNT(*)
FROM TEMP_TEMP41
WHERE DIATRX >= TO_DATE('20140804','YYYYMMDD') AND DIATRX <= TO_DATE('20140808','YYYYMMDD')
and NVL(COLE_CAPITAL,0) + NVL(SUBTE,0) > 0 
GROUP BY NVL(COLE_CAPITAL,0) + NVL(SUBTE,0)
ORDER BY NVL(COLE_CAPITAL,0) + NVL(SUBTE,0)


--cantidad de viajes por dia no capi dias de sem
SELECT NVL(COLE_NO_CAPITAL,0) + NVL(TREN,0) cantidad, COUNT(*)
FROM TEMP_TEMP41
WHERE DIATRX >= TO_DATE('20140804','YYYYMMDD') AND DIATRX <= TO_DATE('20140808','YYYYMMDD')
and NVL(COLE_NO_CAPITAL,0) + NVL(TREN,0) > 0 
GROUP BY NVL(COLE_NO_CAPITAL,0) + NVL(TREN,0)
ORDER BY NVL(COLE_NO_CAPITAL,0) + NVL(TREN,0)




--cantidad de viajes por dia capital dias de sem
SELECT diatrx,NVL(COLE_CAPITAL,0) + NVL(COLE_NO_CAPITAL,0) + NVL(SUBTE,0) + NVL(TREN,0) cantidad, COUNT(*)
FROM TEMP_TEMP41
WHERE DIATRX >= TO_DATE('20140809','YYYYMMDD') AND DIATRX <= TO_DATE('20140810','YYYYMMDD')
GROUP BY diatrx, NVL(COLE_CAPITAL,0) + NVL(COLE_NO_CAPITAL,0) + NVL(SUBTE,0) + NVL(TREN,0) 
ORDER BY diatrx, NVL(COLE_CAPITAL,0) + NVL(COLE_NO_CAPITAL,0) + NVL(SUBTE,0) + NVL(TREN,0) 

--cantidad de viajes por dia capital dias de sem
SELECT diatrx, NVL(COLE_CAPITAL,0) + NVL(SUBTE,0) cantidad, COUNT(*)
FROM TEMP_TEMP41
WHERE DIATRX >= TO_DATE('20140809','YYYYMMDD') AND DIATRX <= TO_DATE('20140810','YYYYMMDD')
and NVL(COLE_CAPITAL,0) + NVL(SUBTE,0) > 0 
GROUP BY diatrx, NVL(COLE_CAPITAL,0) + NVL(SUBTE,0)
ORDER BY diatrx, NVL(COLE_CAPITAL,0) + NVL(SUBTE,0)

--cantidad de viajes por dia no capi dias de sem
SELECT diatrx, NVL(COLE_NO_CAPITAL,0) + NVL(TREN,0) cantidad, COUNT(*)
FROM TEMP_TEMP41
WHERE DIATRX >= TO_DATE('20140809','YYYYMMDD') AND DIATRX <= TO_DATE('20140810','YYYYMMDD')
and NVL(COLE_NO_CAPITAL,0) + NVL(TREN,0) > 0 
GROUP BY diatrx, NVL(COLE_NO_CAPITAL,0) + NVL(TREN,0)
ORDER BY diatrx, NVL(COLE_NO_CAPITAL,0) + NVL(TREN,0)


--cuantos viajan solo en capital

SELECT diatrx, COUNT(*)
FROM TEMP_TEMP41
WHERE 
--DIATRX >= TO_DATE('20140809','YYYYMMDD') AND DIATRX <= TO_DATE('20140810','YYYYMMDD')
NVL(COLE_CAPITAL,0) + NVL(SUBTE,0) > 0 
and NVL(COLE_NO_CAPITAL,0) + NVL(TREN,0) = 0
GROUP BY diatrx
ORDER BY diatrx


SELECT diatrx, COUNT(*)
FROM TEMP_TEMP41
GROUP BY diatrx
ORDER BY diatrx