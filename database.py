import sqlite3

db_name = 'studrada_stats.db'

def init_db():
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY,
            date TEXT,
            char_count INTEGER,
            views INTEGER,
            has_image INTEGER,
            has_link INTEGER
        )
        ''')
    
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS reactions (
                   post_id INTEGER,
                   emoji TEXT,
                   count INTEGER,
                   PRIMARY KEY (post_id, emoji),
                   FOREIGN KEY (post_id) REFERENCES posts (post_id)
                )
                ''')
    connection.commit()
    connection.close()

def save_post(post_id, post_date, char_count, views, has_image, has_link, reactions_dict):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO posts (
            post_id, date, char_count, views, has_image, has_link
        ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
        post_id, post_date, char_count, views, has_image, has_link
    ))

    cursor.execute('DELETE FROM reactions WHERE post_id = ?', (post_id,))

    for emoji, count in reactions_dict.items():
        cursor.execute('''
                INSERT INTO reactions (post_id, emoji, count) 
                VALUES (?, ?, ?)
            ''', (post_id, emoji, count))
        
    connection.commit()
    connection.close()
