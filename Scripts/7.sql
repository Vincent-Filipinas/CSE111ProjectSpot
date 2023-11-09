.headers on
/* most recent released songs*/
SELECT s_trackname as song, s_released_year, s_released_month, s_released_day
FROM song
ORDER BY s_released_year DESC, s_released_month DESC, s_released_day DESC;