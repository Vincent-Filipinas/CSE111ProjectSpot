-- Which month and year had the most songs released
.headers on

 SELECT
     song.s_released_year AS year,
     song.s_released_month AS month,
     COUNT(song.s_released_month) AS release_cnt
 FROM
     song
GROUP BY
    song.s_released_year,
    song.s_released_month
ORDER BY
    release_cnt DESC
LIMIT 1;