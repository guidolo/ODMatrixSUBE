CREATE OR REPLACE PROCEDURE USRNSSA.THE_LOTE_PROC(p_fechaIngresoDesde IN DATE, p_fechaIngresoHasta IN DATE, p_fechaTrxDesde IN DATE, p_fechaTrxHasta IN DATE)
AS

/*
Creaci{on:
Modificaciones:
			   04/10/2013 V1  --Definicion de modificaciones
			   
					   				    

*/
--variables fijas 
codigoError    			   		  NUMBER;
mensajeError 					  VARCHAR(300);
fechaInicioProcedimiento 		  DATE;
fechaFinProcedimiento 			  DATE;
e_error_usuario                   EXCEPTION;
v_procedimiento                   VARCHAR(50);
v_version                         VARCHAR(10);

--variables fechas
v_fechaIngresoDesde 			  DATE;
v_fechaIngresoHasta 			  DATE;
v_fechaTrxDesde                   DATE;
v_fechaTrxHasta					  DATE;

--variables especiales 
    v_linea numeric := 0;
    v_ramal varchar2(5 byte) := '';
    v_contador numeric := 1;
    v_cantidad numeric := 0;
    v_empresa numeric := 0; 
--cursores
 --CURSOR SALDO IS

	
BEGIN


	/******************************************************************/
	/***************** INICIALIZACION VARIABLES ***********************/
	/******************************************************************/
	fechaInicioProcedimiento := SYSDATE;
    v_procedimiento     := 'THE_LOTE_PROC';
    v_version	        := '1';

	v_fechaIngresoDesde  := p_fechaIngresoDesde; 
    v_fechaIngresoHasta  := p_fechaIngresoHasta;
    v_fechaTrxDesde      := p_fechaTrxDesde;
    v_fechaTrxHasta      := p_fechaTrxHasta;
    
	/******************************************************************/
    /***************** CONTROLES ****************************************/
    /******************************************************************/
    
 
     /******************************************************************/
	/***************** BACKUP *****************************************/
	/******************************************************************/


	/******************************************************************/
	/****************** NUCLEO ****************************************/
	/******************************************************************/

    EXECUTE IMMEDIATE 'TRUNCATE TABLE TEMP_LOTES_RAMALES'; 


    INSERT INTO THE_LOTES (CODIGOENTIDAD, CODIGOLINEA, RAMAL, IDARCHIVOINTERCAMBIO, FILE_ID, CANTIDAD_TRX, MINFECHAINGRESO, MAXFECHAINGRESO)
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
             AND mov.FECHAINGRESO >= v_fechaIngresoDesde 
             AND mov.FECHAINGRESO <  v_fechaIngresoHasta
             AND mov.FECHATRX     >= v_fechaTrxDesde
             AND mov.FECHATRX     <  v_fechaTrxHasta
        GROUP BY mov.CODIGOENTIDAD, mov.CODIGOLINEA, mov.CODIGOTRAYECTO, IDARCHIVOINTERCAMBIO
        )  A,
        USR_POSICIONAMIENTO.LOTE L
    WHERE A.IDARCHIVOINTERCAMBIO = L.ID_LOTE;
    

       FOR I IN (SELECT CODIGOENTIDAD,CODIGOLINEA,RAMAL, IDARCHIVOINTERCAMBIO FROM the_lotes ORDER BY CODIGOENTIDAD,CODIGOLINEA,RAMAL, dbms_random.value) LOOP
        
        IF v_empresa = I.CODIGOENTIDAD AND v_linea = I.CODIGOLINEA AND v_ramal = I.RAMAL THEN
        
            v_contador := v_contador + 1;     
        
        ELSE
        
            v_contador := 1;
            v_empresa  := I.CODIGOENTIDAD;
            v_linea    := I.CODIGOLINEA;
            v_ramal    := I.RAMAL;
            
        
        END IF; 
        
        IF v_contador < 26 THEN
                    
            SELECT COUNT(*)
            INTO v_cantidad
            FROM the_lotes
            WHERE IDARCHIVOINTERCAMBIO = I.IDARCHIVOINTERCAMBIO;
            
            IF v_cantidad = 1 THEN 
            
                UPDATE the_lotes
                SET SELECTTED = 'S'
                WHERE IDARCHIVOINTERCAMBIO = I.IDARCHIVOINTERCAMBIO;
                
            ELSE
                
                IF v_contador > 1 THEN
                    v_contador := v_contador - 1; 
                END IF;
            END IF;
            
        END IF; 
        
    
    END LOOP;
    


    INSERT INTO PTOCONTROL201505 ( CODIGOLINEA, RAMAL, FILE_ID, C_CONTROL_POINT, LONGITUD, LATITUD, FECHAPTO, ESTADO, DIFSEC, SEGUNDOSPTO, MINFECHAINGRESO )                   
     SELECT CODIGOLINEA, 
            RAMAL, 
            FILE_ID, 
             C_CONTROL_POINT,  
             LONGITUD,  
             LATITUD,   
             FECHAPTO,  
            (CASE WHEN DIFSEC > 235 AND DIFSEC < 245 THEN 'S' ELSE 'N' END) ESTADO,  
            DIFSEC, 
            SEGUNDOSPTO, 
            MINFECHAINGRESO 
      FROM 
        (SELECT B.CODIGOLINEA,  
                B.RAMAL,  
                P.FILE_ID, 
                C_CONTROL_POINT, 
                LONGITUDE LONGITUD, 
                LATITUDE LATITUD,   
                DATE_TIME FECHAPTO, 
                (CASE WHEN LAG(P.file_id, 1) OVER (ORDER BY P.FILE_ID, P.C_CONTROL_POINT) =  P.file_id  THEN  DATE_TIME - LAG(DATE_TIME, 1) OVER (ORDER BY P.FILE_ID, P.C_CONTROL_POINT) END) * 24*60*60   DIFSEC, 
                (DATE_TIME - TO_DATE('20000101','YYYYMMDD')) * 24 * 60 * 60 SEGUNDOSPTO, 
                B.MINFECHAINGRESO 
           FROM USR_POSICIONAMIENTO.TRX_POSITIONING P, 
                THE_LOTES B 
          WHERE P.FILE_ID = B.FILE_ID 
            AND SELECTTED = 'S'
       ORDER BY FILE_ID, C_CONTROL_POINT 
       );
       
       
     COMMIT;


    /***************************************************************/
    /************* LOG Y EJECUCIONES  ******************************/
    /***************************************************************/


   fechaFinProcedimiento := SYSDATE;
   --Guardo info de la ejecución y hago commit si corresponde
   INSERT INTO EXP_EJEC ( FECHA_INGRESO_INICIO, FECHA_INGRESO_FIN, FECHA_TRX_FIN, FECHA_INICIO, FECHA_FIN, PROCEDIMIENTO, VERSION )
   VALUES ( v_fechaIngresoDesde, v_fechaIngresoHasta, v_fechaTrxHasta, fechaInicioProcedimiento, fechaFinProcedimiento, v_procedimiento, v_version);

   COMMIT;



EXCEPTION
  WHEN e_error_usuario THEN
    codigoError := SQLCODE;
    ROLLBACK; -- Para evitar que lo procesado hasta el momento se guarde
    INSERT INTO EXP_ERROR (CODIGO, MENSAJE, FECHA,PROCEDIMIENTO)
    VALUES (codigoError,mensajeError,SYSDATE,v_procedimiento );
    COMMIT;
    
  WHEN OTHERS THEN
   codigoError := SQLCODE;
   mensajeError := SQLERRM(codigoError);
   ROLLBACK; -- Para evitar que lo procesado hasta el momento se guarde
   INSERT INTO EXP_ERROR (CODIGO, MENSAJE, FECHA,PROCEDIMIENTO)
   VALUES (codigoError, mensajeError, SYSDATE,v_procedimiento );
   COMMIT;



END THE_LOTE_PROC;
/