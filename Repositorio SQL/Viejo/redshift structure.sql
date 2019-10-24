
rollback

select current_user;

ABORT

copy venue from 's3://awssampledbuswest2/tickit/venue_pipe.txt' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' delimiter '|';

drop table MOVIMIENTOTARJETA

/*************** configuracion del EC2 para acceder al S3************************************/

A client error (InvalidAccessKeyId) occurred when calling the ListObjects operation: The AWS Access Key Id yo
does not exist in our records.
PS C:\Users\Administrator> aws configure
AWS Access Key ID [****************ator]: AKIAJ7LPJ7ZDXU6DCYVQ
AWS Secret Access Key [****************!(sm]: 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
Default region name [us-west-2]: us-west-2
Default output format [txt]:
PS C:\Users\Administrator> aws s3 ls s3://guidolo-repositorio1
                           PRE load/
/* ****************************************************************************************** */


CREATE TABLE MOVIMIENTOTARJETA2
(CODIGOTRXTERMINAL INTEGER,
MONTO  varchar(20),
SALDO  varchar(20),
CANTTRX INTEGER,
CODIGOROL VARCHAR(20),
CODIGOERROR INTEGER,
CODIGOTIPOTRX INTEGER,
CODIGOENTIDAD INTEGER,
CODIGOTIPOTARJETA INTEGER,
CODIGOTERMINAL INTEGER,
CODIGOSITIO INTEGER,
NROTARJETA int8,
FECHATRX DATETIME,
CODIGOTIPOTECNOLOGIA INTEGER,
CODIGOCONTRATO INTEGER,
CODIGOTRXTARJETA INTEGER,
CODIGOLINEA INTEGER,
ENTIDADFINANCIERA INTEGER,
FECHAINGRESO DATETIME,
IDARCHIVOINTERCAMBIO INTEGER,
IDINCONSISTENCIA VARCHAR(20),
MONEDERO_ID INTEGER,
EMISOR_CONTRATO INTEGER,
NROTARJETAEXTERNO INTEGER,
SAM_ID VARCHAR(30),
LG_ID VARCHAR(50),
TIPO_TERMINAL INTEGER,
ACCION_HL INTEGER,
ID_COMBINACION INTEGER,
ID_REGLA_COMBINACION INTEGER,
VALOR_TARIFA varchar(20),
ID_SERVICIO INTEGER,
ENTIDAD_EMISORA_TARJ INTEGER,
VERSION_TIPO_TRX INTEGER,
TIPOMAPPING INTEGER,
ID_INTEGRADOR INTEGER,
CODIGOTRAYECTO INTEGER,
EMISOR_MONEDERO INTEGER,
CODIGOSUBTIPOTRX INTEGER,
SECCION_FIN INTEGER,
SECCION_INICIO INTEGER,
DESCUENTO varchar(20),
PROVISION varchar(20),
ID_POSICIONAMIENTO INTEGER,
PTC INTEGER,
LTC INTEGER,
CODIGOTIPOLINEA VARCHAR(30)
);


truncate table MOVIMIENTOTARJETA2

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140801.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140802.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140803.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140804.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140805.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140806.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

	falló
	copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140807.CSV' 
	CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140808.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140809.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140810.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

	fallo
	copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140811.CSV' 
	CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140812.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140813.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;
	fail
	copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140814.CSV' 
	CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

	copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140815.CSV' 
	CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

	copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140816.CSV' 
	CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

	copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140817.CSV' 
	CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140818.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;



copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140819.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140820.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140821.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140822.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140823.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140824.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140825.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140826.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140827.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140828.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140829.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140830.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

copy MOVIMIENTOTARJETA2 from 's3://guidolo-repositorio1/load/DATA_ADATOPRD_MT20140831.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS' delimiter ';' IGNOREHEADER as 1;

			
select * from stl_load_errors;



select codigoentidad, count(*)
from movimientotarjeta
group by codigoentidad

/********************** CREATE TABLE EXP_POSITIONING *********************************/

DROP TABLE  POSITIONING

CREATE TABLE TEMP_POSITIONING
	(TRX_POSITIONING_ID INTEGER,
	INSERTION_DATE DATETIME,
	FILE_ID INTEGER,
	C_OPERATOR_ID INTEGER,
	C_SERVICE_ID INTEGER,
	C_CONTROL_POINT INTEGER,
	C_DEVICE_STATUS INTEGER,
	C_LM_ID INTEGER,
	C_LD_ID INTEGER,
	RECORD_POSITION INTEGER,
	RECORD_TYPE INTEGER,
	RECORD_VERSION INTEGER,
	DTSN INTEGER,
	DATE_TIME DATETIME,
	CONTROL_POINT INTEGER,
	LINE_DETAIL INTEGER,
	SEQUENCE INTEGER,
	TYPE INTEGER,
	DIRECTION INTEGER,
	TP_ID INTEGER,
	VEHICLE INTEGER,
	DEVICE INTEGER,
	LONGITUDE VARCHAR(20) ,
	LATITUDE VARCHAR(20),
	VELOCITY FLOAT,
	DISTANCE FLOAT,
	STATUS INTEGER)

ALTER TABLE TEMP_POSITIONING
ADD LONGITUD FLOAT

ALTER TABLE TEMP_POSITIONING
ADD  LATITUD FLOAT

UPDATE TEMP_POSITIONING SET LONGITUD  = CAST(REPLACE(LONGITUDE, ',','.') AS FLOAT(10) ),
														LATITUD   = CAST(REPLACE(LATITUDE, ',','.') AS FLOAT(10) )
														

copy TEMP_POSITIONING from 's3://guidolo-repositorio1/load/Positioning/DATA_ADAN_TRX_POSITIONING_20140801.csv' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS'  delimiter ';' IGNOREHEADER as 1;

copy TEMP_POSITIONING from 's3://guidolo-repositorio1/load/Positioning/DATA_ADAN_TRX_POSITIONING_20140802.csv' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS'  delimiter ';' IGNOREHEADER as 1;

copy TEMP_POSITIONING from 's3://guidolo-repositorio1/load/Positioning/DATA_ADAN_TRX_POSITIONING_20140803.csv' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS'  delimiter ';' IGNOREHEADER as 1;

copy TEMP_POSITIONING from 's3://guidolo-repositorio1/load/Positioning/DATA_ADAN_TRX_POSITIONING_20140804.csv' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS'  delimiter ';' IGNOREHEADER as 1;

copy TEMP_POSITIONING from 's3://guidolo-repositorio1/load/Positioning/DATA_ADAN_TRX_POSITIONING_20140805.csv' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS'  delimiter ';' IGNOREHEADER as 1;

copy TEMP_POSITIONING from 's3://guidolo-repositorio1/load/Positioning/DATA_ADAN_TRX_POSITIONING_20140806.csv' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS'  delimiter ';' IGNOREHEADER as 1;

select * from stl_load_errors


SELECT COUNT(*) FROM TEMP_POSITIONING

DROP TABLE LINEA

CREATE TABLE LINEA
(
	IDLINEA	INTEGER,
	CODIGOTIPOLINEA INTEGER,
	DESCRIPCION VARCHAR(1000),
	CODIGOGRUPOTARIFARIO VARCHAR(20),
	CODIGOCORREDOR VARCHAR(20),
	FECHABAJA VARCHAR(20),
	AREAGEOGRAFICA INTEGER,
	CODIGOZONADESTINO VARCHAR(20),
	AG VARCHAR(20),
	RUF VARCHAR(20),
	FECHAALTA VARCHAR(20),
	CODIGOSAEF VARCHAR(20),
	CODIGOAFT VARCHAR(20),
	MV_CODSAEF VARCHAR(20),
	MV_CODAFT VARCHAR(20),
	MV_LABELMON VARCHAR(20),
	CODSAEF VARCHAR(20),
	CODAFT VARCHAR(20),
	FECHAVIGENCIA VARCHAR(20),
	DESCRIPCIONCORTA VARCHAR(50),
	CODIGOLINEA VARCHAR(200)
)

copy LINEA from 's3://guidolo-repositorio1/load/Lineas/LINEA.csv' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS'  delimiter ';' IGNOREHEADER as 1;

select * from stl_load_errors

SELECT * FROM LINEA 

/****************************** LOTE *********************************************/

CREATE TABLE LOTE
(ID_LOTE INTEGER,
FECHA_INGRESO_LOTE DATETIME,
REF_EXT INTEGER
)


copy LOTE from 's3://guidolo-repositorio1/load/Lote/LOTEAgo.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS'  delimiter ';' IGNOREHEADER as 1;

copy LOTE from 's3://guidolo-repositorio1/load/Lote/LOTESep.CSV' 
CREDENTIALS 'aws_access_key_id=AKIAJ7LPJ7ZDXU6DCYVQ;aws_secret_access_key=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' TIMEFORMAT AS 'DD/MM/YYYY HH24:MI:SS'  delimiter ';' IGNOREHEADER as 1;

Select top 100 * from Lote

/*****************LINEA  26/12/2014 *************************************************



/**************** 16 / 12 / 2014 ****************************************************/
/****** creacion de la tabla de Esquinas *******************************************/

DROP TABLE NODOS

CREATE TABLE NODOS
(NODOWKT VARCHAR(200))

CREATE TABLE ESQUINAS
(ESQUINAWKT VARCHAR(200))

/************************************************************************************/

Select distinct datepart('day', fechaingreso) from MOVIMIENTOTARJETA2;

Select TOP 100 * 
from MOVIMIENTOTARJETA2
where fechaingreso > to_date('20140802','yyyymmdd');

Select * from lote where id_lote = 43266191

create view punto as
Select top 100 latitude, longitude from temp_positioning where file_id = 22776312 order by c_control_point

Select top 100 * from temp_positioning where file_id = 22776312 order by c_control_point


select * from punto

;
select trunc(fechaingreso), count(*)
from movimientotarjeta2
group by trunc(fechaingreso)
order by trunc(fechaingreso);




