# -*- coding: utf-8 -*-
"""
Created on Fri Dec 26 12:36:37 2014

@author: guidolo
"""

import sys
import pandas as pd
import numpy as np
import sqlite3
import pandas.io.sql as sql
import math
#import statistics as st
from matplotlib.pylab import hist, show
from shapely.wkt import loads as wkt_load
import os
os.chdir('i:\\tesis\\')

#sys.path.insert(0, 'i:\\tesis\\Repositorio Python\\Conections\\')
#import connects
import Background as bk

sys.path.insert(0, 'i:\\tesis\\Repositorio Python\\GEO\\')
import GEOUtiles as geou
 

def largoRuta(PosEngine):
    cursorRamal= PosEngine.execute("SELECT LINEa, RAMALgeo ramal, sentido, geom FROM lineastrxgeo a, lineascole b where a.lineageo = b.linea2 and a.ramalgeo = ramal and a.baja is null  order by a.lineamt, a.ramalmt" )  
    pos = 1
    largos = pd.DataFrame()    
    for row in cursorRamal.fetchall():
        largos.loc[pos, 'codigolinea'] = row.linea
        largos.loc[pos, 'ramal'] = row.ramal
        largos.loc[pos, 'sentido'] = row.sentido
        shplLineIda = wkt_load(row.geom) 
        p2=0
        largo = 0
        for i in shplLineIda.coords:
            p1 = i
            if p2 != 0: 
                largo = largo + geou.distancia(p1[0], p1[1], p2[0], p2[1])
            p2 = p1
        print (largo)   
        largos.loc[pos, 'largo'] = largo
        pos = pos + 1    
    largos.to_sql('largos', con=PosEngine)
    
#==============================================================================
# funcion que devuelve N puntos de control para cada ramal de una linea en particular
# genera un shape con un lineString del recorrido de la linea
#devuelve CODIGOLINEA, RAMALTRX, LONGITUD PTO CONTROL, LATITUL PTO CONTROL
#==============================================================================

    
def shpPuntosControlLinea(line, PosEngine):
    connect = PosEngine.connect()
    #cargo los ramales distintos de los puntos de control 
    cursorRamal = PosEngine.execute("SELECT linea2 LINEA, CODIGOLINEA, RAMAL FROM THE_RAMALES WHERE LINEA2 = '%s'" % line)  
    listShapPoint = []
    if cursorRamal.rowcount > 0 :
        for ramal in cursorRamal.fetchall():      
            
            sqlcode = ("SELECT CODIGOLINEA, RAMAL, LONGITUD, LATITUD "                  
            " FROM PTOCONTROL201505 "
            " WHERE CODIGOLINEA = '%s' "                        
            " AND RAMAL = '%s' "  % (ramal[1],ramal[2]))
            
            tempListPoint = sql.read_sql(sqlcode, PosEngine)
            
            #creo los shape para inspeccion visual
            wkt = [ "POINT(%s %s)" %  (punto[2] , punto[3]) for punto in tempListPoint.values]
            geou.createShpFromWKT(wkt, 'puntosLinea%sRamal%s.shp' %(ramal[0], ramal[2]), 'PT')
                
def puntosControlLinea(line, PosEngine):
    connect = PosEngine.connect()
    cursorRamal = PosEngine.execute("SELECT DISTINCT CODIGOLINEA FROM THE_RAMALES WHERE LINEA2 = '%s'" % line)
    
    listShapPoint = []
    if cursorRamal.rowcount > 0 :
        for ramal in cursorRamal.fetchall():
            sqlcode = ("SELECT CODIGOLINEA, RAMAL, LONGITUD, LATITUD, 0 wkt, FILE_ID, C_CONTROL_POINT "                  
            " FROM PTOCONTROL201505 "
            " WHERE CODIGOLINEA = '%s' "  % ramal[0])

            tempListPoint = sql.read_sql(sqlcode, PosEngine)    
            tempListPoint["wkt"] = tempListPoint.apply(lambda x: wkt_load('POINT(%s %s)' % (x[2],x[3])), axis=1)
            listShapPoint = tempListPoint.values
    return listShapPoint

def puntosControlLineaRamal(lineamt, ramalmt, PosEngine):   
    
    sqlcode = ("SELECT CODIGOLINEA, RAMAL, LONGITUD, LATITUD, 0 wkt, FILE_ID, C_CONTROL_POINT "                  
                " FROM PTOCONTROL201505 "
                " WHERE CODIGOLINEA = '%s' "
                "   AND RAMAL = '%s' "
                " ORDER BY FILE_ID "% (lineamt, ramalmt) )
                
    tempListPoint = sql.read_sql(sqlcode, PosEngine)
    if len(tempListPoint) > 0:
        tempListPoint["wkt"] = tempListPoint.apply(lambda x: wkt_load('POINT(%s %s)' % (x[2],x[3])), axis=1)
        listShapPoint = tempListPoint.values
                
        return listShapPoint
    else:
        return []

#==============================================================================
# test
#==============================================================================
def distPtoLinea(PosEngine, lineaDesde, lineaHasta, shp, db, tst):
    connect = PosEngine.connect()
    if lineaHasta == '':
        lineaHasta = '999'
        
    #tomo de lineas cole
    lineascole = sql.read_sql("select trim(to_char(CASE WHEN substring(LINEA FROM '[0-9]*') != '' THEN TO_NUMBER(substring(LINEA FROM '[0-9]*'),'999') END, '999')) linea, ramal, sentido, geom, LINEA lineaaux FROM lineascole WHERE linea >= '%s' and linea < '%s' ORDER BY linea, ramal, sentido" %(lineaDesde,lineaHasta), PosEngine)
    lineascole = lineascole.values

    i = 0
    cant = 0

    #para cada reccorrido geográfico
    while i < len(lineascole):
        line    = lineascole[i][0] 
        lineant = line
        print('Ejecutando linea: %s ...' % line)
        listShapLineString = []
        distancias = []

        listShapPoint = puntosControlLinea(line, PosEngine)
        if shp == 1:
            #genero un shape con todos los puntos de la linea
            shpPuntosControlLinea(line, PosEngine)
            
        print('     %d Puntos encontrados' % len(listShapPoint))    

        #por cada ramal geográfico
        while line == lineant and i < len(lineascole) and len(listShapPoint) > 0:
            test = []
            print('         Ramal: %s Sentido: %s' % (lineascole[i][1],lineascole[i][2]) )

            if shp == 1:
                #creamos un shape de a linea para la inspeccion visual        
                geou.createShpFromWKT([lineascole[i][3]], 'linea%sRamal%sSentido%s.shp' % (lineascole[i][0], lineascole[i][1], lineascole[i][2]), 'LS')
			
            #shapely del raml de la linea a calcular las distancias
            shplLineString = wkt_load(lineascole[i][3])
			
            j=0
            #para cada punto de control encontrado
            for punto in listShapPoint:  
                j=j+1
                #en p calculo la 
                p = shplLineString.interpolate(shplLineString.project(punto[4]))
                #en distancia voy agregando: codigolinea, ramaltrx,  lineageo, ramalgeo, sentido, distnacia del punto de control al punto proyectado
                distancias.append([j,punto[0], punto[1],lineascole[i][0],lineascole[i][1],lineascole[i][2], geou.distancia(punto[4].x, punto[4].y, p.x, p.y), punto[5], punto[6] ])
                
                if tst == 1:                
                    test.append([j,punto[0], punto[1],lineascole[i][0],lineascole[i][1],lineascole[i][2], geou.distancia(punto[4].x, punto[4].y, p.x, p.y), punto[5], punto[6], p.x, p.y, punto[4].x, punto[4].y])
            
            if tst == 1:
                pdtest = pd.DataFrame(test)
                pdtest.columns = ['punto','lineamt', 'ramalmt', 'lineageo', 'ramalgeo', 'sentidogeo', 'distancia', 'file_id', 'c_control_point','long_linea', 'lat_linea', 'long_pto', 'lat_pto']    
                pdtest.to_csv('linea%sRamal%sSentido%s.csv' % (lineascole[i][0], lineascole[i][1], lineascole[i][2]), sep=';') 
            
            lineant = line    
            i = i + 1    
            if i < len(lineascole):
                line = lineascole[i][0]
		
        if len(listShapPoint) > 0:
            if db == 1:
                PtoControl = pd.DataFrame(distancias)
                PtoControl.columns = ['punto','lineamt', 'ramalmt', 'lineageo', 'ramalgeo', 'sentidogeo', 'distancia', 'file_id', 'c_control_point']    
                PtoControl.to_sql('distancias', con=PosEngine, if_exists='append')
           
        else:
            while line == lineant and i < len(lineascole):
                line    = lineascole[i][0] 
                i = i + 1


def calcRMSE(PosEngine, lineaDesde, lineaHasta):
    
#   cargo todos las rutas
    baseLineasRamales = bk.cargar_lineas(PosEngine).values
 
#    recorro las lineas que estan vacias 
    sql_code = ("    select codigolinea lineamt, ramal ramalmt "
                " from the_ramales a left outer join  lineastrxgeo b "
                " on  a.codigolinea = cast(b.lineamt as integer) "
                " and a.ramal = b.ramalmt "
                " where b.ramalmt is null "
                "  and cantidad_trx > 1000 "
                "  and linea2 is not null "
                "  and codigolinea > %s "
                "  and codigolinea < %s "
                " order by codigolinea " % (lineaDesde, lineaHasta) )

    lineas = PosEngine.execute(sql_code)  
    
#    for linea in lineas.fetchall():
    for linea in range(1):
#        lineamt = linea.lineamt 
#        ramalmt = linea.ramalmt 
        lineamt = '100'
        ramalmt = '202'

        print('Ejecutando lineamt / ramalmt: %s / %s ...' % (lineamt, ramalmt))

#       cargo los puntos de control        
        listShapPointTotales = puntosControlLineaRamal(lineamt, ramalmt, PosEngine)
        
        if len(listShapPointTotales) > 0:
    #        me quedo con los file_id unicos
            fileids = np.unique(listShapPointTotales[:,5])
            fileids = fileids.reshape(len(fileids),1)
            
    #        para cada file_id
            for fileid in fileids:
                i = 0        
                minDistCuad = 0
                RMSE = pd.DataFrame()
                listShapPoint = listShapPointTotales[listShapPointTotales[:,5] == fileid[0]]
                
                #para cada reccorrido geográfico
                while i < len(baseLineasRamales) and len(listShapPoint) > 0:
                    
        #           cargo la ruta            
                    shplLineString = wkt_load(baseLineasRamales[i][3])
                    distanciaCuadrado = 0
                    
                    #para cada punto de control encontrado
                    for punto in listShapPoint:
                        
        #               sumo todas las distancias al cuadrado en metros
                        p = shplLineString.interpolate(shplLineString.project(punto[4]))
                        
                        dist = geou.distancia(punto[4].x, punto[4].y, p.x, p.y)
    #                   solo tomo los puntos que están a menos de 50 km para evitar errores graves en el GPS
                        if dist < 50:                  
                        #en distancia voy agregando: codigolinea, ramaltrx,  lineageo, ramalgeo, sentido, distnacia del punto de control al punto proyectado
                            distanciaCuadrado = distanciaCuadrado + dist ** 2 
        
        #           pruebo que el RMSE encontrado sea el minimo para la linea                
                    if minDistCuad > distanciaCuadrado or minDistCuad == 0:
                        minDistCuad = distanciaCuadrado 
                        minLinea = baseLineasRamales[i][0]
                        minRamal = baseLineasRamales[i][1]
                        minSentido = baseLineasRamales[i][2]
                    i = i + 1
                    
                if len(listShapPoint) > 0:
                    print ('lote:%s - RMSE:%s - linea:%s - ramal:%s - sentido:%s' % (fileid[0], math.sqrt(minDistCuad / len(listShapPoint)), minLinea, minRamal, minSentido ))
                    RMSE.loc[0, 'lineamt'] = lineamt
                    RMSE.loc[0, 'ramalmt'] = ramalmt
                    RMSE.loc[0, 'linea'] = minLinea
                    RMSE.loc[0, 'ramal'] = minRamal
                    RMSE.loc[0, 'sentido'] = minSentido
                    RMSE.loc[0, 'file_id'] = fileid[0]
                    RMSE.loc[0, 'rmse'] = math.sqrt(minDistCuad / len(listShapPoint))
                    RMSE.to_sql('rmse', con=PosEngine, if_exists='append')
                                            
                
                
                
    print ('FIN')
        

        


#==============================================================================
# REPRESENTACION DE LOS DATOS DE DISTANCIA
#==============================================================================
def plot():
	consqlite  = sqlite3.connect('d:\\DataMining\\Tesis\\DATASET SUBE\\base.db')
	consqlite.text_factory = str
	df = sql.read_frame('SELECT  MINDISTANCIA from MINDISTANCIA WHERE LINEAMT = 114 AND RAMALMT = 361  AND RAMALGEO = "B" ', consqlite)    

	df = filtroDesvioStd(df, 'MINDISTANCIA', 6)
	hist([val[0] for val in df.values], 100, (0,200))

	#BOXPLOT
	consqliteBase  = sqlite3.connect('base.db')
	consqliteBase.text_factory = str
	df = sql.read_frame('SELECT A.*, B.AREAGEOGRAFICA FROM LINEASTRXGEO  A, (SELECT DISTINCT LINEA, RAMAL, AREAGEOGRAFICA FROM  LINEARAMALTRX) B WHERE A.LINEAMT = B.LINEA AND A.RAMALMT = B.RAMAL', consqliteBase  )
	df = sql.read_frame('SELECT A.* FROM LINEASTRXGEO A ', consqliteBase  )

	figure()
	boxplot(df['RMSE'],0,'gD', 0)
	boxplot(df['RMSE'],0,'', 0)

	boxplot(df[df['AREAGEOGRAFICA']=='1']['RMSE'],0,)

	#%pylab 

	boxplot(df[df['AREAGEOGRAFICA']=='12']['RMSE'].values,0)
	boxplot(df[df['AREAGEOGRAFICA']=='13']['RMSE'].values,0)


	boxplot([df[df['AREAGEOGRAFICA']=='1']['RMSE'], df[df['AREAGEOGRAFICA']=='12']['RMSE'], df[df['AREAGEOGRAFICA']=='13']['RMSE']],0,'gx',0)
	boxplot([df[df['AREAGEOGRAFICA']=='1']['RMSE'], df[df['AREAGEOGRAFICA']=='12']['RMSE'], df[df['AREAGEOGRAFICA']=='13']['RMSE']],0,'')

	hist(df['RMSE'], 20)

#==============================================================================
# funcion que filtra los puntos de control iterativamente por X sigmas según la
    #distancia con la ruta teórica
#==============================================================================
def filtroDesvioStd(df, columnname, sigma):
    cantAnt = 0
    i = 1
    while cantAnt != len(df):
        print str(i)
        i = i +1
        cantAnt = len(df)
        df = df[np.abs(df[columnname] - df[columnname].mean()) <= (sigma*df[columnname].std())]          
    return df
    
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
