DROP TABLE temp_ramales

CREATE TABLE the_ramales as 
       SELECT /*+ full(mov)*/
            LIN.CODIGOLINEA                             LINEA,
            mov.CODIGOTRAYECTO                          RAMAL,
            LIN.DESCRIPCION,
            mov.CODIGOENTIDAD                          ID_EMPRESA,
            mov.CODIGOLINEA,
            AREAGEOGRAFICA,
            COUNT(*) CANTIDAD_TRX
       FROM USRNSSA.EXP_MOVIMIENTOTARJETA mov,
            USRNSSA.LINEMT LINEA,
            LINEA LIN
       WHERE mov.CODIGOLINEA = linea.LM_ID
         AND mov.CODIGOLINEA = LIN.IDLINEA
         AND LT_CODE = 'COL' -- Que sean líneas de colectivos
         AND mov.CODIGOTIPOTRX = 19          -- Que sean usos 
         AND mov.CODIGOSUBTIPOTRX IS NULL -- Que sean usos 
         AND mov.FECHAINGRESO >= TO_DATE('20150501','YYYYMMDD') 
         AND mov.FECHAINGRESO < TO_DATE('20150601','YYYYMMDD')
         AND mov.FECHATRX >= TO_DATE('20150101','YYYYMMDD')
         AND mov.FECHATRX <  TO_DATE('20150607','YYYYMMDD')
    GROUP BY  LIN.CODIGOLINEA, mov.CODIGOTRAYECTO, LIN.DESCRIPCION, mov.CODIGOENTIDAD,  mov.CODIGOLINEA,  AREAGEOGRAFICA            
