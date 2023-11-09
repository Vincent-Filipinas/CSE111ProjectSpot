.headers on
/*most popular song within all platform charts*/
SELECT s_trackname as song, c_inspotify_chart as spotify_chart, c_inapple_chart as apple_chart, c_indeezer_chart as deezer_chart
FROM song JOIN charts ON s_songkey = c_songkey
ORDER BY c_inapple_chart DESC, c_indeezer_chart DESC, c_inspotify_chart DESC
LIMIT 1;