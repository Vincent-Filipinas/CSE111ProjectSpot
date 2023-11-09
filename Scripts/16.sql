-- Which song has the most streams for its respective release year
.headers on

 SELECT
     song.s_released_year AS year,
     song.s_trackname AS title,
     artist.a_name AS made_by,
     MAX(song.s_streams) AS most_streams
 FROM
     song
     INNER JOIN artist ON song.s_artistkey = artist.a_artistkey
GROUP BY
    song.s_released_year;