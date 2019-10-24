--To cancel a running query, use the CANCEL command with the query's PID.

--To find the process ID, query the STV_RECENTS table, as shown in the previous step. The following example shows how you can make the results more readable by using the TRIM function to trim trailing spaces and by showing only the first 20 characters of the query string.

select pid, trim(user_name), starttime, substring(query,1,20), *
from stv_recents
where status='Running';

/*
The result looks something like this:

  pid  |   btrim    |         starttime          |      substring
-------+------------+----------------------------+----------------------
 18764 | masteruser | 2013-03-28 18:39:49.355918 | select sellerid, fir
(1 row)

To cancel the query with PID 18764, issue the following command:
*/

cancel 30800;
