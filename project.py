import sqlite3
from sqlite3 import Error



def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def createTable(_conn):
    
    try:
        cursor = _conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS new_playlist (
                p_artistname char(100) not null,
                p_artistkey decimal(3,0) not null,
                p_songkey decimal(3,0) not null,
                p_trackname  char(100) not null,
                p_released_year  decimal(4,0) not null,
                p_released_month  decimal(2,0) not null,
                p_released_day decimal(2,0) not null,
                p_labelname char(100) not null
            )
        ''')
        _conn.commit()
        
    except Error as e:
        print(e)

def createList(_conn):
    
    try:
        cursor = _conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_playlist (
                u_artistname char(100) not null,
                u_songkey decimal(3,0) not null,
                u_trackname  char(100) not null,
                u_released_year  decimal(4,0) not null,
                u_released_month  decimal(2,0) not null,
                u_released_day decimal(2,0) not null
            )
        ''')
        _conn.commit()
        
    except Error as e:
        print(e)


def dropList(_conn):
    
    try:
        cursor = _conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS user_playlist')
        _conn.commit()
       
    except Error as e:
        print(e) 

def dropTable(_conn):
    
    try:
        cursor = _conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS new_playlist')
        _conn.commit()
        
    except Error as e:
        print(e) 


def displayPlaylist(conn):
    cursor = conn.cursor()
    display_query = "SELECT u_artistname, u_trackname FROM user_playlist"
    cursor.execute(display_query)
    playlist_songs = cursor.fetchall()

    print("\nCreated Playlist:")
    for artist_name, track_name in playlist_songs:
        print(f"{artist_name} - {track_name}")

def search_song_by_stats(conn):
    streams = input("Enter minimum number of streams to search for: ")
    query = "SELECT s_trackname, a_name, s_streams FROM song JOIN artist ON song.s_artistkey = artist.a_artistkey WHERE s_streams >= ?"
    cursor = conn.cursor()
    cursor.execute(query, (streams,))
    results = cursor.fetchall()

    if results:
        print("\nSearch Results Based on Streams:")
        for track_name, artist_name, stream_count in results:
            print(f"{track_name} by {artist_name} - Streams: {stream_count}")
    else:
        print("No songs found with streams above the specified number.")


def artist_exists(conn, artist_name):
    query = "SELECT COUNT(*) FROM artist WHERE a_name LIKE ?"
    cursor = conn.cursor()
    cursor.execute(query, (artist_name,))
    return cursor.fetchone()[0] > 0

def song_exists(conn, song_name):
    query = "SELECT COUNT(*) FROM song WHERE s_trackname LIKE ?"
    cursor = conn.cursor()
    cursor.execute(query, (song_name,))
    return cursor.fetchone()[0] > 0

def show_songs(conn, limit=10, offset = 0):
    query = f"SELECT DISTINCT s_trackname FROM song LIMIT {limit} OFFSET {offset}"
    cursor = conn.cursor()
    cursor.execute(query)
    songs = cursor.fetchall()
    for song in songs:
        print(song[0])  # Display each artist name

def show_artists(conn, limit=10, offset = 0):
    query = f"SELECT DISTINCT a_name FROM artist LIMIT {limit} OFFSET {offset}"
    cursor = conn.cursor()
    cursor.execute(query)
    artists = cursor.fetchall()
    for artist in artists:
        print(artist[0])  # Display each artist name

def show_years(conn):
    query_min = "SELECT MIN(s_released_year) FROM song"
    query_max = "SELECT MAX(s_released_year) FROM song"
    cursor = conn.cursor()
    cursor.execute(query_min)
    min_year = cursor.fetchone()[0]
    cursor.execute(query_max)
    max_year = cursor.fetchone()[0]
    print(f"Earliest Year: {min_year}, Latest Year: {max_year}")

def insert_song(conn, song_name):
    select_query = """
    SELECT a_name, s_songkey, s_trackname, s_released_year, s_released_month, s_released_day 
    FROM artist 
    JOIN song ON artist.a_artistkey = song.s_artistkey 
    WHERE s_trackname LIKE ?
    """
    cursor = conn.cursor()
    cursor.execute(select_query, (song_name,))
    songs = cursor.fetchall()

    for song in songs:
        insert_query = """
        INSERT INTO user_playlist (u_artistname, u_songkey, u_trackname, u_released_year, u_released_month, u_released_day)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        cursor.execute(insert_query, song)
    
    conn.commit()


def create_playlist(conn, artist=None, year=None, mood=None, mood_value=50):
    # Building the query to fetch and insert songs based on artist, year, and mood
    select_query = """
    SELECT a_name, a_artistkey, s_songkey, s_trackname, s_released_year, s_released_month, s_released_day, label_name
    FROM artist join record_labels ON record_labels.l_artistkey = artist.a_artistkey
    JOIN song ON artist.a_artistkey = song.s_artistkey 
    LEFT JOIN stats ON song.s_songkey = stats.st_songkey
    """
    conditions = []
    if artist:
        conditions.append(f"artist.a_name LIKE '%{artist}%'")
    if year:
        conditions.append(f"song.s_released_year = {year}")
    if mood:
        conditions.append(f"stats.{mood} >= {mood_value}")

    if conditions:
        select_query += " WHERE " + " AND ".join(conditions)

    cursor = conn.cursor()
    cursor.execute(select_query)
    songs = cursor.fetchall()

    # Inserting songs into new_playlist
    for song in songs:
        insert_query = """
        INSERT INTO new_playlist (p_artistname, p_artistkey, p_songkey, p_trackname, p_released_year, p_released_month, p_released_day, p_labelname)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(insert_query, song)
    
    conn.commit()

    display_query = "SELECT p_artistname, p_trackname, p_released_year,p_released_month,p_released_day, p_labelname FROM new_playlist"
    cursor.execute(display_query)
    playlist_songs = cursor.fetchall()

    print("\nSearch Result:")
    for artist_name, track_name, year, month, day, labelname in playlist_songs:
        print(f"{artist_name} - {track_name} {year}-{month}-{day} {labelname}")

def load_playlist(conn):
    # Query to check if the user_playlist table exists
    check_table_query = """
    SELECT name FROM sqlite_master WHERE type='table' AND name='user_playlist';
    """
    cursor = conn.cursor()
    cursor.execute(check_table_query)
    result = cursor.fetchone()

    if result:
        # Table exists, fetch and display its content
        fetch_query = "SELECT u_artistname, u_trackname FROM user_playlist"  # Adjust column names if necessary
        cursor.execute(fetch_query)
        playlist_songs = cursor.fetchall()

        if playlist_songs:
            print("\nCreated Playlist:")
            for artist_name, track_name in playlist_songs:
                print(f"{artist_name} - {track_name}")  # Format: Artist Name - Track Name
        else:
            print("User Playlist is empty.")
    else:
        # Table does not exist
        print("User Playlist does not exist.")



def main():
    with sqlite3.connect('spotify.sqlite') as conn:
        while True:
            choice = input(
                "________________\nDo you want to create a playlist, search for a song, or load an existing playlist? \noptions:\n-playlist\n-search\n-load playlist\n-exit\n select: ").lower()
            if choice == 'search':
                more_artists = True
                offset = 0
                while more_artists:
                    show_artists(conn, offset=offset)
                    more_artists = input("Show more artists? (yes/no): ").lower() == 'yes'
                    if more_artists:
                        offset += 10
                artist = None
                while artist is None:
                    artist_input = input("_______\nChoose an artist (or press enter to skip): ")
                    if artist_input:  # User entered an artist name
                        if artist_exists(conn, artist_input):
                            artist = artist_input
                        else:
                            print("Artist not found. Please choose within given list")
                    else:  # User pressed enter to skip
                        break
                show_years(conn)
                year = input("______\nChoose a year (or press enter to skip): ")
                year = int(year) if year else None
                mood = None
                moods = ['danceability_per', 'valence_per', 'energy_per', 'acousticness_per', 'instrumental_per',
                         'liveness_per', 'speechiness_per']
                print("_________\nChoose a mood attribute from the following:")
                for m in moods:
                    print(m)
                while mood is None:
                    mood_input = input("__________\nEnter the mood attribute (or press enter to skip): ")
                    if mood_input:
                        if mood_input in moods:
                            mood = mood_input
                        else:
                            print("Invalid mood attribute selected. Please select from given options")
                    else:
                        break

                print("list of songs will now displayed")
                dropTable(conn)
                createTable(conn)
                create_playlist(conn, artist, year, mood)
                keep_going = input("Do you want to continue? (yes/no): ")
                if keep_going == 'no':
                    quit()
            elif choice == 'playlist':
                dropList(conn)
                createList(conn)
                addMore = True
                offset = 0
                more_song = True
                while more_song:
                    show_songs(conn, offset=offset)
                    more_song = input("Show more songs? (yes/no): ").lower() == 'yes'
                    if more_song:
                        offset += 10
                while addMore:
                    song = None
                    while song is None:
                        song_input = input("Choose an song you want in your playlist: ")
                        if song_input:  # User entered an song name
                            if song_exists(conn, song_input):
                                song = song_input
                            else:
                                print("Song not found. Please choose within given list")
                    insert_song(conn, song)
                    addMore = input("Would you like to add another song? (yes/no): ").lower() == 'yes'
                displayPlaylist(conn)
                keep_going = input("Do you want to continue? (yes/no): ")
                if keep_going == 'no':
                    quit()
            elif choice == 'load playlist':
                load_playlist(conn)
            elif choice == 'exit':
                break
            else:
                print("Please choose given options")

if __name__ == "__main__":
    main()