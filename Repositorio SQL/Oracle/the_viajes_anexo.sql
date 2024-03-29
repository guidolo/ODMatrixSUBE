/************ CREACION DE LA TABLA THE_VIAJES20150101 ************************/

CREATE TABLE THE_VIAJES20150101 AS
WITH VIAJES_EN_COLE AS 
    (
    SELECT /*+FULL(a) */ 
        NROTARJETAEXTERNO
    FROM exp_movimientotarjeta A JOIN
               LINEMT B ON CODIGOLINEA = LM_ID
               JOIN EXP_MAPEO ON TIPO_TRX     = CODIGOTIPOTRX
    AND NVL(CODIGOSUBTIPOTRX, 0) = SUBTIPO_TRX 
    WHERE fechaingreso >= TO_DATE('20150501', 'YYYYMMDD')
    and fechaingreso < TO_DATE('20150607',  'YYYYMMDD') 
    AND fechatrx >= TO_DATE('20150501', 'YYYYMMDD') + 0.125
    and fechatrx < TO_DATE('20150502', 'YYYYMMDD') + 0.125
    AND CATEGORIA='USO'
    GROUP BY NROTARJETAEXTERNO, TRUNC(FECHATRX - 0.125)
    HAVING COUNT(*) > 1
      AND  MAX(CASE WHEN LT_CODE = 'TRE' THEN 1 ELSE 0 END) = 0
      AND  MAX(CASE WHEN LT_CODE = 'SUB' THEN 1 ELSE 0 END) = 0
      AND  MAX(CASE WHEN LT_CODE = 'COL' THEN 1 ELSE 0 END) = 1
    )
  SELECT  /*+FULL(MT) FULL(L) */ 
        MT.CODIGOLINEA, 
        MT.CODIGOTRAYECTO RAMAL, 
        MT.NROTARJETAEXTERNO,  
        MT.CODIGOTRXTARJETA, 
        MT.FECHATRX, 
        MT.FECHAINGRESO, 
        MT.IDARCHIVOINTERCAMBIO,
        l.REF_EXT FILE_ID,
        MT.ID_POSICIONAMIENTO
FROM EXP_MOVIMIENTOTARJETA MT JOIN VIAJES_EN_COLE B ON MT.NROTARJETAEXTERNO = B.NROTARJETAEXTERNO
     JOIN LOTE L  ON  MT.IDARCHIVOINTERCAMBIO = L.ID_LOTE
WHERE FECHAINGRESO   >= TO_DATE('20150501','YYYYMMDD')
    AND FECHAINGRESO <  TO_DATE('20150607','YYYYMMDD')
    AND FECHATRX     >= TO_DATE('20150501','YYYYMMDD') + 0.125
    AND FECHATRX     <  TO_DATE('20150502','YYYYMMDD') +0.125
    AND CODIGOTIPOTRX = 19
         
SELECT COUNT(*) FROM THE_VIAJES20150101
--2.800.899


ALTER TABLE THE_VIAJES20150101
ADD PORC_RECORRIDO NUMBER

ALTER TABLE THE_VIAJES20150101
ADD (FECHAPTO1 DATE,
     FECHAPTO2 DATE)

MERGE INTO THE_VIAJES20150101 A
USING (
    SELECT  FILE_ID, C_CONTROL_POINT, DATE_TIME 
    FROM USR_POSICIONAMIENTO.TRX_POSITIONING A  
  ) B
ON (  A.FILE_ID = B.FILE_ID
      AND A.ID_POSICIONAMIENTO = B.C_CONTROL_POINT 
   )
WHEN MATCHED THEN UPDATE SET A.FECHAPTO1 = B.DATE_TIME;

COMMIT

MERGE INTO THE_VIAJES20150101 A
USING (
    SELECT  FILE_ID, C_CONTROL_POINT, DATE_TIME 
    FROM USR_POSICIONAMIENTO.TRX_POSITIONING A  
  ) B
ON (  A.FILE_ID = B.FILE_ID
      AND A.ID_POSICIONAMIENTO + 1 = B.C_CONTROL_POINT 
   )
WHEN MATCHED THEN UPDATE SET A.FECHAPTO2 = B.DATE_TIME;

commit;

--consulta que se uso en el qlickview para bajar los viajes de un dia
SELECT 
        CODIGOLINEA, 
        RAMAL, 
        NROTARJETAEXTERNO, 
        CODIGOTRXTARJETA, 
        FECHATRX, 
        FECHAINGRESO, 
        IDARCHIVOINTERCAMBIO, 
        FILE_ID, 
        ID_POSICIONAMIENTO C_CONTROL_POINT1, 
        ID_POSICIONAMIENTO + 1 C_CONTROL_POINT2, 
        REPLACE(TO_CHAR(ROUND((FECHATRX - FECHAPTO1) / (FECHAPTO2 - FECHAPTO1),2)), ',','.')  PORC_RECORRIDO,
        NULL LATITUDPTO3,
        NULL LONGITUDPTO3,
        NULL DISTANCIA
FROM THE_VIAJES20150101


SELECT COUNT(*)
       FROM USR_POSICIONAMIENTO.TRX_POSITIONING P, 
            (SELECT DISTINCT FILE_ID FROM THE_LOTES WHERE SELECTTED IS NULL) B 
      WHERE P.FILE_ID = B.FILE_ID 
        
   
/**/
 SELECT CODIGOLINEA, 
        RAMAL, 
        FILE_ID, 
         C_CONTROL_POINT,  
         LONGITUD,  
         LATITUD,   
         FECHAPTO,  
        (CASE WHEN DIFSEC > 235 AND DIFSEC < 245 THEN 'S' ELSE 'N' END) ESTADO,  
        DIFSEC, 
        SEGUNDOSPTO 
  FROM 
    (SELECT B.CODIGOLINEA,  
            B.RAMAL,  
            P.FILE_ID, 
            C_CONTROL_POINT, 
            LONGITUDE LONGITUD, 
            LATITUDE LATITUD,   
            DATE_TIME FECHAPTO, 
            (CASE WHEN LAG(P.file_id, 1) OVER (ORDER BY P.FILE_ID, P.C_CONTROL_POINT) =  P.file_id  THEN  DATE_TIME - LAG(DATE_TIME, 1) OVER (ORDER BY P.FILE_ID, P.C_CONTROL_POINT) END) * 24*60*60   DIFSEC, 
            (DATE_TIME - TO_DATE('20000101','YYYYMMDD')) * 24 * 60 * 60 SEGUNDOSPTO
       FROM USR_POSICIONAMIENTO.TRX_POSITIONING P, 
            (SELECT DISTINCT FILE_ID FROM THE_LOTES WHERE SELECTTED IS NULL) B  
      WHERE P.FILE_ID = B.FILE_ID 
     );




/************ CREACION DE LA TABLA THE_VIAJES20150508 ************************/

DROP TABLE THE_VIAJES20150508

CREATE TABLE THE_VIAJES20150508 AS
WITH VIAJES_EN_COLE AS 
    (
    SELECT /*+FULL(a) */ 
        NROTARJETAEXTERNO, 
        MIN(FECHATRX) MINFECHATRX,
        MAX(FECHATRX) MAXFECHATRX
    FROM exp_movimientotarjeta A JOIN
               LINEMT B ON CODIGOLINEA = LM_ID
               JOIN EXP_MAPEO ON TIPO_TRX     = CODIGOTIPOTRX
    AND NVL(CODIGOSUBTIPOTRX, 0) = SUBTIPO_TRX 
    WHERE fechaingreso >= TO_DATE('20150501', 'YYYYMMDD')
    and fechaingreso < TO_DATE('20150607',  'YYYYMMDD') 
    AND fechatrx >= TO_DATE('20150501', 'YYYYMMDD') + 0.125
    and fechatrx < TO_DATE('20150509', 'YYYYMMDD') + 0.125
    AND CATEGORIA='USO'
    GROUP BY NROTARJETAEXTERNO, TRUNC(FECHATRX - 0.125)
    HAVING COUNT(*) > 1
      AND  MAX(CASE WHEN LT_CODE = 'TRE' THEN 1 ELSE 0 END) = 0
      AND  MAX(CASE WHEN LT_CODE = 'SUB' THEN 1 ELSE 0 END) = 0
      AND  MAX(CASE WHEN LT_CODE = 'COL' THEN 1 ELSE 0 END) = 1
    )
  SELECT  /*+FULL(MT) FULL(L) */ 
        MT.CODIGOLINEA, 
        MT.CODIGOTRAYECTO RAMAL, 
        MT.NROTARJETAEXTERNO,  
        MT.CODIGOTRXTARJETA, 
        MT.FECHATRX, 
        MT.FECHAINGRESO, 
        MT.IDARCHIVOINTERCAMBIO,
        l.REF_EXT FILE_ID,
        MT.ID_POSICIONAMIENTO
FROM EXP_MOVIMIENTOTARJETA MT JOIN VIAJES_EN_COLE B ON MT.NROTARJETAEXTERNO = B.NROTARJETAEXTERNO AND FECHATRX >= MINFECHATRX AND FECHATRX <= MAXFECHATRX
     JOIN LOTE L  ON  MT.IDARCHIVOINTERCAMBIO = L.ID_LOTE
WHERE FECHAINGRESO   >= TO_DATE('20150501','YYYYMMDD')
    AND FECHAINGRESO <  TO_DATE('20150607','YYYYMMDD')
    AND FECHATRX     >= TO_DATE('20150501','YYYYMMDD') + 0.125
    AND FECHATRX     <  TO_DATE('20150509','YYYYMMDD') +0.125
    AND CODIGOTIPOTRX = 19
    
    
SELECT COUNT(*) FROM THE_VIAJES20150508
--57189859


ALTER TABLE THE_VIAJES20150508
ADD PORC_RECORRIDO NUMBER

ALTER TABLE THE_VIAJES20150508
ADD (FECHAPTO1 DATE,
     FECHAPTO2 DATE)

MERGE INTO  USRNSSA.THE_VIAJES20150508 A
USING (
    SELECT /*+full(A)*/ FILE_ID, C_CONTROL_POINT, DATE_TIME 
    FROM USR_POSICIONAMIENTO.TRX_POSITIONING A  
  ) B
ON (  A.FILE_ID = B.FILE_ID
      AND A.ID_POSICIONAMIENTO = B.C_CONTROL_POINT 
   )
WHEN MATCHED THEN UPDATE SET A.FECHAPTO1 = B.DATE_TIME;

COMMIT;

MERGE INTO USRNSSA.THE_VIAJES20150508 A
USING (
    SELECT  FILE_ID, C_CONTROL_POINT, DATE_TIME 
    FROM USR_POSICIONAMIENTO.TRX_POSITIONING A  
  ) B
ON (  A.FILE_ID = B.FILE_ID
      AND A.ID_POSICIONAMIENTO + 1 = B.C_CONTROL_POINT 
   )
WHEN MATCHED THEN UPDATE SET A.FECHAPTO2 = B.DATE_TIME;

commit;