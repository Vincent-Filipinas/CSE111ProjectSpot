-- Generate a list of most danceable songs from the 2000's
.headers on

SELECT
    stats.danceability_per AS dance_percentage,
    song.s_trackname AS title,
    song.s_released_year AS year_released
FROM
    song
    INNER JOIN stats ON song.s_songkey = stats.st_songkey
WHERE
    song.s_released_year BETWEEN 2000 AND 2009
    AND stats.danceability_per > 70
ORDER BY
    stats.danceability_per ASC
LIMIT 15;
