# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 09:34:54 2014

@author: guidolo
"""
import pandas as pd
import numpy as np
import sqlite3
import pandas.io.sql as sql
import os
os.chdir('i:\\tesis')

import sys
sys.path.insert(0, 'i:\\tesis\\Repositorio Python\\GEO\\')
import GEOUtiles as geo




#==============================================================================
# truncar tablas temporales
#==============================================================================

def truncate(PosEngine):
    print('Truncando tabla sentido')
    PosEngine.execute("TRUNCATE TABLE sentido")
    print('Sentido truncada')

#==============================================================================
#  funcion de devuelve la linea GEO de una linea ramal TRx
#==============================================================================
def ramalGeo(PosEngine, lineamt, ramalmt):
    import sys  
    
#    consqliteBase  = sqlite3.connect('base.db')    
#    consqliteBase.text_factory = str
    df = sql.read_sql("select lineageo, ramalgeo from lineastrxgeo where lineamt = '%s' and ramalmt = '%s' " % (lineamt, ramalmt), PosEngine)
    try:
        resultado = [str(df.ramalgeo[0]), str(df.lineageo[0])]
    except:
        resultado = ['0','0']
        
#    consqliteBase.close()
    return resultado

def connect():
    #conecto con base de datos SQLLite
    consqliteSecuencia= sqlite3.connect('secuencialinea.db')
    consqlite  = sqlite3.connect('secuencialinea.db')
    consqliteLineatrx  = sqlite3.connect('lineatrx.db')


#==============================================================================
# CARGA LAS LINEAS
#==============================================================================
def cargar_lineas(connBase):
    return sql.read_sql("SELECT linea, ramal, sentido, geom  FROM LineasCole where baja is null", connBase)



#==============================================================================
# conversion de shape lineas a dataframe
#==============================================================================
def extraeLineaShp(inShapefile, engine):
    
    if os.path.isfile(inShapefile) == False:
        print('No existe el archivo :-P')
        return 0
    
#    inShapefile = 'Recorridos.shp'
    col = ['FIRST_IDNO','IDRUTA','LINEA','LINEARAMAL','RAMAL','ROUTE_ID','ROUTE_NAME','SENTIDO']
    
    features = geo.extraeFatures(inShapefile, col)
    
    for i in range(len(features)):
        features[i][3] = features[i][3].decode('latin1').encode('utf8')
        features[i][4] = features[i][4].decode('latin1').encode('utf8')
        features[i][7] = features[i][7].decode('latin1').encode('utf8')
        
#    npfeatures = np.array(features)
    lineasCole = pd.DataFrame(features, columns=col)
    
    lineawkt = geo.extraeLineas(inShapefile)
    lineasCole['GEOM'] = lineawkt
    
    #guardo las lineas de colectivo en base 
#    sql.write_frame(lineasCole, "LineasCole", connect )
    lineasCole.to_sql("LineasCole", con = engine, if_exists='append')

#lineasCole[lineasCole['IDRUTA'] == '2349']['GEOM']

#==============================================================================
# shapely -- pongo los puntos de control sobre sus lineas de colectivo
#==============================================================================
def puntoEnLinea():
    lineStringAux = lineasCole[lineasCole['IDRUTA'] == '2349']['GEOM']
    lineString = lineStringAux.values.tolist()[0]
    line = wkt_load(lineString)
    list(line.coords)
    
    inShapeFile = 'puntoslinea.shp'
    listPuntos = extraePuntosPuntos(inShapeFile)
    
    listPuntoEnLinea = []
    for punto in listPuntos:
        splypunto = wkt_load(punto)
        puntoenlinea = line.interpolate(line.project(splypunto))
        listPuntoEnLinea.append(puntoenlinea.wkt)
    
    createShpFromWKT(listPuntoEnLinea,'puntoEnLinea.shp')

#==============================================================================
# shape de puntos de control de una linea
#==============================================================================
def puntoLinea():
    conn = redShiftConnect()
    cursor = redShiftCursor(conn,'CliSide')
    resultado = select(cursor, 'PUNTOSCONTROL')
    
    npresultado = np.array(resultado)
    #wkt = [npresultado[:,3], npresultado[:,4]]
    
    df = pandas.DataFrame(npresultado)
    df['wkt'] = df.apply(lambda x:'POINT(%s %s)' % (x[3],x[4]),axis=1)
    df['wkt'] = df['wkt'].astype('str')
    createShpFromWKT(df['wkt'].astype('str'),'puntoslinea.shp')


#==============================================================================
# AUXILIAR BAJO PUNTOS EN SECUENCIA DE UNA LINEA PARA TENERLOS A MANO
#==============================================================================
def aux():
    import pandas.io.sql as sql
    #me bajo la secuencia de una linea
    conn = redShiftConnect()
    cursor = redShiftCursor(conn,'CliSide')
    
    resultado = select(cursor, 'PUNTOSCONTROL WHERE LINEA = 118  ORDER BY IDARCHIVOINTERCAMBIO, FECHATRX')
    resultado = select(cursor, 'LINEASRAMALTRX')
    
    sql.write_frame(resultado, "SECUENCIA", consqliteSecuencia )
    sql.write_frame(resultado, "linearamaltrx", consqliteLineatrx  )
    
    resultado = select(cursor, 'RAWPTOCONTROL2')
    
    sql.write_frame(resultado, "RAWPTOCONTROL", consqliteSecuencia )



#==============================================================================
# paso de una base de SQLITE a otra
#==============================================================================
def aux2():
    consqliteLineatrx  = sqlite3.connect('lineatrx.db')
    consqliteBase  = sqlite3.connect('base.db')
    lineatrx = sql.read_frame('SELECT * FROM linearamaltrx ', consqliteBase  )
    sql.write_frame(lineatrx,'LINEARAMALTRX', con=consqliteBase, if_exists='append')


#==============================================================================
# store procedure para cargar puntos de control de manera automática para cada linea
#==============================================================================
def cargaPtoControl():
    conn = redShiftConnect()
    cursor = redShiftCursor(conn,'CliSide')
    resultado = select(cursor, 'LINEASRAMALTRX')
    
    for i, row in resultado.iterrows():
        print(row['codigolinea'])
    
        sql = ('		INSERT INTO PUNTOSCONTROL (LINEA, RAMAL, NROTARJETAEXTERNO, TIPOMAPPING, CODIGOTRXTARJETA, FECHATRX, FECHAINGRESO, IDARCHIVOINTERCAMBIO, REF_EXT, CONTROL_POINT_1, LONGITUDPTO1, LATITUDPTO1, FECHAPTO1)'
        '               SELECT MT.CODIGOLINEA LINEA, MT.CODIGOTRAYECTO RAMAL, MT.NROTARJETAEXTERNO, MT.TIPOMAPPING, MT.CODIGOTRXTARJETA, MT.FECHATRX, MT.FECHAINGRESO, MT.IDARCHIVOINTERCAMBIO, L.REF_EXT, P.C_CONTROL_POINT CONTROL_POINT_1, P.LONGITUD LONGITUDPTO1, P.LATITUD LATITUDPTO1, P.DATE_TIME FECHAPTO1'
        '               FROM MOVIMIENTOTARJETA2 MT, LOTE L, POSITIONING P'
        '               WHERE MT.IDARCHIVOINTERCAMBIO = L.ID_LOTE AND CODIGOTIPOTRX = 19 AND L.REF_EXT = P.FILE_ID AND MT.ID_POSICIONAMIENTO = P.C_CONTROL_POINT '
        '               AND MT.CODIGOLINEA = %s AND MT.CODIGOTRAYECTO = %s '
        '               LIMIT 10000;  ' % (row['codigolinea'], row['ramal']))
        
        print(sql)    
        
        cursor.execute(sql)


#==============================================================================
# histograma de distancias a los recorridos
#==============================================================================
def hisPtosLineas():
    import matplotlib.pyplot as plt
   
    sentido = sql.read_frame('SELECT * FROM sentido', consqliteSecuencia  )
    
    sentido.dtypes
    
    np.unique(sentido["linea"])
    
    xy_sentido = sentido[(sentido["linea"] == 160) & (sentido["Sentido"] == 'V') & (sentido["DistAIda"] < 1000)][["MilePostIda","DistAIda"]].values
    
    plt.hist(xy_sentido[:,1], 100)
    
    plt.hist(xy_sentido[:,0], 100)
    
    plt.hist(log(xy_sentido[:,1]+1), 100)
    
    plt.hist2d(xy_sentido[:,0], xy_sentido[:,1])
    
    plt.hist2d(xy_sentido[:,0], log(xy_sentido[:,1]+1), 20)
    
    plt.scatter(xy_sentido[:,0], xy_sentido[:,1])
    
    plt.scatter(xy_sentido[:,0], log(xy_sentido[:,1]+1))





