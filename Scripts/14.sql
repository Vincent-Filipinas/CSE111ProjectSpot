-- Return a list of the 20 most streamed songs that are in a given key 
.headers on

SELECT
    song.s_trackname AS title,
    song.s_streams AS streamed_cnt,
    song.s_key AS in_key
FROM
    song
WHERE
    song.s_key = 'C#'
ORDER BY song.s_streams DESC
LIMIT 20;
