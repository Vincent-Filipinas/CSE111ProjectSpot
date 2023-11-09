.headers on

/* most streamed song by taylor swift*/
SELECT s_trackname as song, a_name as artist
from song JOIN artist ON a_artistkey = s_artistkey
WHERE a_name LIKE '%Taylor Swift%' AND s_streams = (SELECT MAX(s_streams) FROM song JOIN artist ON a_artistkey = s_artistkey WHERE a_name LIKE '%Taylor Swift%');