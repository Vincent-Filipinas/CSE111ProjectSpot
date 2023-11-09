.headers on

-- song in the most amount of playlist amongst spotify
SELECT
    s_trackname,
    p_inspotify_playlist as spotify_playlist
FROM
    song
    JOIN playlist on s_songkey = p_songkey_playlist
ORDER BY p_inspotify_playlist DESC
LIMIT 10;
