# -*- coding: utf-8 -*-
"""
Created on Sat Mar 05 11:23:21 2016

@author: gsidoni
"""

import pandas.io.sql as sql
from shapely.wkt import loads as wkt_load
import pandas as pd
import numpy as np
from numpy import mod as mod
import Background as bk


#la siguiente funcion lacula mediante una funcion de POSTGIS la distancias minima entre cada una de las paradas de colectivo
#previamente calculados con los clusters


def recuperar_linea(linea, ramal, sentido,baseLineasRamales):
    return baseLineasRamales[(baseLineasRamales['linea'] == linea) & (baseLineasRamales['ramal'] == ramal) & (baseLineasRamales['sentido'] == sentido)]
   

def distaciaParadas(PosEngine):
    
#    PosEngine.execute("TRUNCATE TABLE dist_paradas")
    
    cursorLineas = PosEngine.execute("SELECT DISTINCT linea, ramal, sentido FROM PARADAS "
                                     " where linea >= '291' " 
                                     " ORDER BY LINEA, RAMAL, SENTIDO ")  
  
    for linea in cursorLineas.fetchall():   
        print('procesando codigolinea %s ramal %s sentido %s' % (linea.linea, linea.ramal, linea.sentido) )      
    
        sqlcode = ("  INSERT INTO dist_paradas (linea_origen, ramal_origen, sentido_origen, parada_origen, linea_destino, ramal_destino, sentido_destino, parada_destino, distancia_grados, distancia_metros ) "
                    " SELECT LINEA_ORIGEN, RAMAL_ORIGEN, SENTIDO_ORIGEN, PARADA_ORIDEN, LINEA_DESTINO, RAMAL_DESTINO, SENTIDO_DESTINO, PARADA_DESTINO, dist, "
                    "	(ST_DISTANCE( "
                    "				ST_Transform("
                    "						ST_GEOMFROMTEXT('POINT (' || P1LONGITUD || ' ' || P1LATITUD || ')',4326), 22182) "
                    "						, "
                    "				ST_Transform( "
                    "						ST_GEOMFROMTEXT('POINT (' || P2LONGITUD || ' ' || P2LATITUD || ')',4326), 22182) "
                    "						) ) distancia "
                    " FROM ( "
                    "	SELECT P1.LINEA LINEA_ORIGEN, P1.RAMAL RAMAL_ORIGEN, P1.SENTIDO SENTIDO_ORIGEN, P1.CLUSTERORD PARADA_ORIDEN, P2.LINEA  LINEA_DESTINO, P2.RAMAL RAMAL_DESTINO, P2.SENTIDO SENTIDO_DESTINO, P2.CLUSTERORD PARADA_DESTINO, "
                    "				 P1.LONGITUD P1LONGITUD, P1.LATITUD P1LATITUD, P2.LONGITUD P2LONGITUD, P2.LATITUD P2LATITUD, "
                    "				(ST_DISTANCE(ST_GEOMFROMTEXT('POINT (' || P1.LONGITUD || ' ' || P1.LATITUD || ')',4326), ST_GEOMFROMTEXT('POINT (' || P2.LONGITUD || ' ' || P2.LATITUD || ')',4326) ) )  DIST, "
                    "				 MIN(ST_DISTANCE(ST_GEOMFROMTEXT('POINT (' || P1.LONGITUD || ' ' || P1.LATITUD || ')',4326), ST_GEOMFROMTEXT('POINT (' || P2.LONGITUD || ' ' || P2.LATITUD || ')',4326) ) ) OVER (PARTITION BY  P1.LINEA, P1.RAMAL, P1.SENTIDO, P1.CLUSTERORD, P2.LINEA, P2.RAMAL, P2.SENTIDO)  MINDIST "
                    "	 FROM PARADAS P1, PARADAS P2  "
                    "	 WHERE (LPAD(P1.LINEA, 5, '0') || LPAD(P1.RAMAL,5,'0') || P1.SENTIDO) <> (LPAD(P2.LINEA, 5, '0') || LPAD(P2.RAMAL,5,'0') || P2.SENTIDO)  "
                    "	 	AND P1.LINEA = '%s' AND P1.RAMAL = '%s' AND P1.SENTIDO = '%s'  "
                    "	) A       "
                    " WHERE DIST = MINDIST " % (linea.linea, linea.ramal, linea.sentido) )
        
        PosEngine.execute(sqlcode)
        


#primero es asignar los sentidos a los puntos de control 
#segundo asignar a un viaje una parada.
#correr el agoritmo de deteccion de destino


def asignOrigen(PosEngine, lineaDesde, lineaHasta):

    print('-------- HELLO --- I will asign you the origin bus stops to every trip ----')
   
    cursorRamal = PosEngine.execute("SELECT a.LINEAMT, A.RAMALMT,A.LINEAGEO,A.RAMALGEO, sentido, geom FROM lineastrxgeo a, lineascole b where a.lineageo = b.linea2 and a.ramalgeo = ramal and a.baja is null  AND lineageo >= '%s' and lineageo < '%s' order by a.lineageo, a.ramalgeo" % (lineaDesde, lineaHasta))  
    
    if cursorRamal.rowcount > 0 :
        # por cada ramal de la linea
        for ramal in cursorRamal.fetchall():      
            
            lineamt = ramal[0]
            ramalmt = ramal[1]
            sentido = ramal[4]
            
            print('procesando codigolinea %s ramal %s sentido %s' % (lineamt,ramalmt, sentido) ) 
        
            #cargo las paradas para la linea - ramal - sentido
            sqlcode = ("SELECT clusterord, limiteinf FROM paradas where linea = '%s'and ramal = '%s' and sentido = '%s' order by clusterord" % (lineamt, ramalmt, sentido) )
            paradas = sql.read_sql(sqlcode  , PosEngine)  
            paradas = paradas.values.astype(np.float)
            
            if len(paradas) > 0:
                
                #recupero para cada viaje lo longitud y la latitud de los puntos de control anterior y siguiente, 
                #ademas se recupera el porcentaje del recorrido en que se encuentra el viaje desde el punto de control anterior al siguiente
                #finalmente se recupera el sentido del punto de control anterior
                sqlcode = ("SELECT B.NROTARJETAEXTERNO, B.CODIGOTRXTARJETA, A.LONGITUD longitudpto1, A.LATITUD latitudpto1, "
                           " C.LONGITUD longitudpto2, C.LATITUD latitudpto2, B.PORC_RECORRIDO "
                            " FROM  PTOCONTROL201505B A, THE_VIAJESMAYO B, PTOCONTROL201505B C "
                            " WHERE A.FILE_ID = B.FILE_ID "
                            "  AND A.C_CONTROL_POINT = B.C_CONTROL_POINT1  "
                            "  AND B.FILE_ID = C.FILE_ID "
                            "  AND B.C_CONTROL_POINT2 = C.C_CONTROL_POINT "                        
                            "  AND B.CODIGOLINEA = %s "
                            "  AND B.RAMAL = '%s' "
                            "  AND a.SENTIDO = '%s' "
                            "  AND B.DISTANCIA IS NULL  " % (lineamt, ramalmt, sentido))
    
                viajes = sql.read_sql(sqlcode  , PosEngine)            
           
                #paso a shapely
                shplLine = wkt_load(ramal[5])
                
                cantidad = len(viajes)
    
                for i, row in viajes.iterrows():                
                    if mod(i, cantidad/100) == 0:
                        print('Puntos procesados al: %i porciento' % int(i*100/cantidad))
                        
                    shplPoint1 = wkt_load("POINT(%s %s)" %  (row['longitudpto1'] , row['latitudpto1']))
                    projPoint1 = shplLine.project(shplPoint1, normalized=True)
                
                    shplPoint2 = wkt_load("POINT(%s %s)" %  (row['longitudpto2'] , row['latitudpto2']))
                    projPoint2 = shplLine.project(shplPoint2, normalized=True)
    
                    #la distancia está calculada como la proporcion del recorrido entre el pto de control anterior y siguiente
                    dist = projPoint1 + ((projPoint2 -projPoint1) * float(row['porc_recorrido']))
                    if dist > 0:
                        nroParada = paradas[paradas[:,1] < dist].argmax(axis=0)[0]
#                        print([dist,nroParada])
                        sql.execute("UPDATE THE_VIAJESMAYO SET PARADAORIGEN = %s, SENTIDO = '%s' WHERE NROTARJETAEXTERNO = '%s' AND CODIGOTRXTARJETA = '%s' " %(nroParada,sentido, row['nrotarjetaexterno'], int(row['codigotrxtarjeta'])), PosEngine)
            
            else:
                print('No tiene paradas asociadas')
    else:
        print('NO DATA available for this linea')
        
def asignDestiny(PosEngine, dia, nrotar, tst):
    
    print('-------- HELLO --- I will asign you YOUR DESTINY. ----')
    
    if tst == 1:
        cursorTarjetas = PosEngine.execute("SELECT DISTINCT NROTARJETAEXTERNO FROM THE_VIAJESMAYO_CRUCE%s WHERE NROTARJETAEXTERNO = '%s'" %(dia,nrotar))  
    else:
        cursorTarjetas = PosEngine.execute("SELECT DISTINCT NROTARJETAEXTERNO FROM THE_VIAJESMAYO_CRUCE%s" %dia)  
    print 'Load complete'
    cantidad = cursorTarjetas.rowcount
    j = 0
    if cursorTarjetas.rowcount > 0 :
        # por cada ramal de la linea
        for nroTarjeta in cursorTarjetas.fetchall():
            j = j + 1
            if mod(j, cantidad/1000) == 0:
                print('Tarjetas procesadas al: %i porciento' % int(j*100/cantidad))

            nroTarjetaExterno = nroTarjeta[0]

            sqlcode = ("SELECT codigolinea, ramal, sentido, paradaorigen parada, codigotrxtarjeta, file_id idarchivointercambio, "
                        " EXTRACT(EPOCH FROM FECHATRX) segundos "
                        " FROM THE_VIAJESMAYO_CRUCE%s  "
                        " WHERE NROTARJETAEXTERNO = '%s' "
                        " order by NROTARJETAEXTERNO, CODIGOTRXTARJETA " % (dia, nroTarjetaExterno) )
            
            viajes = sql.read_sql(sqlcode, PosEngine)
            
            primerViaje = 1
            row_iterator = viajes.iterrows()

            try:
                i, row = row_iterator.next()
            except:
                i = i + 1

            while i <= len(viajes) - 1:
                #print('tarjeta %s, codigotrxtarjeta: %i' % (nroTarjetaExterno, int(row['codigotrxtarjeta'])))

                #si es primer viaje de tarjeta guardo los datos del viaje para usar en el viaje final
                if primerViaje == 1:
                    lineaPrimer = row['codigolinea']
                    ramalPrimer = row['ramal']
                    sentidoPrimer = row['sentido']
                    paradaPrimer = row['parada']
                    UDprimer = row['idarchivointercambio']
                    primerViaje = 0
                    if tst == 1: print 0

                #si la parada es nula itero hasta encontrar un viaje que tenga parada
                while pd.isnull(row['parada']) and i <= len(viajes) - 1:
                    try:
                        if tst == 1: print 1
                        actRegistro(PosEngine, nroTarjetaExterno, int(row['codigotrxtarjeta']), 'E1', 0, dia)        
                        i, row = row_iterator.next()
                    except:
                        if tst == 1: print 11
                        i = i + 1

                            
                #obtengo el primer viaje     
                codigoTrxTarjeta = int(row['codigotrxtarjeta'])
                lineaOrigen = row['codigolinea']
                ramalOrigen = row['ramal']
                sentidoOrigen = row['sentido']
                paradaOrigen = row['parada']
                UDOrigen = row['idarchivointercambio']
                segOrigen = row['segundos']
                                    
                #si hay un viaje mas
                if i < len(viajes) - 1:
                    if tst == 1: print 2                    
                   
                    #recupero prox viaje	
                    i, row = row_iterator.next()
                    
                    #compruebo que no sea un multiviaje
                    #para que sea multiviaje tienen que tener mismo Ud y diferencia meor a 180 segundos
                    while UDOrigen == row['idarchivointercambio'] and (row['segundos'] - segOrigen) < 180 and i <= len(viajes) - 1:
                        try:
                            actRegistro(PosEngine, nroTarjetaExterno, int(row['codigotrxtarjeta']), 'EM', 0,dia)        
                            if tst == 1: print 4                            
                            i, row = row_iterator.next()                            
                        except:
                            i = i + 1
                            if tst == 1: print 5
                            
                    #verifoco que no sea el fin                    
                    if i <= len(viajes) - 1:                        
                        if tst == 1: print 6
                        #verifico que la parada no sea nula
                        if not pd.isnull(row['parada']):
                            #si no es nula, puede determinarse el destino 
                            if tst == 1: print 7
                            paradaDestino = recParadaDestino(PosEngine, lineaOrigen, ramalOrigen, sentidoOrigen, row['codigolinea'], row['ramal'], row['sentido'], row['parada'])
    
                            actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'P', paradaDestino, dia)        
    
                        else:
                            if tst == 1: print 8
                            #si la parada de origen es nula, no puede determinarse el destino  --EEROR 3
                            actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'E3', 0, dia)    
                    else:
                        if tst == 1: print 9
                        #si llego al fin, significa que el multiviaje era el fin
                        #verifico que no haya sido el unico viaje
                        if primerViaje == 0:
                            if tst == 1: print 10
                            
                            #verifico que el primer viaje y el ultimo no sean iguales
                            if UDprimer <> row['idarchivointercambio']:
                                
                                #verifico que el primer viaje no tenga la parada nula
                                if not pd.isnull(paradaPrimer):
                                    if tst == 1: print 11
                                    paradaDestino = recParadaDestino(PosEngine, lineaOrigen, ramalOrigen, sentidoOrigen, lineaPrimer, ramalPrimer, sentidoPrimer, paradaPrimer)
                                    
                                    actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'P', paradaDestino,dia)        
        
                                else:
                                    if tst == 1: print 12
                                    #si el primer viaje tiene parada nula, no puede identificarse el destino
                                    actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'E4', 0,dia)        
                            else:
                                #si son iguales, solo hubo un multivije
                                actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'E5', 0,dia)        
                                
                        else:
                            if tst == 1: print 13
                            actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'E2', 0,dia)   
                else:
                    if tst == 1: print 14
                    #si no hay un viaje mas significa que puedo usar el primer viaje como destino
                    i = i + 1
                    
                    if not pd.isnull(row['parada']):
                        
                        #verifico que no haya sido el unico viaje
                        if primerViaje == 0:
                            if tst == 1: print 15
                                
                            #verifico que el primer viaje y el ultimo no sean iguales
                            if UDprimer <> row['idarchivointercambio']:                                                      
                                
                                #verifico que el primer viaje no tenga la parada nula
                                if not pd.isnull(paradaPrimer):
                                    if tst == 1: print 16
                                    paradaDestino = recParadaDestino(PosEngine, lineaOrigen, ramalOrigen, sentidoOrigen, lineaPrimer, ramalPrimer, sentidoPrimer, paradaPrimer)
                                    
                                    actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'P', paradaDestino,dia)        
        
                                else:
                                    if tst == 1: print 17
                                    #si el primer viaje tiene parada nula, no puede identificarse el destino
                                    actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'E4', 0,dia)        
                            else:
                                actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'E5', 0,dia)        
                        else:
                            if tst == 1: print 18
                            actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'E2', 0,dia)        
                    else:
                        if tst == 1: print 19
                        actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, 'E6', 0,dia)        


    
    
                
def recParadaDestino(PosEngine, lineaOrigen, ramalOrigen, sentidoOrigen, lineaDestino, ramalDestino, sentidoDestino, paradaDestino):
    
    sqlcode = (" SELECT parada_destino "
                " FROM DIST_PARADAS "
                " WHERE LINEA_ORIGEN = '%s' AND RAMAL_ORIGEN = '%s' AND SENTIDO_ORIGEN = '%s' AND PARADA_ORIGEN = %i "
                "  AND LINEA_DESTINO = '%s' AND RAMAL_DESTINO = '%s' AND SENTIDO_DESTINO = '%s' " % (int(lineaDestino), ramalDestino, sentidoDestino, int(paradaDestino), int(lineaOrigen), ramalOrigen, sentidoOrigen ) )

    dfParadaDest = sql.read_sql(sqlcode, PosEngine)
    
    try:
        paradaDestino = int(dfParadaDest['parada_destino'][0])
    except:
        paradaDestino = -1
        
    return paradaDestino
    
def actRegistro(PosEngine, nroTarjetaExterno, codigoTrxTarjeta, procesado, paradaDestino, dia): 
    try:
        #print ("UPDATE THE_VIAJESMAYO SET PROCESADO = '%s', PARADADESTIN = %i WHERE NROTARJETAEXTERNO = '%s' AND CODIGOTRXTARJETA = %i" %(procesado, paradaDestino, nroTarjetaExterno, codigoTrxTarjeta))
        sql.execute("UPDATE THE_VIAJESMAYO_CRUCE%s SET PROCESADO = '%s', PARADADESTIN = %i WHERE NROTARJETAEXTERNO = '%s' AND CODIGOTRXTARJETA = %i" %(dia, procesado, paradaDestino, nroTarjetaExterno, codigoTrxTarjeta), PosEngine)
        return 1
    except:
        print 'Error al actualizar'
        return 0
    
        
def addFechaDestino(PosEngine):
    cursorLineas = PosEngine.execute("SELECT DISTINCT linea, ramal, sentido FROM PARADAS ORDER BY LINEA, RAMAL, SENTIDO")  
    baseLineasRamales = bk.cargar_lineas(PosEngine)
    
    for curLinea in cursorLineas.fetchall():   
        lineamt = curLinea.linea
        ramalmt = curLinea.ramal
        sentido = curLinea.sentido
        [ramal, linea] = bk.ramalGeo(PosEngine, int(lineamt) ,ramalmt)
        print('procesando codigolinea %s ramal %s sentido %s' % (linea, ramal, sentido)) 
        
#        recupero el shape de la linea
        lineasCole = recuperar_linea(linea, ramal, sentido, baseLineasRamales)
        shplLineStr = wkt_load(lineasCole['geom'].values[0])
        
#        recuoero todos los viajes que tienen un procesado P para esa linea
#        me quedo con los segundospto de origen, parada destino, file_id
#        recupero la parada de destino y su centroide
        
        sqlcode = (" SELECT nrotarjetaexterno, codigotrxtarjeta, file_id,   "
                   "        extract(epoch from cast(fechatrx as timestamp with time zone)) - 946695600 segundospto, " #SE suma 946695600 que es la diferencia en segundos desde 1970 a 2000
                   "        c_control_point2, paradadestin, centroide "
                    " FROM THE_VIAJESMAYO A, PARADAS B "
                    " WHERE A.CODIGOLINEA = CAST(B.LINEA AS INTEGER) "
                    " 	AND A.RAMAL = B.RAMAL "
                    " 	AND A.SENTIDO = B.SENTIDO  "
                    " 	AND A.PARADADESTIN = B.CLUSTERORD  "
                    "  AND PROCESADO = 'P'"
                    "  AND A.CODIGOLINEA = %s "
                    "  AND A.RAMAL = '%s' "
                    "  AND A.SENTIDO = '%s' " % (lineamt, ramalmt, sentido) )
        
        viajes = sql.read_sql(sqlcode, PosEngine)
        
        for i, row in viajes.iterrows():
            
            controlPointOrigen = int(row.c_control_point2)
            centroideParada = row.centroide
            file_id = int(row.file_id)
            segundospto = row.segundospto
            
#           para este viaje recupero los puntos de control mayores a los segundospto
        
            sqlcode = (" 	SELECT segundospto, c_control_point,   "
                       "          TO_DATE('20000101 00:00:00', 'YYYYMMDD HH24:MI:SS') + SEGUNDOSPTO * INTERVAL '1 SECOND' fechadestino, "
                       "          latitud, longitud "
                        " FROM ptocontrol201505b "
                        " WHERE FILE_ID = %s " 
                        " AND  SEGUNDOSPTO > %s "
                        " AND C_CONTROL_POINT > %s "
                        " ORDER BY C_CONTROL_POINT " % (file_id, segundospto, controlPointOrigen) )
            
            ptosControl = sql.read_sql(sqlcode, PosEngine)  
            
            diferencia = 1
            
            for j, rowpto in ptosControl.iterrows():
                
#                algunos puntos gps vienen en cero                
                if rowpto['longitud'] < -57 and rowpto['latitud'] < -33:
    #               proyecto los puntos de conrtol, y calculo la diferencia proyectada contra el centroide de la parada
    #               mientras la distancias se achique sigo, cuando se agranda corto
        
                    shplPointaux = wkt_load("POINT(%s %s)" %  (rowpto['longitud'], rowpto['latitud'])) 
                    shplProj  = shplLineStr.project(shplPointaux, normalized=True)
                    if (centroideParada - shplProj.real) < diferencia and (centroideParada - shplProj.real) > 0:
                        diferencia = centroideParada - shplProj.real
                    else:
                        break
                
#               actualizo el registro en viaje
                sql.execute("UPDATE THE_VIAJESMAYO SET C_CONTROL_POINT_DEST = %s, FECHA_DEST = to_timestamp('%s','YYYY-MM-DD HH24:MI:SS') WHERE NROTARJETAEXTERNO = '%s' AND CODIGOTRXTARJETA = '%s' " %(rowpto['c_control_point'], rowpto['fechadestino'], row['nrotarjetaexterno'], int(row['codigotrxtarjeta'])), PosEngine)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    