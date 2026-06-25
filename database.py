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
            has_link INTEGER,
            thumbs_up INTEGER, thumbs_down INTEGER, angry INTEGER,
            face_hearts INTEGER, face_tear INTEGER, clown INTEGER, flame INTEGER
        )
        ''')
    connection.commit()
    connection.close()

def save_post(post_id, post_date, char_count, views, has_image, has_link, reactions):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO posts (
            post_id, date, char_count, views, has_image, has_link,
            thumbs_up, thumbs_down, angry, face_hearts, face_tear, clown, flame
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        post_id, post_date, char_count, views, has_image, has_link,
        reactions['👍'], reactions['👎'], reactions['🤬'],
        reactions['🥰'], reactions['😢'], reactions['🤡'], reactions['🔥']
    ))
    connection.commit()
    connection.close()
