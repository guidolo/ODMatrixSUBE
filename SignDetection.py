# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 15:05:02 2015

@author: GSIDONI
"""
import sys
import pandas.io.sql as sql
import pandas as pd
import numpy as np
from shapely.wkt import loads as wkt_load
from shapely.geometry import Point
from itertools import cycle
from numpy import mod as mod
import os
import matplotlib.pyplot as plt
os.chdir('i:\\tesis')

#cargo repositorios propios
sys.path.insert(0, 'i:\\tesis\\Repositorio Python\\GEO\\')
from lineasEnPuntos import distancia as distancia
import Background as bk
import shapely


#==============================================================================
# Bienvenidos al facinante mundo de la detección del sentido de los puntos de control 
#==============================================================================

            
#==============================================================================
#  PASO 4: RECORRO LOS PUNTOS DE CONTROL --
#            se recorren para ver en su conjunto para que sentido se dirigen 
#==============================================================================


def recuperar_linea(linea, ramal, sentido,baseLineasRamales):
    return baseLineasRamales[(baseLineasRamales['linea'] == linea) & (baseLineasRamales['ramal'] == ramal) & (baseLineasRamales['sentido'] == sentido)]

def sentido_init(linea, ramal, PtoControl, baseLineasRamales, tst):
    #parte 1: recorro os puntos de control en orden y voy poniendo un sentido inicial según se encuetren mas cerca de uno o de otro
    #           en caso de que estén quidistantes se asigna un sentido aleatorio
    #           además se hacen las mediciones a los sentidos de IDA y VUELTA que luego serán usados en el paso 2
    
#    print('Inicializando Sentido...') 
    
    if len(np.unique(PtoControl.file_id)) != 1:
        print('ERROR: solo es posible procesar un FILE_ID')
        exit(0)
    
#    lineasColeIda = sql.read_sql("SELECT linea, ramal, sentido, geom  FROM LineasCole WHERE LINEA = %s AND RAMAL = '%s' AND SENTIDO = 'I'" %(linea, ramal), consqliteBase  )
#    lineasColeVuelta = sql.read_sql("SELECT linea, ramal, sentido, geom  FROM LineasCole WHERE LINEA = %s AND RAMAL = '%s' AND SENTIDO = 'V'" %(linea, ramal), consqliteBase  )
    
    lineasColeIda = recuperar_linea(linea, ramal, 'I', baseLineasRamales)
    lineasColeVuelta = recuperar_linea(linea, ramal, 'V', baseLineasRamales)
    
    shplLineStrIda = wkt_load(lineasColeIda['geom'].values[0])
    shplLineStrVuelta = wkt_load(lineasColeVuelta['geom'].values[0])
    
    sentidoAleatorio = 'I'

    for i, rowpto in PtoControl.iterrows():
        
        shplPointaux = wkt_load("POINT(%s %s)" %  (rowpto['longitud'], rowpto['latitud']))
        
#        shplProjIda = shplLineStrIda.project(Point(rowpto['longitud'], rowpto['latitud']))
        shplProjIda = shplLineStrIda.project(shplPointaux, normalized=True)
        shplPoint = shplLineStrIda.interpolate(shplProjIda, normalized=True)
        distanciaIda = distancia(rowpto['longitud'], rowpto['latitud'], shplPoint.x, shplPoint.y) * 1000
        PtoControl.loc[i,'DistAIda'] = distanciaIda 
        PtoControl.loc[i,'MilePostIda'] = shplProjIda
            
#        shplProjVuelta = shplLineStrVuelta.project(Point(rowpto['longitud'], rowpto['latitud']))
        shplProjVuelta = shplLineStrVuelta.project(shplPointaux, normalized=True)        
        shplPoint = shplLineStrVuelta.interpolate(shplProjVuelta, normalized=True)
        distanciaVuelta = distancia(rowpto['longitud'], rowpto['latitud'], shplPoint.x, shplPoint.y) * 1000
        PtoControl.loc[i,'DistAVuelta'] = distanciaVuelta
        PtoControl.loc[i,'MilePostVuelta'] = shplProjVuelta
        
        if distanciaIda == distanciaVuelta:
            PtoControl.loc[i,'Sentido'] = sentidoAleatorio
            sentidoAleatorio = 'V' if sentidoAleatorio == 'I' else 'I'
        else:
            if distanciaIda < distanciaVuelta:
                PtoControl.loc[i,'Sentido'] = 'I'
            else:
                PtoControl.loc[i,'Sentido'] = 'V'
        
        if tst == 1:
            PtoControl.loc[i,'SentidoHis'] = PtoControl.loc[i,'Sentido']
        else:
            PtoControl.loc[i,'SentidoHis'] = ''
        
        PtoControl.loc[i,'MilePost'] =  shplProjIda if PtoControl['Sentido'][i] == 'I' else shplProjVuelta

    return PtoControl

#==============================================================================
#     
#==============================================================================

def sentido_asignar_sentido(PtoControl, tst):
    #parte 2: asigno el sentido según los valores de las proyecciones de pto de control actual y siguiente
    #para cada uno de los file_id que hay dentro de los puntos de control.

#    print('Asignando sentidos en grupo...') 

    cambio = True #variable que indica se hubo cambios en la iteración. Si no hay más cambios el algoritmo termina
    maxiter  = 20 #maxma cantidad de iteraciones
    maxRepeticion = 3  #cantidad de ciclos en donde se cambian la misma cantidad que el ciclo pasado
    iter = 0 # contador de la posición de la iteracion
    cantRepeticion = 0 #cuantas veces se cambiaron la misma cantidad de puntos 
    cantCambios = 0
    
    while cambio and iter < maxiter and cantRepeticion < maxRepeticion:
        iter = iter + 1 
        cambio = False
        cantCambiosAnterior = cantCambios
        cantCambios = 0
    
        #    recorro todos los puntos de control
        for i, rowpto in PtoControl.iterrows():
            sentido = rowpto.Sentido
            
            #me paro es un punto y miro el proximo del mismo sentido
            j=i+1
            while j < len(PtoControl) and PtoControl['Sentido'][j] <> sentido:
                j=j+1
            
            # En caso de que llegue al final y no encuentre otro de igual sentido, salteo el punto
            if j == len(PtoControl):
                break
            
            #El mile post del siguiente punto de control de igual sentido debe ser mayor al mail post actual. En caso contrario se cambia de sentido
            if PtoControl['MilePost'][j] < rowpto.MilePost or (PtoControl['MilePost'][j] > rowpto.MilePost and PtoControl['segundospto'][j] - rowpto.segundospto > 30*60):
                # Cambio de sentido
                PtoControl.loc[i,'Sentido'] = 'V' if sentido == 'I' else 'I'
                if tst==1:
                    PtoControl.loc[i,'SentidoHis'] =  '%s -a %s %s' % (PtoControl.loc[i,'SentidoHis'], iter, PtoControl.loc[i,'Sentido'])                    
                PtoControl.loc[i,'MilePost'] = PtoControl.loc[i,'MilePostVuelta'] if sentido =='I' else PtoControl.loc[i,'MilePostIda']
                cambio = True            
                cantCambios = cantCambios + 1
            
#        print('     Iteración %s: cantidad de cambios: %s' % (iter, cantCambios))
        cantRepeticion = cantRepeticion + 1 if cantCambiosAnterior == cantCambios else 0    
        
    return PtoControl

#==============================================================================
# 
#==============================================================================

def sentido_Sueltos(PtoControl, tst):
    #parte 3:  En caso de que hayan quedado un punto en el sentido opuesto rodeado por puntos de otro signo se le cambia el signo

#    print('Corrigiendo segun anterior y siguiente...') 

    cambio = True #variable que indica se hubo cambios en la iteración. Si no hay más cambios el algoritmo termina    
    iter = 0 # contador de la posición de la iteracion
    maxiter  = 20 #maxma cantidad de iteraciones
    cantCambios = 0
    while cambio and iter < maxiter:
        iter = iter + 1 
        cambio = False
        cantCambios = 0
        
        #    recorro todos los puntos de control
        for i, rowpto in PtoControl.iterrows():
            
            j = i + 1 #punto de control siguiente      
            h = i - 1 #punto de control anterior
            
            # en caso de que no haya punto anterior salteo el punto
            if h < 0:
                continue
            
            #si no hay siguiente termino la iteracion
            if j == len(PtoControl):
                break
            
            SegundosEntrePuntos = 60*4+10  #4 minutos mas 10 segundos en caso de error
            sentido = rowpto.Sentido
            sentidoAnterior = PtoControl['Sentido'][h]
            sentidoSiguiente  = PtoControl['Sentido'][j]
            SegundosAlAnterior = rowpto.segundospto - PtoControl['segundospto'][h]
            SegundosAlSiguiente =  PtoControl['segundospto'][j] - rowpto.segundospto
            
            #si el anterior y el siguiente tienen distinto signo y cumplen con el tiempo entre puntos consecutivos, se le cambia el signo al actual
            if sentidoAnterior <> rowpto.Sentido and sentidoSiguiente <> rowpto.Sentido and SegundosAlAnterior < SegundosEntrePuntos and SegundosAlSiguiente < SegundosEntrePuntos:
                # Cambio de sentido
                PtoControl.loc[i,'Sentido'] = 'V' if sentido == 'I' else 'I'
                if tst == 1:
                    PtoControl.loc[i,'SentidoHis'] =  '%s -b %s %s' % (PtoControl.loc[i,'SentidoHis'], iter, PtoControl.loc[i,'Sentido'])
                PtoControl.loc[i,'MilePost'] = PtoControl.loc[i,'MilePostVuelta'] if sentido =='I' else PtoControl.loc[i,'MilePostIda']
                cambio = True            
                cantCambios = cantCambios + 1
        
#        print('     Iteración %s: cantidad de cambios: %s' % (iter, cantCambios))
    return PtoControl
    

    

#==============================================================================
#FUNCIONES AUXILIARES DE CARGA Y RECUPERACION DE DATOS
#==============================================================================
    
  
def recuperar_prox_lotes(PosEngine, lineaDesde, lineaHasta):
    
    sqlquery = ("SELECT CODIGOLINEA, RAMAL, FILE_ID "
                " FROM THE_LOTES  "
                " WHERE CODIGOLINEA >= %s "
                "   AND CODIGOLINEA < %s "
                " AND PROCESADO IS NULL "
                " AND SELECTTED IS NOT NULL "
                " ORDER BY file_id LIMIT 1" %(lineaDesde, lineaHasta) )
    
    pdfileid = sql.read_sql(sqlquery , PosEngine)
    if len(pdfileid) > 0:
        fileid = pdfileid.values[0][2]
        if fileid != 0:
            #marco los lotes que se están procesando con T
            sql.execute("UPDATE THE_LOTES SET PROCESADO =  'T' WHERE FILE_ID = %s" %(fileid), PosEngine)
        #devuelve file_id, codigolinea, ramal
        return [fileid, pdfileid.values[0][0], pdfileid.values[0][1]]
    else:
        return [0,0,0]
            

def recuperar_lote(PosEngine, fileid):
    return sql.read_sql("SELECT CODIGOLINEA, RAMAL, FILE_ID, C_CONTROL_POINT, LONGITUD, LATITUD, FECHAPTO, SEGUNDOSPTO FROM PTOCONTROL201505 WHERE FILE_ID = %s ORDER BY C_CONTROL_POINT" %fileid, PosEngine)

def actualizar_sentidos(PosEngine):
    try:    
        resultado = sql.execute("UPDATE PTOCONTROL201505B A SET SENTIDO = B.SENTIDO FROM SENTIDO B WHERE A.FILE_ID = B.FILE_ID AND A.C_CONTROL_POINT = B.C_CONTROL_POINT", PosEngine)
        return 'OK'
    except:
        return sys.exc_info()[1]

#==============================================================================
#     EJECUTOR
#==============================================================================

def sentido_ejecutar(PosEngine, lineaDesde, lineaHasta, tst):
    from time import time
    
    vervose = 'N'
    print('Inicio de sign detection...')
    print('HOLA!!!!!!!!')
    print('Este proceso va a guardar en la tabla SENTIDO !!!!!')
    
#    connect = PosEngine.connect()
        
    baseLineasRamales = bk.cargar_lineas(PosEngine)
    print('    Lineas recuperdas')  
    print('    Leyendo Lotes a procesar')       
    print('    __INICIO LOOP__')

    PtoControlTotal = pd.DataFrame()
    cantidadErrores = 0
    i = 0
    lineamt = 0
    ramalmt = 0
    #recupero el file_id, la lineamt y el ramalmt
    [fileid,lineamt,ramalmt] = recuperar_prox_lotes(PosEngine, lineaDesde, lineaHasta)
    while fileid != 0:
        print(fileid)
        i = i + 1
        
#        muestra evolución de la ejecución cada 1%
#        if mod(i, cantidad/10000) == 0:
#            print('Lotes procesados al: %f porciento. LotesOK: %s Errores: %s' %((i*100/cantidad), cantidadLotes, cantidadErrores))
        print('cantidad de lostes procesados %i, errores %s' %(i,cantidadErrores))

#        t0 = time()
                                
        PtoControl = sql.read_sql(" SELECT FILE_ID, C_CONTROL_POINT, LONGITUD, LATITUD, SEGUNDOSPTO "
                                " FROM PTOCONTROL201505B "
                                " WHERE FILE_ID = %s "
                                " ORDER BY C_CONTROL_POINT" % int(fileid), PosEngine)                                
                                
        PtoControl.columns = ['file_id','c_control_point','longitud','latitud','segundospto']    
#        print('carga lotes %.2fs' % (time() - t0))
#        t0 = time()        
        
        if len(PtoControl) > 0:
            #recupero la linea y el ramal
#            lineamt = PtoControl.linea[0]
#            ramalmt = PtoControl.ramal[0]
            [ramal, linea] = bk.ramalGeo(PosEngine, int(lineamt) ,ramalmt)
            PtoControl.loc[:,'linea'] = int(linea)
            PtoControl.loc[:,'ramal'] = ramal
#            print('carga ramal %.2fs' % (time() - t0))
            print('linea %s, ramaltrx %s, ramal %s' %(linea, ramalmt, ramal.decode('latin-1') ))
            estadoFileId = 'S'
            
            if ramal != '0':
                try:
#                    t0 = time()
                    PtoControl = sentido_init(linea, ramal, PtoControl, baseLineasRamales, tst)  
#                    print('sentido init %.2fs' % (time() - t0))
#                    t0 = time()
                    PtoControl = sentido_asignar_sentido(PtoControl, tst)
#                    print('sentido asignar sentido %.2fs' % (time() - t0))
#                    t0 = time()
                    PtoControl = sentido_Sueltos(PtoControl, tst)
#                    print('sentido_sueltos %.2fs' % (time() - t0))
                except:
                    print "ERROR - en algoritmos de asignacion: code 1:", sys.exc_info()[0]
#                    error = pd.DataFrame([fileid], columns=['fileid'])
                    cantidadErrores = cantidadErrores + 1 
#                    error.to_sql('error', con=PosEngine,  if_exists='append')
                    estadoFileId = '1'
            else: 
                print ('ERROR - Ramal CERO: code 2')
                cantidadErrores = cantidadErrores + 1
                estadoFileId = '2'
            
            if estadoFileId == 'S':
                # marco al lote como procesado

                try:
                    if tst == 0:                    
    #                        t0 = time()
                        del PtoControl['DistAIda']
                        del PtoControl['MilePostIda']
                        del PtoControl['DistAVuelta']
                        del PtoControl['MilePostVuelta']
                        del PtoControl['SentidoHis']
                        del PtoControl['longitud']
                        del PtoControl['latitud']
                        del PtoControl['segundospto']
                        PtoControl.columns = ['file_id','c_control_point','linea','ramal','sentido','milepost']    
                        PtoControl.to_sql('sentido', con=PosEngine, if_exists='append')
                    else:
                        PtoControl.columns = ['file_id','c_control_point','longitud','latitud','segundospto', 'linea','ramal','distaida','milepostida','distavuelta','milepostvuelta','sentido','sentidohis','milepost']    
                        PtoControl.to_sql('sentidotest', con=PosEngine, if_exists='append')
    #                        print('volcado de datos %.2fs' % (time() - t0))
                except:
                    print "ERROR - error al grabar: code 3:", sys.exc_info()[0]
                    cantidadErrores = cantidadErrores + 1
                    estadoFileId = '3'
        else:
            print "ERROR - sin datos para lote: code 4:", sys.exc_info()[0]
            estadoFileId = '4'
            cantidadErrores = cantidadErrores + 1
            
        PtoControl = pd.DataFrame()                
        sql.execute("UPDATE THE_LOTES SET PROCESADO = '%s' WHERE FILE_ID = %s" %(estadoFileId, fileid), PosEngine)
        [fileid,lineamt,ramalmt] = recuperar_prox_lotes(PosEngine, lineaDesde, lineaHasta)
    
    print('Actualizando la tabla de Ptos de control')
    resultado = actualizar_sentidos(PosEngine)    
    print('Actualizacion: %s' %resultado)
    print('----------FIN----------------')

#==============================================================================
#     agrupar signos sirve para analizar cuanto tardan los colectivos en viajar
#     de IDA y de VUELTA
#==============================================================================

    
def agrupaSigno(PosEngine, linea):
    print('Genera la tabla signoag con los sentidos agrupados')
    print('RECIBE CODIGOLINEA !!!!! ')
    cursorRamal= PosEngine.execute("SELECT distinct LINEAMT, RAMALMT FROM lineastrxgeo a, lineascole b where a.lineageo = b.linea2 and a.ramalgeo = ramal and a.baja is null  AND lineamt = '%s' order by a.lineamt, a.ramalmt" % (linea))  
    for ruta in cursorRamal.fetchall():
        print('linea %s ramal %s ' % (ruta.lineamt, ruta.ramalmt))
        ptos= PosEngine.execute("SELECT codigolinea, ramal, file_id, c_control_point, longitud, latitud, fechapto, segundospto - 483000000 segundospto, sentido FROM PTOCONTROL201505 WHERE CODIGOLINEA = '%s' and ramal = '%s' ORDER BY CODIGOLINEA, RAMAL, FILE_ID, C_CONTROL_POINT " % (ruta.lineamt, ruta.ramalmt) )  
        sentidoAg = pd.DataFrame()
        pos = 1    
        row = ptos.fetchone()
        while row != None:
            sentidoant = row.sentido
            fileidant  = row.file_id
            sentidoAg.loc[pos, 'codigolinea'] = row.codigolinea
            sentidoAg.loc[pos, 'ramal'] = row.ramal
            sentidoAg.loc[pos, 'sentido'] = row.sentido
            sentidoAg.loc[pos, 'fechainicio'] = row.fechapto
            sentidoAg.loc[pos, 'segundosinicio'] = row.segundospto    
            sentidoAg.loc[pos, 'file_id'] = row.file_id
            sentidoAg.loc[pos, 'c_control_point'] = row.c_control_point
            cant = 0
            while row != None and sentidoant == row.sentido and fileidant == row.file_id:
                cant = cant + 1
                fechafin =row.fechapto
                segundos = row.segundospto  
                if segundos < 0:
                    print('ERROR grave') 
                row = ptos.fetchone()
            sentidoAg.loc[pos, 'fechafin'] = fechafin 
            sentidoAg.loc[pos, 'segundosfin'] = segundos
            sentidoAg.loc[pos, 'difmin'] = (segundos - sentidoAg.loc[pos, 'segundosinicio']) / 60
            
            sentidoAg.loc[pos, 'cantidad'] = cant
            pos = pos + 1
        
        sentidoAg.to_sql('sentidoag', con=PosEngine, if_exists='append')


        xy = sentidoAg[sentidoAg['difmin']< 500]
        x =xy[xy['sentido']=='I']['difmin'].values
        y =xy[xy['sentido']=='V']['difmin'].values    
        bins = np.linspace(0, 2000, 500)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_xlabel('minutos')
        ax1.set_ylabel('frecuencia')
        ax1.hist(x, bins, alpha=0.5, label='Ida')
        ax1.hist(y, bins, alpha=0.5, label='Vuelta')
        plt.savefig('hittiemposerv-linea%s-ramal%sEVAL.png' %(ruta.lineamt, ruta.ramalmt)) 
         
        xy = sentidoAg[(sentidoAg['difmin']< 500) & (sentidoAg['difmin'] > 20)]
        x =xy[xy['sentido']=='I']['difmin'].values
        y =xy[xy['sentido']=='V']['difmin'].values    
        bins = np.linspace(0, 200, 50)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_title("histograma de tiempo por servicio linea %s ramal %s" % (ruta.lineamt, ruta.ramalmt))
        ax1.set_xlabel('minutos')
        ax1.set_ylabel('frecuencia')
        ax1.hist(x, bins, alpha=0.5, label='Ida')
        ax1.hist(y, bins, alpha=0.5, label='Vuelta')
        plt.savefig('hittiemposerv-linea%s-ramal%s.png' %(ruta.lineamt, ruta.ramalmt)) 

