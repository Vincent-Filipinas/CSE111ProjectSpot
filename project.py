import sqlite3
from sqlite3 import Error
import pandas as pd


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
    print("Create table")
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
                p_released_day decimal(2,0) not null
            )
        ''')
        _conn.commit()
        print("Table created successfully.")
    except Error as e:
        print(e)


def dropTable(_conn):
    print("Drop tables")
    try:
        cursor = _conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS new_playlist')
        _conn.commit()
        print("Table dropped successfully.")
    except Error as e:
        print(e) 

def search_song(conn):
    song_name = input("Enter a song name to search for: ")
    query = "SELECT s_trackname, a_name FROM song JOIN artist ON song.s_artistkey = artist.a_artistkey WHERE s_trackname LIKE ?"
    cursor = conn.cursor()
    cursor.execute(query, ('%' + song_name + '%',))
    results = cursor.fetchall()

    if results:
        print("\nSearch Results:")
        for track_name, artist_name in results:
            print(f"{track_name} by {artist_name}")
    else:
        print("No songs found matching your search.")

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
    query = "SELECT COUNT(*) FROM artist WHERE a_name = ?"
    cursor = conn.cursor()
    cursor.execute(query, (artist_name,))
    return cursor.fetchone()[0] > 0


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


def create_playlist(conn, artist=None, year=None):
    # Building the query to fetch and insert songs based on artist and year
    select_query = "SELECT a_name, a_artistkey, s_songkey, s_trackname, s_released_year, s_released_month, s_released_day FROM artist JOIN song ON artist.a_artistkey = song.s_artistkey"
    conditions = []
    if artist:
        conditions.append(f"artist.a_name = '{artist}'")
    if year:
        conditions.append(f"song.s_released_year = {year}")

    if conditions:
        select_query += " WHERE " + " AND ".join(conditions)

    cursor = conn.cursor()
    cursor.execute(select_query)
    songs = cursor.fetchall()

    # Inserting songs into new_playlist
    for song in songs:
        insert_query = """
        INSERT INTO new_playlist (p_artistname, p_artistkey, p_songkey, p_trackname, p_released_year, p_released_month, p_released_day)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(insert_query, song)
    
    conn.commit()

    # Query to retrieve and display songs from new_playlist
    display_query = "SELECT p_artistname, p_trackname, p_released_year,p_released_month,p_released_day FROM new_playlist"
    cursor.execute(display_query)
    playlist_songs = cursor.fetchall()

    print("\nCreated Playlist:")
    for artist_name, track_name, year, month, day in playlist_songs:
        print(f"{artist_name} - {track_name} {year}-{month}-{day}")




def main():
    with sqlite3.connect('tpch.sqlite') as conn:
        while True:
            choice = input("Do you want to create a playlist or search for a song? (playlist/search/exit): ").lower()
            if choice == 'playlist':
                more_artists = True
                offset = 0
                while more_artists:
                    show_artists(conn, offset=offset)
                    more_artists = input("Show more artists? (yes/no): ").lower() == 'yes'
                    if more_artists:
                        offset += 10
                artist = None
                while artist is None:
                    artist_input = input("Choose an artist (or press enter to skip): ")
                    if artist_input:  # User entered an artist name
                        if artist_exists(conn, artist_input):
                            artist = artist_input
                        else:
                            print("Artist not found. Please choose within given list")
                    else:  # User pressed enter to skip
                        break
                show_years(conn)
                year = input("Choose a year (or press enter to skip): ")
                year = int(year) if year else None
                print("playlist will now be created and displayed")
                dropTable(conn)
                createTable(conn)
                create_playlist(conn, artist, year)
                keep_going = input("Do you want to continue? (yes/no): ")
                if keep_going == 'no':
                    break
            elif choice == 'search':
                search_input = input('Search song by name (1) or by mood (2) (enter 1 or 2): ')
                if search_input == '1':
                    search_song(conn)
                elif search_input == '2':
                    search_song_by_stats(conn)

            elif choice == 'exit':
                break
            else:
                print("Please choose given options")

if __name__ == "__main__":
    main()