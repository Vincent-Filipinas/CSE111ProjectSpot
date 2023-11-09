-- Retrun all songs released for a given calender year
.headers on

SELECT
    song.s_released_month AS month,
    song.s_released_day AS day,
    song.s_trackname AS title
FROM
    song
WHERE
    song.s_released_year = 2016
ORDER BY
    song.s_released_month ASC,
    song.s_released_day ASC;
