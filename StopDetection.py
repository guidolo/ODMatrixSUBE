# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 16:52:02 2015

@author: gsidoni
"""
import pandas.io.sql as sql
from shapely.wkt import loads as wkt_load
from numpy import mod as mod
import pandas as pd
from sklearn import cluster, datasets
from sklearn import metrics
from time import time
import numpy as np
import matplotlib.pyplot as plt


#==============================================================================
# esta funcion agrega sobre el viaje el punto interpolado sobre la ruta
#==============================================================================
def cargarLotesAMuestra(PosEngine, lineamt,ramalmt, sentido, cantidadLotes):
    
    cursorLotes = PosEngine.execute("select distinct file_id "
                                    " from the_viajesmayo a"
                                    " where a.codigolinea = %s "
                                    "  and a.ramal = '%s' "
                                    "  limit %s " % (lineamt,ramalmt,cantidadLotes ))  


    if cursorLotes.rowcount > 0 :
        print('delete ptocontrol muesta')
        PosEngine.execute("delete from ptocontrol201505_muestra where codigolinea = '%s' and ramal = '%s'" %(lineamt, ramalmt))

        print('delete the viajes muesta')
        PosEngine.execute("delete from the_viajes_muestra where codigolinea = '%s' and ramal = '%s'" %(lineamt, ramalmt))
    
        for lote in cursorLotes.fetchall():         
            file_id = lote[0]
            print('file_id: %s' %file_id)
            
            print('update pto control')
            sql_code = (" UPDATE THE_VIAJESMAYO A "
                        " SET LATITUDPTO3 = B.LATITUDPTO3, "
                        " LONGITUDPTO3 = B.LONGITUDPTO3, "
                        " DISTANCIA = B.DISTANCIA "
                        " FROM PROYECCIONRUTA B "
                        " WHERE A.NROTARJETAEXTERNO = B.NROTARJETAEXTERNO "
                        "  AND A.CODIGOTRXTARJETA = B.CODIGOTRXTARJETA "								 
                        "  AND A.FILE_ID = %s" %(file_id) )
            PosEngine.execute(sql_code)

            print('insert pto control')
            PosEngine.execute(" insert into ptocontrol201505_muestra (codigolinea, ramal, file_id, c_control_point, longitud, latitud,  segundospto, sentido) "
                                " select %s, '%s', file_id, c_control_point, longitud, latitud, segundospto, sentido "
                                " from ptocontrol201505b "
                                " where file_id = %s" %(lineamt, ramalmt, file_id ))

            print('insert viajes')
            PosEngine.execute(" insert into the_viajes_muestra (codigolinea, ramal, nrotarjetaexterno, codigotrxtarjeta, fechatrx, fechaingreso, idarchivointercambio, file_id, c_control_point1, c_control_point2, porc_recorrido, latitudpto3, longitudpto3, distancia) "
                              "  select codigolinea, ramal, nrotarjetaexterno, codigotrxtarjeta, fechatrx, fechaingreso, idarchivointercambio, file_id, c_control_point1, c_control_point2, porc_recorrido, latitudpto3, longitudpto3, distancia"
                              "  from the_viajesmayo "
                              "  where file_id = %s " %(file_id ))
            

                   
            

def proyLinea(PosEngine, lineaDesde, lineaHasta):

    print('Este procedimeinto graba en proyeccionruta y luego en THE_VIAJESMAYO')
   
    cursorRamal = PosEngine.execute("SELECT a.LINEAMT, A.RAMALMT,A.LINEAGEO,A.RAMALGEO, sentido, geom "
                                    " FROM lineastrxgeo a, lineascole b "
                                    " where a.lineageo = b.linea2 and a.ramalgeo = ramal "
                                    "   and a.baja is null  AND lineageo >= '%s' "
                                    "   and lineageo < '%s' "
                                    "order by a.lineageo, a.ramalgeo" % (lineaDesde, lineaHasta))  
    
    listShapPoint = []
    if cursorRamal.rowcount > 0 :
        # por cada ramal de la linea
        for ramal in cursorRamal.fetchall():      
            lineamt = ramal[0]
            ramalmt = ramal[1]
            lineageo  = ramal[2]
            sentido = ramal[4]
            print('procesando codigolinea %s lineaGEO %s ramal %s sentido %s' % (ramal[0], lineageo, ramal[1], ramal[4]) ) 
        
            #recupero para cada viaje lo longitud y la latitud de los puntos de control anterior y siguiente, 
            #ademas se recupera el porcentaje del recorrido en que se encuentra el viaje desde el punto de control anterior al siguiente
            #finalmente se recupera el sentido primer punto de control
            sqlcode = ("SELECT B.NROTARJETAEXTERNO, B.CODIGOTRXTARJETA, A.LONGITUD longitudpto1, A.LATITUD latitudpto1, "
                       " C.LONGITUD longitudpto2, C.LATITUD latitudpto2, B.PORC_RECORRIDO, A.SENTIDO "
                        " FROM  PTOCONTROL201505B A, THE_VIAJESMAYO B, PTOCONTROL201505B C "
                        " WHERE A.FILE_ID = B.FILE_ID "
                        "  AND A.C_CONTROL_POINT = B.C_CONTROL_POINT1  "
                        "  AND B.FILE_ID = C.FILE_ID "
                        "  AND B.C_CONTROL_POINT2 = C.C_CONTROL_POINT "                        
                        "  AND B.CODIGOLINEA = %s "
                        "  AND B.RAMAL = '%s' "
                        "  AND a.SENTIDO = '%s' "
                        "  AND B.DISTANCIA IS NULL  "
                        " ORDER BY B.FECHATRX " % (ramal[0],ramal[1], ramal[4]))

            viajes = sql.read_sql(sqlcode  , PosEngine)            
            
            #paso a shapely
            shplLine = wkt_load(ramal[5])
            
            viajestemp = pd.DataFrame()
            viajestemp['nrotarjetaexterno'] = ''
            viajestemp['codigotrxtarjeta']= ''
            viajestemp['latitudpto3'] = 0
            viajestemp['longitudpto3'] = 0
            viajestemp['distancia'] = 0
            
            shplLineIda = wkt_load(ramal[5]) 
            
            cantidad = len(viajes)

            for i, row in viajes.iterrows():                
                if mod(i, cantidad/100) == 0:
                    print('Puntos procesados al: %i porciento' % int(i*100/cantidad))
                    
                shplPoint1 = wkt_load("POINT(%s %s)" %  (row['longitudpto1'] , row['latitudpto1']))
                projPoint1 = shplLine.project(shplPoint1, normalized=True)
            
                shplPoint2 = wkt_load("POINT(%s %s)" %  (row['longitudpto2'] , row['latitudpto2']))
                projPoint2 = shplLine.project(shplPoint2, normalized=True)

                dist = projPoint1 + ((projPoint2 -projPoint1) * float(row['porc_recorrido']))
                puntoenlinea3 = shplLine.interpolate(dist, normalized=True)       
                
                viajestemp.loc[i,'nrotarjetaexterno'] = row['nrotarjetaexterno']
                viajestemp.loc[i,'codigotrxtarjeta'] = row['codigotrxtarjeta']
                viajestemp.loc[i,'latitudpto3'] = puntoenlinea3.y
                viajestemp.loc[i,'longitudpto3'] = puntoenlinea3.x
                viajestemp.loc[i,'distancia'] = dist
            
            viajestemp.to_sql('proyeccionruta', con=PosEngine, if_exists='append')

    print ('Actualizando tabla THE_VIAJESMAYO...')

#    sql_code = (" UPDATE THE_VIAJESMAYO A "
#                " SET LATITUDPTO3 = B.LATITUDPTO3, "
#                " LONGITUDPTO3 = B.LONGITUDPTO3, "
#                " DISTANCIA = B.DISTANCIA "
#                " FROM PROYECCIONRUTA B "
#                " WHERE A.NROTARJETAEXTERNO = B.NROTARJETAEXTERNO "
#                "  AND A.CODIGOTRXTARJETA = B.CODIGOTRXTARJETA "
#            )

    PosEngine.execute(sql_code)

def actualizarViajes(Connect, PosEngine):
    cur = Connect.cursor('cursorOne')
    cur.itersize = 10000
    print("Iniciando Update masivo...")
    cur.execute("SELECT nrotarjetaexterno"
                " FROM proyeccionruta order by nrotarjetaexterno")
#                                    " order by nrotarjetaexterno" )  
    print("Fetch complete...")
    cont = 0
    t0 = time()    
    tarjetafin = '0'
    for tarjeta in cur:
        cont = cont + 1
#        print tarjeta[0]
        
        if cont > 9999:
            
            tarjetainicio = tarjetafin
            tarjetafin = tarjeta[0]
            sql_code = (
                        "UPDATE THE_VIAJESMAYO A "
                        " SET LATITUDPTO3 = B.LATITUDPTO3, "
                        " LONGITUDPTO3 = B.LONGITUDPTO3, "
                        " DISTANCIA = B.DISTANCIA  "
                        " FROM (select * FROM PROYECCIONRUTA WHERE NROTARJETAEXTERNO >= '%s' and NROTARJETAEXTERNO < '%s' ) B "
                        " WHERE A.NROTARJETAEXTERNO = B.NROTARJETAEXTERNO "
                        "  AND A.CODIGOTRXTARJETA = B.CODIGOTRXTARJETA ; " %(tarjetainicio, tarjetafin))
                    
            PosEngine.execute(sql_code)
            print('Tarjeta fin %s, tiempo %s' %(tarjetafin, time() - t0))
        #    Connect.rollback()
            cont = 0
            t0 = time()    
            
    Connect.rollback()
    
#        sql_code = (" UPDATE THE_VIAJESMAYO A "
#                    " SET LATITUDPTO3 = B.LATITUDPTO3, "
#                    " LONGITUDPTO3 = B.LONGITUDPTO3, "
#                    " DISTANCIA = B.DISTANCIA "
#                    " FROM PROYECCIONRUTA B "
#                    " WHERE A.NROTARJETAEXTERNO = B.NROTARJETAEXTERNO "
#                    "  AND A.CODIGOTRXTARJETA = B.CODIGOTRXTARJETA "
#                )

#    PosEngine.execute(sql_code)
        
    
    
def proyLineaMuestra(PosEngine, lineaDesde, lineaHasta):

    print('Este procedimeinto graba en proyeccionruta y luego en THE_VIAJES_MUESTRA')
   
    cursorRamal = PosEngine.execute("SELECT a.LINEAMT, A.RAMALMT,A.LINEAGEO,A.RAMALGEO, sentido, geom "
                                    " FROM lineastrxgeo a, lineascole b "
                                    " where a.lineageo = b.linea2 and a.ramalgeo = ramal "
                                    "   and a.baja is null  AND lineageo >= '%s' "
                                    "   and lineageo < '%s' "
                                    "   and etapa in (2,3) "
                                    "order by a.lineageo, a.ramalgeo" % (lineaDesde, lineaHasta))  
    
    listShapPoint = []
    if cursorRamal.rowcount > 0 :
        # por cada ramal de la linea
        for ramal in cursorRamal.fetchall():      
            lineamt = ramal[0]
            ramalmt = ramal[1]
            sentido = ramal[4]
            print('procesando codigolinea %s ramal %s sentido %s' % (ramal[0],ramal[1], ramal[4]) ) 
        
            print('inicio cargar lotes')
            # cargo 25 lotes al azar
            cargarLotesAMuestra(PosEngine, lineamt,ramalmt, sentido, 25)                                
            print('fin cargar lotes')
            #recupero para cada viaje lo longitud y la latitud de los puntos de control anterior y siguiente, 
            #ademas se recupera el porcentaje del recorrido en que se encuentra el viaje desde el punto de control anterior al siguiente
            #finalmente se recupera el sentido primer punto de control
            sqlcode = ("SELECT B.NROTARJETAEXTERNO, B.CODIGOTRXTARJETA, A.LONGITUD longitudpto1, A.LATITUD latitudpto1, "
                       " C.LONGITUD longitudpto2, C.LATITUD latitudpto2, B.PORC_RECORRIDO, A.SENTIDO "
                        " FROM  PTOCONTROL201505_muestra A, THE_VIAJES_MUESTRA B, PTOCONTROL201505_muestra C "
                        " WHERE A.FILE_ID = B.FILE_ID "
                        "  AND A.C_CONTROL_POINT = B.C_CONTROL_POINT1  "
                        "  AND B.FILE_ID = C.FILE_ID "
                        "  AND B.C_CONTROL_POINT2 = C.C_CONTROL_POINT "                        
                        "  AND B.CODIGOLINEA = %s "
                        "  AND B.RAMAL = '%s' "
                        "  AND a.SENTIDO = '%s' "
                        "  AND B.DISTANCIA IS NULL  "
                        " ORDER BY B.FECHATRX " % (ramal[0],ramal[1], ramal[4]))

            viajes = sql.read_sql(sqlcode  , PosEngine)            
            
            #paso a shapely
            shplLine = wkt_load(ramal[5])
            
            viajestemp = pd.DataFrame()
            viajestemp['nrotarjetaexterno'] = ''
            viajestemp['codigotrxtarjeta']= ''
            viajestemp['latitudpto3'] = 0
            viajestemp['longitudpto3'] = 0
            viajestemp['distancia'] = 0
            
            shplLineIda = wkt_load(ramal[5]) 
            
            cantidad = len(viajes)

            for i, row in viajes.iterrows():                
                if mod(i, cantidad/100) == 0:
                    print('Puntos procesados al: %i porciento' % int(i*100/cantidad))
                    
                shplPoint1 = wkt_load("POINT(%s %s)" %  (row['longitudpto1'] , row['latitudpto1']))
                projPoint1 = shplLine.project(shplPoint1, normalized=True)
            
                shplPoint2 = wkt_load("POINT(%s %s)" %  (row['longitudpto2'] , row['latitudpto2']))
                projPoint2 = shplLine.project(shplPoint2, normalized=True)

                dist = projPoint1 + ((projPoint2 -projPoint1) * float(row['porc_recorrido']))
                puntoenlinea3 = shplLine.interpolate(dist, normalized=True)       
                
                viajestemp.loc[i,'nrotarjetaexterno'] = row['nrotarjetaexterno']
                viajestemp.loc[i,'codigotrxtarjeta'] = row['codigotrxtarjeta']
                viajestemp.loc[i,'latitudpto3'] = puntoenlinea3.y
                viajestemp.loc[i,'longitudpto3'] = puntoenlinea3.x
                viajestemp.loc[i,'distancia'] = dist
            
            viajestemp.to_sql('proyeccionruta', con=PosEngine, if_exists='append')

    print ('Actualizando tabla THE_VIAJES...')

    sql_code = (" UPDATE THE_VIAJES_MUESTRA A "
                " SET LATITUDPTO3 = B.LATITUDPTO3, "
                " LONGITUDPTO3 = B.LONGITUDPTO3, "
                " DISTANCIA = B.DISTANCIA "
                " FROM PROYECCIONRUTA B "
                " WHERE A.NROTARJETAEXTERNO = B.NROTARJETAEXTERNO "
                "  AND A.CODIGOTRXTARJETA = B.CODIGOTRXTARJETA ")

    PosEngine.execute(sql_code)
                        
#==============================================================================
# #funcion que evalua k-means iterativomente con los ditintos vaores valores de K
# #devuelve el valor de K optimo
#==============================================================================
def kmeansIterativo(X, k):
    #evaluacion por iteracion de silhouette
    eval = []
    for i in k:
        print(str('Procesando k == %i' %i))
        k_means = cluster.KMeans(n_clusters=i)  
        eval.append([i, bench_k_means(k_means, 'kmeans', X)])
    
    npeval = np.array(eval)        
    #determinar el mejor nro de clusters
    nclusters = int(npeval[npeval.argmax(axis=0)[1]][0])
    return [nclusters, npeval]

def plotSilhoutte(linea, ramal, sentido, nclusters, npeval, corrida):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_title("silhouette para linea %s ramal %s sentido %s" % (linea, ramal, sentido))
    ax1.set_xlabel('k clusters')
    ax1.set_ylabel('silhouette')
    ax1.plot(npeval[:,0], npeval[:,1], 'r-')
    ax1.axvline(x=nclusters, linewidth=1, color='r')
    plt.savefig('sil-linea%s-ramal%s-%s-corr%s.png' %(linea,ramal,sentido, corrida))   



def plotHist(linea, ramal, sentido, X, grupo, corrida):
    fig = plt.figure(figsize=(10, 5), dpi=100)    
    ax1 = fig.add_subplot(111)
    ax1.set_title("histograma para linea %s ramal %s sentido %s" % (linea, ramal, sentido))
    ax1.hist(X, 500, (0, 1), color=['black'], edgecolor = 'none')
    ax1.set_xlabel('mile post  (cant paradas: %s)' %len(grupo))
    ax1.set_ylabel('frecuencia  (cant. casos: %s)' % len(X) )
#    ax1.set_ylim(0,160)
    ax1.set_ylim(0,40)
    if len(grupo) > 0:
        for i, row in grupo.iterrows():
            ax1.axvline(row.limiteinf, color='b', linestyle='dashed', linewidth=1)
            ax1.axvline(row.centroide, color='r', linestyle=':', linewidth=1)
#            ax1.set_xticks([0,1])
#            ax1.set_xticklabels("12")
    plt.savefig('hist-linea%s-ramal%s-%s-corr%s.png' %(linea,ramal,sentido,corrida), dpi=1000)   
    
#==============================================================================
# FUNCION QUE DEVUELVE LOS LIMITES DEL CLUSTER 
#==============================================================================
def clusterLimit(X, linea, ramal, sentido, k_means, geom):
    
    res = np.vstack(np.array([X, k_means.labels_])).transpose()
    pdres = pd.DataFrame(res, columns=['valores','cluster'])
    grupo = pd.merge( pdres.groupby(['cluster']).min(),  pdres.groupby(['cluster']).max(), left_index=True, right_index=True, how='outer', suffixes=('_min', '_max'))
    grupo = grupo.sort('valores_min')
    shplLine = wkt_load(geom)

    #renumero los cluster ordenadamente, pego el centroide
    for idx, i in zip(grupo.index, range(len(grupo))):
        grupo.loc[idx, 'linea'] = linea
        grupo.loc[idx, 'ramal'] = ramal
        grupo.loc[idx, 'sentido'] = sentido
        grupo.loc[idx, 'clusterord'] = i
        grupo.loc[idx, 'centroide']  =  k_means.cluster_centers_[int(idx)]
        puntoaux = shplLine.interpolate(k_means.cluster_centers_[int(idx)], normalized=True)               
        grupo.loc[idx,'latitud'] = puntoaux.y
        grupo.loc[idx,'longitud'] = puntoaux.x
    
    #encontrar los limites de los clusters
    limites = grupo[['valores_min','valores_max']].values
    for idx, i in zip(grupo.index, range(len(grupo))):
        if i == 0:    
            grupo.loc[idx, 'limiteinf'] = 0
            grupo.loc[idx, 'limitesup'] = (limites[i,1]+limites[i+1,0])/2
        else:
            if i == len(limites) - 1:
                grupo.loc[idx, 'limiteinf'] = (limites[i-1,1]+limites[i,0])/2
                grupo.loc[idx, 'limitesup'] = 1
            else:
                grupo.loc[idx, 'limiteinf'] = (limites[i-1,1]+limites[i,0])/2
                grupo.loc[idx, 'limitesup'] = (limites[i,1]+limites[i+1,0])/2
    return grupo

#==============================================================================
# #BENCHMARK SILHOUETTE    
#==============================================================================
def bench_k_means(estimator, name, data):
#    sample_size = 10000
#    t0 = time()
    estimator.fit(data)
#    metric = metrics.silhouette_score(data, estimator.labels_, metric='euclidean', sample_size=sample_size)
    metric = metrics.silhouette_score(data, estimator.labels_, metric='euclidean')
#    print('% 9s   %.2fs    %i   %.3f' % (name, (time() - t0), estimator.inertia_, metric))
    return metric
    
    
def ClusterAnalisis(PosEngine, lineadesde, lineahasta, plt, corrida):
    
    #recorrer UNA TABLA CON TODAS LAS LINEAS Y LOS RAMALES
    
    sql_code = ("SELECT a.LINEAMT, A.RAMALMT,A.LINEAGEO,A.RAMALGEO, sentido, geom "
                " FROM lineastrxgeo a, lineascole b "
                " where a.lineageo = b.linea2 and a.ramalgeo = ramal and a.baja is null "
                " AND lineageo >= '%s' AND lineageo < '%s' "
                " and etapa in (2,3) "
                " order by a.lineageo, a.ramalgeo"                 
                % (lineadesde, lineahasta) )
               
    rutas = PosEngine.execute(sql_code)  
        
    for ruta in rutas.fetchall():
        
        lineageo = ruta.lineageo
        ramalgeo = ruta.ramalgeo
        sentido  = ruta.sentido
        lineamt  = ruta.lineamt
        ramalmt  = ruta.ramalmt
        
        
        print('procesando lineageo %s ramal %s sentido %s' % (ruta.lineageo, ruta.ramalgeo, ruta.sentido) ) 
            
        sqlcode = (" SELECT NROTARJETAEXTERNO, DISTANCIA "
                 "    FROM THE_VIAJES_MUESTRA A, PTOCONTROL201505_MUESTRA B "
                 "    WHERE A.C_CONTROL_POINT1 = B.C_CONTROL_POINT "
                 "      AND A.FILE_ID = B.FILE_ID "
                 "   	 AND A.CODIGOLINEA = %s "
                 "   	 AND A.RAMAL = '%s' "
                 "   	 AND (PORC_RECORRIDO < 0.04 OR PORC_RECORRIDO > 0.96) "
                 "   	 AND SENTIDO = '%s' "
                 "      AND DISTANCIA IS NOT NULL"
#                 "      AND DISTRUTA > 0 AND DISTRUTA < 94 "  #disruta, es la distancia del punto de control a la ruta
                 "    ORDER BY A.FECHATRX " % (lineamt, ramalmt, sentido) ) 
                                 
        viajes = sql.read_sql(sqlcode, PosEngine)           
        
        npViajes = np.unique(viajes["distancia"])
        
        if len(viajes) > 120 and len(npViajes) > 120:
            
            vecdist = viajes['distancia'].values
                        
            #determino el cluster ganador
            k=range(10,121)
            vecdistT = vecdist.reshape((len(vecdist), 1))
            [nclusters, npeval] = kmeansIterativo(vecdistT, k)
            
            if plt == 1:
                # grafico el resultado
                ramalcombinado = '%s%s' %(ruta.ramalmt, ruta.ramalgeo)
                plotSilhoutte(ruta.lineageo, ramalcombinado , ruta.sentido, nclusters, npeval, corrida)
            
            pdeval = pd.DataFrame(npeval)
            pdeval['corrida'] = corrida
            pdeval['lineamt'] = ruta.lineamt
            pdeval['ramalmt'] = ruta.ramalmt
            pdeval['sentido'] = ruta.sentido    
            pdeval.columns = ['k','shilo','corrida','lineamt','ramalmt','sentido']
            pdeval.to_sql("clusters", con=PosEngine, if_exists='append')
                        
            if plt == 1:
                plotHist(ruta.lineageo, ramalcombinado , ruta.sentido, vecdist, grupo, corrida)
        
        else:
            print('No hay suficientes datos')

def StopDetection(PosEngine, lineaDesde, lineaHasta, plot, db):
    print('Imprime masivamente el silhouette....')
    print('Debe existir la tabla Clusters creada con stop_clus')
    
    cursorRamal = PosEngine.execute("SELECT a.LINEAMT, A.RAMALMT,A.LINEAGEO,A.RAMALGEO, sentido, geom "
                                    " FROM lineastrxgeo a, lineascole b " 
                                    " where a.lineageo = b.linea2 and a.ramalgeo = ramal and a.baja is null  "
                                    " AND lineageo >= '%s' and lineageo < '%s' "
                                    " and etapa in (1) "
                                    " order by a.lineageo, a.ramalgeo" % (lineaDesde, lineaHasta))  
    
    for ramal in cursorRamal.fetchall():
        print('procesando lineaGEO %s ramalGEO %s sentido %s' % (ramal.lineageo, ramal.ramalgeo, ramal.sentido) ) 
        sqlcode = ("SELECT * FROM CLUSTERS WHERE LINEAMT = '%s' AND RAMALMT = '%s' AND SENTIDO = '%s' " % (ramal.lineamt, ramal.ramalmt, ramal.sentido))
        clusters = sql.read_sql(sqlcode  , PosEngine)
        
        if len(clusters) > 0:
            ramalcombinado = '%s%s' %(ramal.ramalmt, ramal.ramalgeo)
            fig = plt.figure()  
            ax1 = fig.add_subplot(111)
            ax1.set_title("silhouette para linea %s ramal %s sentido %s" % (ramal.lineamt, ramal.ramalmt, ramal.sentido))
            ax1.set_xlabel('k clusters')
            ax1.set_ylabel('silhouette')
            #largo = []
            
            nclustersaux = []
            #me quedo en rango con los numero distintos de corridas
            rango = np.unique(clusters['corrida'])

            for i in rango:
                k = clusters[clusters['corrida'] == i ]["k"].values
                silho = clusters[clusters['corrida'] == i ]["shilo"].values
                ax1.plot(k, silho , 'b-')
                npeval = np.array(clusters[clusters['corrida'] == i ][['k','shilo']])
                nclustersaux.append(int(npeval[npeval.argmax(axis=0)[1]][0]))
                
            # pregunto por si existe la Moda si es asi toma la moda sino la media        
            if pd.DataFrame(nclustersaux).mode().count().values[0] > 0:
                nclusters = pd.DataFrame(nclustersaux).mode().values[0][0]
            else:
                nclusters = int(pd.DataFrame(nclustersaux).median().values[0])
    
            ax1.axvline(x=nclusters, linewidth=1, color='r')
            plt.savefig('sil-linea%s-ramal%s-%s.png' %(ramal.lineageo, ramalcombinado , ramal.sentido)) 
            plt.close()
            
            if db == 1 or plot == 1:
                print('in')
                sqlcode = (" SELECT NROTARJETAEXTERNO, DISTANCIA "
                             "    FROM THE_VIAJES_MUESTRA A, PTOCONTROL201505_MUESTRA B "
                             "    WHERE A.C_CONTROL_POINT1 = B.C_CONTROL_POINT "
                             "      AND A.FILE_ID = B.FILE_ID "
                             "   	 AND A.CODIGOLINEA = %s "
                             "   	 AND A.RAMAL = '%s' "
                             "   	 AND (PORC_RECORRIDO < 0.04 OR PORC_RECORRIDO > 0.96) "
                             "   	 AND SENTIDO = '%s' "
                             "     AND DISTANCIA IS NOT NULL "
#                             "      AND DISTRUTA > 0 AND DISTRUTA < 94 "
                             "    ORDER BY A.FECHATRX " % (ramal.lineamt, ramal.ramalmt, ramal.sentido) ) 
                                         
                viajes = sql.read_sql(sqlcode, PosEngine)           
        
                if len(viajes) > nclusters:
                    vecdist = viajes['distancia'].values
                    vecdistT = vecdist.reshape((len(vecdist), 1))
                    k_means = cluster.KMeans(n_clusters=nclusters )
                    k_means.fit(vecdistT)                     
                    grupo = clusterLimit(vecdist, ramal.lineamt, ramal.ramalmt, ramal.sentido, k_means, ramal.geom)
                    
                    if db == 1:
                        #guardo las paradas en tabla 
                        grupo.to_sql("paradas", con=PosEngine, if_exists='append')           
                        
                    if plot == 1:
                        plotHist(ramal.lineageo, ramalcombinado , ramal.sentido, vecdist, grupo, 1)
                        plotHist(ramal.lineageo, ramalcombinado , ramal.sentido, vecdist, [], 5)
                        plotHistCrudo(PosEngine, ramal.lineamt, ramal.ramalmt, ramal.sentido, ramal.lineageo, ramalcombinado)
                else:
                    print('no enought data %s' %len(viajes))

def plotHistCrudo(PosEngine, lineamt, ramalmt, sentido, lineageo, ramalcombinado):

    sqlcode = (" SELECT NROTARJETAEXTERNO, DISTANCIA "
                             "    FROM THE_VIAJES_MUESTRA A, PTOCONTROL201505_MUESTRA B "
                             "    WHERE A.C_CONTROL_POINT1 = B.C_CONTROL_POINT "
                             "      AND A.FILE_ID = B.FILE_ID "
                             "   	 AND A.CODIGOLINEA = %s "
                             "   	 AND A.RAMAL = '%s' "
#                             "   	 AND (PORC_RECORRIDO < 0.04 OR PORC_RECORRIDO > 0.96) "
                             "   	 AND SENTIDO = '%s' "
                             "     AND DISTANCIA IS NOT NULL "
#                             "      AND DISTRUTA > 0 AND DISTRUTA < 94 "
                             "    ORDER BY A.FECHATRX " % (lineamt, ramalmt, sentido) ) 
                             
    viajes = sql.read_sql(sqlcode, PosEngine)   
    vecdist = viajes['distancia'].values  
    plotHist(lineageo, ramalcombinado , sentido, vecdist, [], 2)    