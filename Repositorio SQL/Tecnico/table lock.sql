SELECT*
FROM pg_catalog.pg_locks l;


SELECT blockeda.pid AS blocked_pid, blockeda.query as blocked_query,
  blockinga.pid AS blocking_pid, blockinga.query as blocking_query
FROM pg_catalog.pg_locks blockedl
JOIN pg_stat_activity blockeda ON blockedl.pid = blockeda.pid
JOIN pg_catalog.pg_locks blockingl ON(blockingl.transactionid=blockedl.transactionid
  AND blockedl.pid != blockingl.pid)
JOIN pg_stat_activity blockinga ON blockingl.pid = blockinga.pid
WHERE NOT blockedl.granted ;


SELECT locktype, relation::regclass,mode, transactionid AS tid,
virtualtransaction AS vtid,pid, granted
FROM pg_catalog.pg_locks l LEFT JOIN pg_catalog.pg_database db
ON db.oid=l.database WHERE (db.datname='sandbox' OR db.datname IS NULL)
AND NOT pid = pg_backend_pid();

SELECT pg_cancel_backend(3084); 
