-- Return list of songs that are one attribute but not so much of another attribute
.headers on

 SELECT
    song.s_trackname AS title,
    artist.a_name AS by_artist
 FROM
     song
     INNER JOIN stats ON song.s_songkey = stats.st_songkey
     INNER JOIN artist ON song.s_artistkey = artist.a_artistkey
 WHERE acousticness_per > 70 AND liveness_per < 30
 LIMIT 10;