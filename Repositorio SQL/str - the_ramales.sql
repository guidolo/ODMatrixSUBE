

SELECT count(*) FROM THE_RAMALES ;
--1419

SELECT count(*) FROM THE_RAMALES where linea2 is null;
--55 nulos

SELECT * FROM THE_RAMALES where linea2 is null;


SELECT LINEA2, RAMAL 
FROM THE_RAMALES 
group BY LINEA2, RAMAL 
having count(*) > 1;
--no tiene duplicados

SELECT *
FROM THE_RAMALES
where linea2 is not null 
ORDER BY LINEA2, RAMAL ;
 

select  count(*)
from lineastrxgeo
where baja is null;
--773

select * 
from lineastrxgeo
where lineamt || '-' || ramalmt in  (
			select  lineamt || '-' || ramalmt
			from lineastrxgeo
			where baja is null
			group by lineamt, ramalmt
			having count(*) > 1
 )
 order by lineamt, ramalmt;
--no hay duplicados entre las lineas sin baja

----------------------------------------------------------------------------
-------------- ESTA CONSULTA MUESTRA QUE MUCHAS LINEAS NO FUERNO TENIDAS EN CUENTA -------------
------------- esto es claramente un error inicial de carga. Muchas lineas tenias cantidad suficiente de -----
------------- transacciones como para ser tenidas en cuenta pero sin embargo no fueron procesadas -----
-------------- creo que el preblema lo tuvo el proceso ORACLE inicial que cargaba los 25 lotes

with trxgeo as (
	select  *
	from lineastrxgeo
	where baja is null
	)
SELECT *
FROM THE_RAMALES a full outer join trxgeo b on  cast(a.codigolinea as varchar) = b.lineamt and a.RAMAL = b.ramalmt
order by cantidad_trx ;


-------------------------------------------------------------------------------------------------------
