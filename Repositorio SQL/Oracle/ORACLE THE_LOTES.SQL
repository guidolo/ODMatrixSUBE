

DROP TABLE the_lotes 

CREATE TABLE the_lotes as
SELECT CODIGOENTIDAD,
       CODIGOLINEA,
       RAMAL,
       IDARCHIVOINTERCAMBIO,
       L.REF_EXT FILE_ID,
       CANTIDAD_TRX,
       MINFECHAINGRESO,
       MAXFECHAINGRESO
FROM          
( 
       SELECT /*+ full(mov)*/
            mov.CODIGOENTIDAD,
            mov.CODIGOLINEA,
            mov.CODIGOTRAYECTO                          AS RAMAL,
            IDARCHIVOINTERCAMBIO,
            COUNT(*) CANTIDAD_TRX,
            MIN(FECHAINGRESO) MINFECHAINGRESO,
            MAX(FECHAINGRESO) MAXFECHAINGRESO
       FROM USRNSSA.EXP_MOVIMIENTOTARJETA mov,
            USRNSSA.LINEMT linea
       WHERE mov.CODIGOLINEA = linea.LM_ID
         AND LT_CODE = 'COL' -- Que sean líneas de colectivos
         AND mov.CODIGOTIPOTRX = 19          -- Que sean usos 
         AND mov.CODIGOSUBTIPOTRX IS NULL -- Que sean usos 
         AND mov.FECHAINGRESO >= TO_DATE('20150501','YYYYMMDD') 
         AND mov.FECHAINGRESO < TO_DATE('20150607','YYYYMMDD')
         AND mov.FECHATRX >= TO_DATE('20150501','YYYYMMDD')
         AND mov.FECHATRX <  TO_DATE('20150601','YYYYMMDD')
    GROUP BY mov.CODIGOENTIDAD, mov.CODIGOLINEA, mov.CODIGOTRAYECTO, IDARCHIVOINTERCAMBIO
    )  A,
    USR_POSICIONAMIENTO.LOTE L
WHERE A.IDARCHIVOINTERCAMBIO = L.ID_LOTE    
            
ALTER TABLE the_lotes ADD
( selectted varchar2(1 byte)
 )

CREATE INDEX the_lotes_IDX1 ON the_lotes (IDARCHIVOINTERCAMBIO) TABLESPACE USRNSSA_IDX 
