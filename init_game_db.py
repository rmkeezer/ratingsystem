import sqlite3

def init_game_db(out_db):
    print("STARTING GAME SEARCH, PLEASE WAIT")
    out_c = out_db.cursor()
    out_c.execute('''CREATE TABLE IF NOT EXISTS games
        (game_id INT PRIMARY KEY,
        name TEXT,
        type TEXT,
        required_age INT,
        num_dlc INT,
        detailed_description TEXT,
        about_the_game TEXT,
        supported_languages TEXT,
        header_image TEXT,
        website TEXT,
        min_req TEXT,
        rec_req TEXT,
        developers TEXT,
        publishers TEXT,
        demo_id INT,
        platflorms TEXT,
        metacritic INT,
        metaurl TEXT,
        release_date TEXT)''')
    out_c.execute('''CREATE TABLE IF NOT EXISTS categories
        (game_id INT,
        id INT,
        description TEXT,
        PRIMARY KEY(game_id, id))''')
    out_c.execute('''CREATE TABLE IF NOT EXISTS genres
        (game_id INT,
        id INT,
        description TEXT,
        PRIMARY KEY(game_id, id))''')
    out_c.execute('''CREATE TABLE IF NOT EXISTS screenshots
        (game_id INT,
        id INT,
        path_thumbnail TEXT,
        path_full TEXT,
        PRIMARY KEY(game_id, id))''')
    out_c.execute('''CREATE TABLE IF NOT EXISTS movies
        (game_id INT,
        id INT,
        name TEXT,
        thumbnail TEXT,
        webm480 TEXT,
        webm TEXT,
        PRIMARY KEY(game_id, id))''')
    out_db.commit()