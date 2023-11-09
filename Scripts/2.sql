.headers on
/* most streamed song on spotify*/
SELECT s_trackname as number_oneSong, s_streams
FROM song
WHERE s_streams == (SELECT MAX(s_streams) FROM song);
