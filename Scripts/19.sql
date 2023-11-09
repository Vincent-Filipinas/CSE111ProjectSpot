.headers on

SELECT
    s_trackname,
    c_inspotify_chart as spotify_chart
FROM
    song
    JOIN charts on s_songkey = c_songkey
ORDER BY c_inspotify_chart DESC
LIMIT 10;
