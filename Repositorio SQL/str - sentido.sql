CREATE TABLE sentido
(
  index bigint,
  linea text,
  ramal text,
  file_id integer,
  c_control_point integer,
  longitud numeric,
  latitud numeric,
  fechapto date,
  segundospto integer,
  DistAIda numeric,
  MilePostIda numeric,
  DistAVuelta numeric,
  MilePostVuelta numeric,
  Sentido character varying(2),
  SentidoHis text,
  MilePost numeric
);


select to_date('20150505','yyyymmdd')  from sentido limit 1;

select * from sentido where linea = '180' order by fechapto desc;

select * from sentido where file_id = 38863981;

SELECT * FROM PTOCONTROL201505;



