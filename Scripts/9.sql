.headers on
/* songs by/features taylor swift */
SELECT s_trackname as song
from song JOIN artist ON a_artistkey = s_artistkey
WHERE a_name LIKE '%Taylor Swift%';