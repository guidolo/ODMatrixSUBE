DISTANCIAS (la carga phyton) -- distancias de cada punto con las lineas de colectivo. La distancia viene expresada en km.


drop table distancias;

create table distancias
(
  Punto bigint,
  LineaMT text,
  RamalMT text,
  LineaGeo text,
  RamalGeo text,
  SentidoGeo text,
  Distancia double precision
);


SELECT count(*) FROM distancias;
--28.540.920
--27.980.151

