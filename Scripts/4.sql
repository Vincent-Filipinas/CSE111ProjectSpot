.headers on
/* streamed songs from least to most*/
SELECT a_name as artist, s_streams
FROM artist JOIN song ON a_artistkey = s_artistkey
ORDER BY s_streams ASC;