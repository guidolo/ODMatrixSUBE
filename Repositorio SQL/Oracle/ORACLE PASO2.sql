


DECLARE

    v_empresa numeric := 0; 
    v_linea numeric := 0;
    v_ramal varchar2(5 byte) := '';
    v_contador numeric := 1;
    v_cantidad numeric := 0;
    
BEGIN   

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
            
            --CUENTA PARA SABER SI ESTÁ DUPLICADO -- creo que es posible que se haya duplicado porque se opero en dos linaeas o ramales diferentes dentro del mismo lote
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
    
    COMMIT;
END;

SELECT COUNT(*) FROM THE_LOTES WHERE SELECTTED IS NOT NULL
--28456

CREATE INDEX THE_LOTES_IDX1 ON THE_LOTES (IDARCHIVOINTERCAMBIO) TABLESPACE USRNSSA_IDX


DECLARE 
BEGIN
    DBMS_OUTPUT.PUT_LINE('A');
END;

--- REFILL 
DECLARE

    v_empresa numeric := 0; 
    v_linea numeric := 0;
    v_ramal varchar2(5 byte) := '';
    v_contador numeric := 1;
    v_cantidad numeric := 0;
    v_alreadyselected numeric := 0;
    
BEGIN   

    FOR I IN (SELECT CODIGOENTIDAD,CODIGOLINEA,RAMAL, IDARCHIVOINTERCAMBIO FROM the_lotes ORDER BY CODIGOENTIDAD,CODIGOLINEA,RAMAL, dbms_random.value) LOOP
        
         
        IF v_empresa = I.CODIGOENTIDAD AND v_linea = I.CODIGOLINEA AND v_ramal = I.RAMAL THEN
        
            v_contador := v_contador + 1;     
        
        ELSE
        
            v_contador := 1;
            v_empresa  := I.CODIGOENTIDAD;
            v_linea    := I.CODIGOLINEA;
            v_ramal    := I.RAMAL;
            
        
        END IF; 
        
        IF v_contador < 76 THEN
            
            --CUENTA PARA SABER SI ESTÁ DUPLICADO -- creo que es posible que se haya duplicado porque se opero en dos linaeas o ramales diferentes dentro del mismo lote
            SELECT COUNT(*) CANTIDAD, SUM(CASE WHEN SELECTTED IS NOT NULL THEN 1 ELSE 0 END) ALREADYSELECTED
            INTO v_cantidad, v_alreadyselected
            FROM the_lotes
            WHERE IDARCHIVOINTERCAMBIO = I.IDARCHIVOINTERCAMBIO;
            
            IF v_cantidad = 1 AND v_alreadyselected = 0 THEN 
            
                UPDATE the_lotes
                SET SELECTTED = '2'
                WHERE IDARCHIVOINTERCAMBIO = I.IDARCHIVOINTERCAMBIO
                  AND SELECTTED IS NULL;
                
            ELSE
                
                IF v_contador > 1 THEN
                    v_contador := v_contador - 1; 
                END IF;
            END IF;
            
        END IF; 
        
    
    END LOOP;
    
    COMMIT;
END;


ROLLBACK;


SELECT SELECTTED, COUNT(*) 
FROM THE_LOTES 
GROUP BY SELECTTED

SELECT COUNT(*) FROM PTOCONTROL201505

SELECT CODIGOENTIDAD,CODIGOLINEA,RAMAL, COUNT(*)
FROM the_lotes 
WHERE SELECTTED IS NOT NULL
GROUP BY CODIGOENTIDAD,CODIGOLINEA,RAMAL
ORDER BY COUNT(*) DESC




       );
        
        
        
        /***************************************************************/
        /**************** RAW PUNTOS CONTROL **************************/
        
        
      INSERT INTO PTOCONTROL(LINEA, 
                           RAMAL, 
                           FILE_ID, 
                           C_CONTROL_POINT, 
                           LONGITUD, 
                           LATITUD, 
                           FECHAPTO, 
                           ESTADO, 
                           DIFSEC, 
                           SEGUNDOSPTO, 
                           FECHAINGRESO) 
                           
CREATE TABLE PTOCONTROL AS                         
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
       )

               
    CREATE TABLE PTOCONTROL201505B AS
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
            AND SELECTTED = '2'
       ORDER BY FILE_ID, C_CONTROL_POINT )
       
UPDATE THE_LOTES
SET selectted = 'S'
WHERE FILE_ID IN (
                    SELECT FILE_ID
                    FROM PTOCONTROL201505
                    GROUP BY FILE_ID
                    )
                    --28456
                    
                    COMMIT