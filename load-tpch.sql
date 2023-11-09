.mode csv
.headers off
.separator "," 
.import -skip 1 archive/Artist.csv artist
.import -skip 1 archive/Song.csv song
.import -skip 1 archive/Playlist.csv playlist
.import -skip 1 archive/Stats.csv stats
.import -skip 1 archive/Charts.csv charts
