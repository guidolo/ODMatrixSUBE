# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 11:48:49 2015

@author: gsidoni
"""

#PROCEDIMIENTO QUE COMPILADA TODA LA EJECUCIÓN COMPLETA 
import sys
import os
os.chdir('i:\\tesis\\')

import shapely

sys.path.insert(0, 'i:\\tesis\\Repositorio Python\\Conections\\')
import connects

sys.path.insert(1, 'i:\\tesis\\Repositorio Python\\Tesis\\')
import Background as bk
import LineAnalisys as la
import SignDetection as sg
import StopDetection as sd
import DestinyAsign as da
#import Procedures  as prc
#from SignDetection import sentido_ejecutar
#from IdentificacionParadas import test



if __name__ == '__main__':
    if(len(sys.argv) < 1):
        sys.stderr.write('Parametros requeridos: FECHA INGRESO FORMATO YYYYMMDD\n')
        exit
    
    if sys.argv[1] == '-h':
        print('Este es un programa para la generacion de una matriz OD')
        print('')
        print('Comandos permitidos: ')
        print('-reco        : extrae de un shapefile los recorridos')
        print('-truncate    : vacía tablas temporales')
        print('-dist        : calculo de distancias entre puntos de control y recorridos. Parametros lineaDesde lineaHasta')
        print('-dist_test   : genera csv con datos extras para pruebas. Par lineaDesde lineaHasta')
        print('-dist_RMSE   : calcula para las lineas que no tienen relacion en el archivo de shape todos los RMSE con todas las lineas del archivo para ver cual tiene mejor ajuste')
        print('-sign        : asigna el sentido Ida o Vuelta segun putnos de control')
        print('-sign_test   : como -sign pero deja registros para test')
        print('-sign_ag     : agrupa los puntos de control de ida y vuelta para crear servicios')        
        print('-stop_proy   : proyecta los puntos de control sobre las rutas adecuadas. No solo toma el pto de control sino que toma el porcentaje de tamo recorrido por cada viaje y calcula el mile post en funcion')
        print('-stop_proy_muestra   : proyecta los puntos de control sobre las rutas adecuadas. Toma datos de muestra')
        print('-stop_clus   : corre cluster masivo para k de 10 a 120')
        print('-stop_det    : imprime masivamente los silhuette y graba tabla paradas')
        print('-stop_matrix : genera la matriz de las distancias entre paradas con menor distancia')
        print('-ori_asign   : asigna el origen en base a la tabla de paradas')
        print('-destiny_asign: asigna el destino del viaje en la tabla the_viajesmayo')
        
    #coneccion con POSGRESQL
    PosEngine, PosConnect = connects.PostgreSQLConnectSQLAlchemy()
    if sys.argv[1] == 'nada':
        print('nada')
    
    if sys.argv[1] == '-help':
        print('Probar con -h')
        
    if sys.argv[1] == '-reco':
    
        #PASO 1: dado un shape de recorridos, los paso a una tabla 
        #guarda la rabla "LineasCole"
        shpRecorridos = 'Recorridos.shp'
        bk.extraeLineaShp(shpRecorridos, PosEngine)
    
    if sys.argv[1] == '-truncate':
        bk.truncate(PosEngine)

    if sys.argv[1] == '-lot':
        #==============================================================================
        # #PASO 2: crea ta tabla distancias
        #==============================================================================
        #2.1 creacion de la tabla lote y de puntos de control 
        prc.lotes(PosEngine)

    if sys.argv[1] == '-dist':
        #3 CREACION DE LA TABLA DE DISTANCIAS
    
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        shp = 0  #1 genera archivos shape / 0 no los genera
        db  = 1  #1 gurda en base de datos / 0 no guarda
        tst = 0  #1 genera archivo de test / 0 no lo genera
        print('Comenzando trabajo desde %s a %s' %(lineaDesde, lineaHasta))
        la.distPtoLinea(PosEngine, lineaDesde, lineaHasta, shp, db, tst )
    
    if sys.argv[1] == '-dist_test':
        #generación de alrchivo csv de test
        print('Se va a generar un archivo csv con datos de prueba para validar distancias')
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        shp = 0  #1 genera archivos shape / 0 no los genera
        db  = 0  #1 gurda en base de datos / 0 no guarda
        tst = 1  #1 genera archivo de test / 0 no lo genera
        la.distPtoLinea(PosEngine, lineaDesde, lineaHasta, shp, db, tst )

    if sys.argv[1] == '-dist_RMSE':
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        la.calcRMSE(PosEngine, lineaDesde, lineaHasta)


    if sys.argv[1] == '-dist_long':
        #generación de alrchivo csv de test
        print('Se va a generar la tabla largos con las distancias en Km de las rutas')
        la.largoRuta(PosEngine)     

    if sys.argv[1] == '-sign':
        #PASO 4: Sign Detection. Deteccion del sentido del colectivo
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        tst = 0
        sg.sentido_ejecutar(PosEngine, lineaDesde, lineaHasta, tst)
        
    if sys.argv[1] == '-sign_test':
        #PASO 4: Sign Detection. Deteccion del sentido del colectivo
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        tst = 1
        sg.sentido_ejecutar(PosEngine, lineaDesde, lineaHasta, tst)

    if sys.argv[1] == '-sign_ag':
        # agrupa en la tbla signoag los signos agrupados
        linea = str(sys.argv[2])
        sg.agrupaSigno(PosEngine, linea)

    if sys.argv[1] == '-stop_cargar_muestra':
        lineamt = str(sys.argv[2])
        ramalmt = str(sys.argv[3])
        sentido = str(sys.argv[4])
        cantidadLotes = str(sys.argv[5])
        sd.cargarLotesAMuestra(PosEngine, lineamt, ramalmt, sentido, cantidadLotes)

    if sys.argv[1] == '-stop_proy':
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        sd.proyLinea(PosEngine, lineaDesde, lineaHasta)
        
    if sys.argv[1] == '-stop_proy_muestra':
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        sd.proyLineaMuestra(PosEngine, lineaDesde, lineaHasta)
        
    if sys.argv[1] == '-stop_clus':
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        corrida = str(sys.argv[4])
        plt = 0
        sd.ClusterAnalisis(PosEngine, lineaDesde, lineaHasta, plt, corrida)
    
    if sys.argv[1] == '-stop_det':
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        plt = 1
        db = 0
        sd.StopDetection(PosEngine, lineaDesde, lineaHasta, plt, db)
    
    if sys.argv[1] == '-stop_matrix':
        da.distaciaParadas(PosEngine)
        
    if sys.argv[1] == '-stop_updv':
        Connect = connects.PostgreSQLConnect()
        sd.actualizarViajes(Connect, PosEngine)
        Connect.rollback()
        Connect.close()
    
    if sys.argv[1] == '-ori_asign':
        lineaDesde = str(sys.argv[2])
        lineaHasta = str(sys.argv[3])
        da.asignOrigen(PosEngine, lineaDesde, lineaHasta)
    
    if sys.argv[1] == '-destiny_asign_tst':
        nrotar =  str(sys.argv[2])
        tst = 1
        da.asignDestiny(PosEngine, 0, nrotar, tst)
        
    if sys.argv[1] == '-destiny_asign':
        tst = 0
        dia =  str(sys.argv[2])
        da.asignDestiny(PosEngine, dia, 0, tst)
        #da.addFechaDestino(PosEngine)