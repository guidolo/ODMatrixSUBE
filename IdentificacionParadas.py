# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 15:17:54 2014

@author: guidolo
"""
%pylab inline 
%pylab 

#==============================================================================
#BIENVENDOS al mágico mundo de la identificación de paradas de colectivo 
#==============================================================================

from shapely.wkt import loads as wkt_load
import sqlite3
import pandas.io.sql as sql
import pandas as pd
import numpy as np

import Background as bk

#==============================================================================
# ASIGNACION DE PROYECCION A UN PUNTO
#==============================================================================

import os
os.chdir('i:\\tesis')

#viajes debe ser un dataFrame con los siguientes datos 
def proyeccionLineaRamal(linea, ramal, viajes):

    #consqliteLineas  = sqlite3.connect('d:\\DataMining\\Tesis\\DATASET SUBE\\base.db')
    consqliteLineas  = sqlite3.connect('base.db')
    consqliteLineas.text_factory = str

    #RECUPERO LAS SECUENCIAS DE VIAJES 
    
    viajes['latitudpto3'] = 0
    viajes['longitudpto3'] = 0
    viajes['sentido'] = ''
    viajes['error'] = ''
    viajes['distancia'] = 0

    #RECUPERO LOS RECORRIDOS TEORICOS
    lineascole = sql.read_frame('select linea, ramal, sentido, geom  from lineascole where linea = %s and ramal = "%s" order by linea, ramal, sentido' % (linea, ramal), consqliteLineas)

    #tomo los recorridos de ida y de vuelta 
    lineaIDA    = lineascole[(lineascole['LINEA'] == linea) & (lineascole['RAMAL'] == ramal) & (lineascole['SENTIDO'] == 'I')]['GEOM'].values
    lineaVUELTA = lineascole[(lineascole['LINEA'] == linea) & (lineascole['RAMAL'] == ramal) & (lineascole['SENTIDO'] == 'V')]['GEOM'].values

    #paso a shapely
    shplLineIda = wkt_load(lineaIDA[0])
    shplLineVuelta = wkt_load(lineaVUELTA[0])
    #createShpFromWKT([lineascole[0][3]], 'controlsLinea.shp', 'LS')
    
    cantidad = len(viajes)

    for i, row in viajes.iterrows():
        if mod(i, cantidad/100) == 0:
            print('Puntos procesados al: %i porciento' % int(i*100/cantidad))
        
        #proyecciones sobre la IDA
        shplPoint1 = wkt_load("POINT(%s %s)" %  (row['longitudpto1'] , row['latitudpto1']))
        projPoint1 = shplLineIda.project(shplPoint1, normalized=True)
    
        shplPoint2 = wkt_load("POINT(%s %s)" %  (row['longitudpto2'] , row['latitudpto2']))
        projPoint2 = shplLineIda.project(shplPoint2, normalized=True)
    
        #supongo que el uso fue en la IDA
        shpLineaUsada = shplLineIda
        sentido = 'Ida'
        #si son iguales, posiblemente sea un punto alejado, outlier
        if projPoint1 == projPoint2:
            viajes.loc[i,'error'] = 'Mismo punto'
            continue
    
        #la proyeccion del punto 1 debe ser menor a la del punto 2. 
        #en caso contrario es porque el vehiculo está circulando en la otra direccion
        if projPoint1 > projPoint2:
            #proyecciones sobre la vuelta
            shplPoint1 = wkt_load("POINT(%s %s)" %  (row['longitudpto1'] , row['latitudpto1']))
            projPoint1 = shplLineVuelta.project(shplPoint1, normalized=True)
        
            shplPoint2 = wkt_load("POINT(%s %s)" %  (row['longitudpto2'] , row['latitudpto2']))
            projPoint2 = shplLineVuelta.project(shplPoint2, normalized=True)    
            
            #si paso esto supongo que el viaje fue en la VUELTA
            shpLineaUsada = shplLineVuelta    
            sentido = 'Vuelta'
            #si la proyeccion de la VUELTA queda mal tambien, se descarta el punto
            if projPoint1 > projPoint2:
                viajes.loc[i,'error'] = 'Sentido no detectado'
                continue
        
        #calculo la interpolacion entre los dos puntos 
        #puntoenlinea1 = shpLineaUsada.interpolate(projPoint1, normalized=True).wkt
        #puntoenlinea2 = shpLineaUsada.interpolate(projPoint2, normalized=True).wkt
        dist = projPoint1 + ((projPoint2 -projPoint1) * float(row['porc_recorrido']))
        puntoenlinea3 = shpLineaUsada.interpolate(dist, normalized=True)   
        
        
        viajes.loc[i,'latitudpto3'] = puntoenlinea3.y
        viajes.loc[i,'longitudpto3'] = puntoenlinea3.x
        viajes.loc[i,'sentido'] = sentido
        viajes.loc[i,'distancia'] = dist
        viajes.loc[i,'projectpto1'] = projPoint1
        viajes.loc[i,'latsobrelineapto1'] = shpLineaUsada.interpolate(projPoint1, normalized=True).y
        viajes.loc[i,'lonsobrelineapto1'] = shpLineaUsada.interpolate(projPoint1, normalized=True).x
        viajes.loc[i,'projectpto2'] = projPoint2  
        viajes.loc[i,'latsobrelineapto2'] = shpLineaUsada.interpolate(projPoint2, normalized=True).y
        viajes.loc[i,'lonsobrelineapto2'] = shpLineaUsada.interpolate(projPoint2, normalized=True).x
        viajes.loc[i, 'proj1o2'] = projPoint1 if (row['porc_recorrido'] <= 0.5) else projPoint2
        
    return viajes

#==============================================================================
# ASIGNACION DE PARADAS A VIAJES 
#==============================================================================
def asignarParada(linea, ramal, viajes):
    
    consqliteBase  = sqlite3.connect('base.db')
    consqliteBase.text_factory = str
    cantidad = len(viajes)
    #para ambos sentidos
    for sentido in ['Ida', 'Vuelta']:

        #recupero los cortes de las paradas
        paradas = sql.read_frame('select clusterOrd, limiteinf, limitesup, centroide from paradas where linea = %s and ramal = %s and sentido = "%s" ' % (linea, ramal, sentido), consqliteBase)
        paradas = paradas.values.astype(np.float)
        
        for i, row in viajes[viajes['sentido']==sentido].iterrows():
            if mod(i, cantidad/100) == 0:
                 print('Puntos procesados %s al: %i porciento' % (sentido,int(i*100/cantidad)))
            #me quedo con la parada del adecuada del punto
            # parada[:,1] esta ubicado el valor minimo
            #me quedo con el maximo valor menor a la distancia calculada
            nroParada = paradas[paradas[:,1] < row.distancia].argmax(axis=0)[0]
            
            viajes.loc[i, 'parada'] = nroParada
    return viajes 
#==============================================================================
# PRUEBA DE COSAS QUE NO SE EJECUTAN
#==============================================================================

#LOOK FOR ERRORS
viajes[viajes['error'] !='']

nrotarjetaexterno = '1715904373'
dftemp = viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno]
dftemp.to_csv('viajes1715904373.csv', sep=';' )

punto1 ='POINT(%s %s)'% (viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].longitudpto1.values[0], viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].latitudpto1.values[0])
punto2 ='POINT(%s %s)'% (viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].longitudpto2.values[0], viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].latitudpto2.values[0])
puntosl1 ='POINT(%s %s)'% (viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].lonsobrelineapto1.values[0], viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].latsobrelineapto1.values[0])
puntosl2 ='POINT(%s %s)'% (viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].lonsobrelineapto2.values[0], viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].latsobrelineapto2.values[0])
puntosl3 ='POINT(%s %s)'% (viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].longitudpto3.values[0], viajes[viajes['nrotarjetaexterno']== nrotarjetaexterno].latitudpto3.values[0])



#CREATE SHAPE FROM EVERY SINGLE POINT 
wkt = [punto1, punto2, puntosl1, puntosl2, puntosl3]
createShpFromWKT(wkt, 'controls.shp', 'PT')

#CREATE SHAPE FROM DATAFRAME
#en la posicion 13 y 14 esta la lati y long del punto calculado
df = viajes.apply(lambda x:'POINT(%s %s)' % (x[16],x[15]),axis=1)
createShpFromWKT(df, 'puntocalculado.shp', 'PT')

#en la posicion 5 y 4 esta la lati y long del punto1
df = viajes.apply(lambda x:'POINT(%s %s)' % (x[4],x[5]),axis=1)
createShpFromWKT(df, 'punto1.shp', 'PT')



#GAUSSIAN MIXTURE MODEL
dpgmm = mixture.DPGMM(n_components=2, covariance_type='full')
X = viajes[viajes['sentido'] =='Vuelta']['distancia'].values
X = X.reshape((len(X), 1))
data = X
dpgmm.fit(X)
Y_ = dpgmm.predict(X)
Y_.mean()


#PLOT PARA SHAPELY 

fig = nuevoGraf()
line = shplLineString
xrange = [-58.51, -58.50]
yrange = [-34.54, -34.545]
xrange = [0,0]
yrange = [0,0]
addObject(fig, line, xrange, yrange)
addObject(fig,shplPoint1, xrange, yrange)
addObject(fig,shplPoint2, xrange, yrange)
pyplot.show()

#KDE PARA LAS PARADAS DE COLECTIVO 
import numpy as np
from scipy.stats import kde
import matplotlib.pyplot as plt
x1 = np.random.normal(0, 3, 50)
x2 = np.random.normal(4, 1, 50)
x = np.r_[x1, x2]
x=X
density = kde.gaussian_kde(x)
xgrid = np.linspace(x.min(), x.max(), 1000)
plt.hist(x, bins=100, normed=True)
plt.plot(xgrid, density(xgrid), 'r-')
plt.show()


#==============================================================================
#==============================================================================
#==============================================================================
###########################   K-MEANS  ########################################
#==============================================================================
#==============================================================================
#==============================================================================

from sklearn import cluster, datasets
from itertools import cycle
from time import time
from sklearn import metrics


#==============================================================================
# #BENCHMARK SILHOUETTE    
#==============================================================================
def bench_k_means(estimator, name, data):
    sample_size = 1000
    t0 = time()
    estimator.fit(data)
    metric = metrics.silhouette_score(data, estimator.labels_, metric='euclidean', sample_size=sample_size)
    #metric = metrics.silhouette_score(data, estimator.labels_, metric='euclidean')
    print('% 9s   %.2fs    %i   %.3f' % (name, (time() - t0), estimator.inertia_, metric))
    return metric

#==============================================================================
# #scatter de los puntos y centroides 
#==============================================================================
def scatter(Xgraf, k_means):
    plt.figure(1)
    plt.clf()
    labels = k_means.labels_
    cluster_centers = k_means.cluster_centers_
    cluster_centers = [[x[0],1] for x in cluster_centers]
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(Xgraf[my_members, 0], Xgraf[my_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=2)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()


#==============================================================================
# #funcion que evalua k-means iterativomente con los ditintos vaores valores de K
# #devuelve el valor de K optimo
#==============================================================================
def kmeansIterativo(X, K):
    #evaluacion por iteracion de silhouette
    eval = []
    for i in K:
        print(str('Procesando K == %i' %i))
        k_means = cluster.KMeans(n_clusters=i)  
        eval.append([i, bench_k_means(k_means, 'kmeans', X)])
    # plot del resultado
    npeval = np.array(eval)
    plt.plot(npeval[:,0], npeval[:,1], 'r-')
    #plt.plot(npeval[:,0], npeval[:,1], 'r-', npeval2[:,0], npeval2[:,1], 'b-', npeval3[:,0], npeval3[:,1], 'g-')
    plt.show()
    #determinar el mejor nro de clusters
    nclusters = int(npeval[npeval.argmax(axis=0)[1]][0])
    return nclusters

#==============================================================================
# FUNCION QUE DEVUELVE LOS LIMITES DEL CLUSTER 
#==============================================================================
def clusterLimit(X, linea, ramal, sentido, kmeans):
    res = np.vstack(np.array([X, k_means.labels_])).transpose()
    pdres = pd.DataFrame(res, columns=['valores','cluster'])
    grupo = pd.merge( pdres.groupby(['cluster']).min(),  pdres.groupby(['cluster']).max(), left_index=True, right_index=True, how='outer', suffixes=('_min', '_max'))
    grupo = grupo.sort('valores_min')
    
    #renumero los cluster ordenadamente, pego el centroide
    for idx, i in zip(grupo.index, range(len(grupo))):
        grupo.loc[idx, 'linea'] = linea
        grupo.loc[idx, 'ramal'] = ramal
        grupo.loc[idx, 'sentido'] = sentido
        grupo.loc[idx, 'clusterOrd'] = i
        grupo.loc[idx, 'centroide']  =  k_means.cluster_centers_[int(idx)]
        
    #encontrar los limites de los clusters
    limites = grupo[['valores_min','valores_max']].values
    for idx, i in zip(grupo.index, range(len(grupo))):
        if i == 0:    
            grupo.loc[idx, 'limiteInf'] = 0
            grupo.loc[idx, 'limiteSup'] = (limites[i,1]+limites[i+1,0])/2
        else:
            if i == len(limites) - 1:
                grupo.loc[idx, 'limiteInf'] = (limites[i-1,1]+limites[i,0])/2
                grupo.loc[idx, 'limiteSup'] = 1
            else:
                grupo.loc[idx, 'limiteInf'] = (limites[i-1,1]+limites[i,0])/2
                grupo.loc[idx, 'limiteSup'] = (limites[i,1]+limites[i+1,0])/2
    return grupo


def cluserScatter():
    scatter(pdres[['valores','clusterOrd']].values, k_means)
    #graficos
    Xgraf=numpy.array(map(lambda x:numpy.array((x,1)), X))
    scatter(Xgraf, k_means)    
    scatter(res, k_means)
    

#==============================================================================
# TEST DE ASIGNACION DE PROYECCION A UN PUNTO
#==============================================================================
def histograma()
    from matplotlib.pyplot import hist
    
def StopDetection(PosEngine, linea):
    
    
    #conecto con base de datos SQLLite
    #consqliteSecuencia  = sqlite3.connect('d:\\DataMining\\Tesis\\DATASET SUBE\\secuencialinea.db')
#    consqliteSecuencia  = sqlite3.connect('secuencialinea.db')
    
#    consqliteBase  = sqlite3.connect('base.db')
#    consqliteBase.text_factory = str
        
    #recorrer UNA TABLA CON TODAS LAS LINEAS Y LOS RAMALES
        
    for row in lineaRamal.iterow()
    
        ramalTrx = row.Ramal
    
        #parametros
        lineamt = '118'
        ramalmt = '363'
        
        
        #dado un ramal de TRX encuentro la mejor correspondencia dentro de los remales de GEO
        ramalGeo = getMejorRamalGeo(linea, ramalTRX)
        
        [ramal, linea] = bk.ramalGeo(PosEngine, lineamt ,ramalmt)
        
        #recupero 10.000 viajes al azar 
        viajes = sql.read_frame('select codigolinea, linea, ramal, nrotarjetaexterno, longitudpto1, latitudpto1, longitudpto2, latitudpto2, porc_recorrido '
        ' from secuencia '
        ' where porc_recorrido is not null '
        ' and (porc_recorrido < 0.1 or porc_recorrido > 0.9)'
        ' order by fechatrx', consqliteSecuencia)
        
        #viajes sin filtro de cercania
#        viajes = sql.read_frame('select codigolinea, linea, ramal, nrotarjetaexterno, longitudpto1, latitudpto1, longitudpto2, latitudpto2, porc_recorrido '
#        ' from secuencia '
#        ' where porc_recorrido is not null '
#        ' order by fechatrx', consqliteSecuencia)    
        
        #proyecto las subidas sobre su traycto, completo dataframe con posicion estandarizada y sentido (ida o vuelta)
        viajes = proyeccionLineaRamal(linea, ramalGeo, viajes)
        
        #calculo automático de las paradas de colectivo
        for sentido in ['Ida', 'Vuelta']:
            X = viajes[ (viajes['sentido'] == sentido) & (viajes['distancia'] > 0.001) & (viajes['distancia'] < 0.99) ]['distancia'].values
            X = viajes[ (viajes['sentido'] == sentido) & (viajes['distancia'] > 0.001) & (viajes['distancia'] < 0.99) ]['proj1o2'].values
            X = viajes[viajes['sentido'] == sentido ]['projectpto1'].values    
            X = viajes['projectpto1'].values    
            X = viajes[viajes['sentido'] == sentido ]['projectpto2'].values    
            X = viajes[viajes['sentido'] == sentido]['distancia'].values
    
            # HISTOGRAMAS de ingreso al colectivo
            hist(X, 500, (0, 1), color=['r'])
    
            #determino el cluster ganador
            k=range(2,50)
            nclusters = kmeansIterativo(X, k)
          
            #uso del cluster ganador 
            k_means = cluster.KMeans(n_clusters=nclusters )  
            X = X.reshape((len(X), 1))
            k_means.fit(X) 
            
            #agrego informacion del cluster
            grupo = clusterLimit(X, linea, ramalTrx, sentido, k_means)
    
            #guardo las paradas en tabla 
            sql.write_frame(grupo, "Paradas", consqliteBase, if_exists='append')
    
            his = hist(X, 500, (0, 1), color=['r'])
            for i, row in grupo.iterrows():
                  plt.axvline(row.limiteInf, color='b', linestyle='dashed', linewidth=1)
                  plt.axvline(row.centroide, color='r', linestyle=':', linewidth=1)
              
              
#==============================================================================
# ASIGNACION DE LAS PARADAS A LOS PUNTOS DE CONTROL
#==============================================================================

#conecto con base de datos SQLLite
#consqliteSecuencia  = sqlite3.connect('d:\\DataMining\\Tesis\\DATASET SUBE\\secuencialinea.db')
consqliteSecuencia  = sqlite3.connect('secuencialinea.db')

#HACER UNA TABLA CON TODAS LAS LINEAS Y LOS RAMALES
    
for row in lineaRamal.iterow()
    
    linea = '118'
    ramal = '363'    
    
     #recupero 10.000 viajes al azar 
    viajes = sql.read_frame('select codigolinea, linea, ramal, nrotarjetaexterno, longitudpto1, latitudpto1, longitudpto2, latitudpto2, porc_recorrido '
    ' from secuencia '
    ' where porc_recorrido is not null '
    ' order by fechatrx', consqliteSecuencia)

    grupo = sql.read_frame('select * from paradas where linea = %s and ramal = %s and sentido = "%s" ' % (linea, ramal, sentido), consqliteBase)

    #proyecto las subidas sobre su traycto, completo dataframe con posicion estandarizada y sentido (ida o vuelta)
    viajes = proyeccionLineaRamal(linea, ramalGeo, viajes)

    #le asigno a los viajes sus paradas
    viajes = asignarParada(linea, ramal, viajes)

    for i, row in grupo.iterrows():        
        #en la posicion 13 y 14 esta la lati y long del punto calculado              
        puntocalc = viajes[(viajes['parada']== i)&(viajes['sentido']== sentido)].apply(lambda x:'POINT(%s %s)' % (x[10],x[9]),axis=1)
        createShpFromWKT(puntocalc, 'puntos118%s_p%s.shp' % (sentido, str(i)), 'PT')




