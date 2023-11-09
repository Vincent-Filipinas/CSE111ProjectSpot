-- generate a list of 10 most streamed songs released on the a specific day and month
.headers on

SELECT
    song.s_trackname AS titles,
    song.s_streams AS numOfStreams
FROM
    song
WHERE
    song.s_released_day = 10 AND song.s_released_month = 06
ORDER BY
    song.s_trackname DESC,
    song.s_streams DESC
LIMIT 10;
