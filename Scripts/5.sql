.headers on
/* song in the most amount of playlist amongst all platforms*/
SELECT s_trackname, p_inspotify_playlist as spotify_playlist, p_inapple_playlist as apple_playlist, p_indeezer_playlist as deezer_playlist
FROM song JOIN playlist on s_songkey = p_songkey_playlist
WHERE p_inspotify_playlist > p_indeezer_playlist AND p_inspotify_playlist > p_inapple_playlist
ORDER BY p_inspotify_playlist DESC
LIMIT 1;