.headers on
/* least streamed artist of the year*/
SELECT a_name as artist, s_streams as streams
FROM artist JOIN song ON a_artistkey = s_artistkey
WHERE s_streams = (SELECT MIN(s_streams) FROM song);