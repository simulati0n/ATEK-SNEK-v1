import sqlite3


class Database:
    def __init__(self, db_name="snake_game.db"):
       #initialize the database connection
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        #create tables for the database
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def add_score(self, player_name, score):
        #add a new score to the high_scores table
        self.cursor.execute("""
            INSERT INTO high_scores (player_name, score)
            VALUES (?, ?)
        """, (player_name, score))
        self.connection.commit()

    def get_high_scores(self, limit=10):
        #retrieve the top high scores
        self.cursor.execute("""
            SELECT player_name, score
            FROM high_scores
            ORDER BY score DESC
            LIMIT ?
        """, (limit,))
        return self.cursor.fetchall()

    def close(self):
        #close the database connection
        self.connection.close()
