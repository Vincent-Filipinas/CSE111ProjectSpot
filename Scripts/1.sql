.headers on
/* most danceable and high energy songs*/
SELECT s_trackname as song_name, danceability_per, energy_per
FROM song JOIN stats on s_songkey = st_songkey
WHERE danceability_per >= 50 AND energy_per >= 50
ORDER BY danceability_per desc, energy_per desc;