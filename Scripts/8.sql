.headers on
/* song with the most beats along with energy and liveness*/
SELECT s_trackname as song, s_bpm, energy_per as energy, liveness_per as liveness
FROM song JOIN stats ON s_songkey = st_songkey
ORDER BY s_bpm desc, energy_per desc, liveness_per desc
LIMIT 1;