-- Return a list all the songs with an instance of a substring
.headers on

 SELECT
    song.s_trackname AS title,
    artist.a_name AS by_artist
 FROM
     song
     INNER JOIN artist ON song.s_artistkey = artist.a_artistkey
 WHERE song.s_trackname LIKE '%happy%';