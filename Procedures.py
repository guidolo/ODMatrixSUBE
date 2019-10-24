# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 15:44:29 2015

@author: gsidoni
"""


def lineaTrxGeo(cursor):

    sqlquery = ("CREATE TABLE MINDISTANCIA AS "
                "SELECT LINEAMT, RAMALMT, LINEAGEO, RAMALGEO, PUNTO, MIN(DISTANCIA) MINDISTANCIA, MAX(DISTANCIA) MAXDISTANCIA, COUNT(*) CANTIDADREG "
                "FROM DISTANCIAS  "
                "GROUP BY  LINEAMT, RAMALMT, LINEAGEO, RAMALGEO, PUNTO" )

    cursor.execute(sqlquery)

    sqlquery = ("CREATE TABLE DISTANCIACUADRADO AS "
                "SELECT lineamt, ramalmt,lineageo, ramalgeo,  "
                "		sum(SQUARE(MINDISTANCIA)) distanciacuad, " 
                "		count(*) cantidad, "
                "		SQRT(sum(SQUARE(MINDISTANCIA))/ COUNT(*))  RMSE "
                "FROM MINDISTANCIA "
                "WHERE MINDISTANCIA < 50 "
                "GROUP BY LINEAMT, RAMALMT, LINEAGEO, RAMALGEO; " )

    cursor.execute(sqlquery)

    sqlquery = ("CREATE TABLE LINEASTRXGEO AS "
                "SELECT A.* "
                "FROM DISTANCIACUADRADO A, "
                "		(SELECT LINEAMT, RAMALMT,  MIN(RMSE) MINRMSE "
                "		FROM DISTANCIACUADRADO "
                "		WHERE CANTIDAD > 50 "
                "		GROUP BY LINEAMT, RAMALMT "
                "		) B "
                "WHERE A.LINEAMT = B.LINEAMT "
                "  AND A.RAMALMT = B.RAMALMT "
                "  AND A.RMSE = B.MINRMSE ")

    cursor.execute(sqlquery)
	
def puntosControl():

	sqlquery = ("CREATE TABLE MINDISTANCIA AS "
                "SELECT LINEAMT, RAMALMT, LINEAGEO, RAMALGEO, PUNTO, MIN(DISTANCIA) MINDISTANCIA, MAX(DISTANCIA) MAXDISTANCIA, COUNT(*) CANTIDADREG "
                "FROM DISTANCIAS  "
                "GROUP BY  LINEAMT, RAMALMT, LINEAGEO, RAMALGEO, PUNTO" )

    cursor.execute(sqlquery)

def rawPuntosControl(fechaingreso, fechaingresohasta, cursor):  
    sqlquery = ("INSERT INTO GUI_LOTES (ID_LOTE, FILE_ID, LINEA, RAMAL, FECHAINGRESO)" 
          "  SELECT B.ID_LOTE, " 
          "         REF_EXT FILE_ID, "
          "         C.CODIGOLINEA LINEA, "
          "         A.CODIGOTRAYECTO RAMAL, "
          "         MIN(TRUNC(A.FECHAINGRESO)) FECHAINGRESO "
          "  FROM EXP_movimientotarjeta A, LOTE B, LINEA C "
          "  WHERE FECHAINGRESO > TO_DATE('%s','YYYYMMDD') AND FECHAINGRESO < TO_DATE('%s','YYYYMMDD')  "
          "    AND A.CODIGOLINEA = C.IDLINEA "
          "    AND A.idarchivointercambio = B.id_lote "
          "    AND AREAGEOGRAFICA IN (1,11,12,13) "
          "  GROUP BY B.ID_LOTE, REF_EXT, C.CODIGOLINEA, A.CODIGOTRAYECTO " %(fechaingreso, fechaingresohasta))    
    
    curora.execute(sqlquery)

    #        se cargan todos los puntos de control de los lotes previamente cargados
    sqlquery = ("INSERT INTO RAWPTOCONTROL(LINEA, 
                                           RAMAL, 
                                           FILE_ID, 
                                           C_CONTROL_POINT, 
                                           LONGITUD, 
                                           LATITUD, 
                                           FECHAPTO, 
                                           ESTADO, 
                                           DIFSEC, 
                                           SEGUNDOSPTO, 
                                           FECHAINGRESO) "
    " SELECT LINEA, 
    "        RAMAL, 
    "        FILE_ID, 
    "         C_CONTROL_POINT,  "
    "         LONGITUD,  "
    "         LATITUD,   "
    "         FECHAPTO,  "
    "        (CASE WHEN DIFSEC > 235 AND DIFSEC < 245 THEN 'S' ELSE 'N' END),  
            DIFSEC, 
            SEGUNDOSPTO, 
            FECHAINGRESO "
    "  FROM "
    "    (SELECT B.LINEA,  "
    "            B.RAMAL,  "
    "            P.FILE_ID, "
    "            C_CONTROL_POINT, "
    "            LONGITUDE LONGITUD, "
    "            LATITUDE LATITUD,   "
    "            DATE_TIME FECHAPTO, "
    "            (CASE WHEN LAG(P.file_id, 1) OVER (ORDER BY P.FILE_ID, P.C_CONTROL_POINT) =  P.file_id  THEN  DATE_TIME - LAG(DATE_TIME, 1) OVER (ORDER BY P.FILE_ID, P.C_CONTROL_POINT) END) * 24*60*60   DIFSEC, "
    "            (DATE_TIME - TO_DATE('20000101','YYYYMMDD')) * 24 * 60 * 60 SEGUNDOSPTO, "
    "            B.FECHAINGRESO "
    "       FROM USR_POSICIONAMIENTO.TRX_POSITIONING P, "
    "            GUI_LOTES B "
    "      WHERE P.FILE_ID = B.FILE_ID "
    "        AND B.FECHAINGRESO = TO_DATE('%s','YYYYMMDD')"
    "   ORDER BY FILE_ID, C_CONTROL_POINT "
    "   ) " %fechaingreso)

    curora.execute(sqlquery)

def puntos():
CREATE TABLE PUNTOSCONTROL AS 
    SELECT /*+ FULL(MT)*/
           MT.CODIGOLINEA CODIGOLINEA, 
		   MT.CODIGOTRAYECTO RAMAL, 
		   MT.NROTARJETAEXTERNO, 
		   MT.TIPOMAPPING, 
		   MT.CODIGOTRXTARJETA, 
		   MT.FECHATRX, 
		   MT.FECHAINGRESO, 
           MT.IDARCHIVOINTERCAMBIO,    
		   L.REF_EXT, 
		   P.C_CONTROL_POINT CONTROL_POINT_1, 
		   P.LONGITUDE LONGITUDPTO1, 
		   P.LATITUDE LATITUDPTO1, 
		   P.DATE_TIME FECHAPTO1
    FROM 
         (SELECT * FROM TEMP_LOTES_RAMALES WHERE L.SELECTTED = 'S') L, 
         USR_POSICIONAMIENTO.TRX_POSITIONING P
    WHERE MT.IDARCHIVOINTERCAMBIO = L.IDARCHIVOINTERCAMBIO
      AND CODIGOTIPOTRX = 19
        AND L.REF_EXT = P.FILE_ID
        AND MT.ID_POSICIONAMIENTO = P.C_CONTROL_POINT

def lotes(cursor):
    
#    PARA EJECUTAR EN ORACLE
#    esto crea la tabla 
     sqlquery = ("EXEC THE_LOTES_PROC(TO_DATE('20150501','YYYYMMDD'), TO_DATE('20150601','YYYYMMDD'), TO_DATE('20150501','YYYYMMDD'), TO_DATE('20150607','YYYYMMDD'))")
     
     curora.execute(sqlquery)
    
def LineaRamal():

#CREATE TABLE temp_lineas_ramales as 
#       SELECT /*+ full(mov)*/
#            mov.CODIGOENTIDAD                          AS ID_EMPRESA,
#            mov.CODIGOLINEA                          AS ID_LINEA,
#            mov.CODIGOTRAYECTO                          AS RAMAL,
#            COUNT(*) CANTIDAD_TRX
#       FROM USRNSSA.EXP_MOVIMIENTOTARJETA mov,
#            USRNSSA.LINEMT linea
#       WHERE mov.CODIGOLINEA = linea.LM_ID
#         AND LT_CODE = 'COL' -- Que sean líneas de colectivos
#         AND mov.CODIGOTIPOTRX = 19          -- Que sean usos 
#         AND mov.CODIGOSUBTIPOTRX IS NULL -- Que sean usos 
#         AND mov.FECHAINGRESO >= TO_DATE('20140801','YYYYMMDD') 
#         AND mov.FECHAINGRESO < TO_DATE('20140905','YYYYMMDD')
#         AND mov.FECHATRX >= TO_DATE('20140801','YYYYMMDD')
#         AND mov.FECHATRX <  TO_DATE('20140901','YYYYMMDD')
#    GROUP BY mov.CODIGOENTIDAD, mov.CODIGOLINEA, mov.CODIGOTRAYECTO  