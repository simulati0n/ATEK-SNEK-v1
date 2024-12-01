import sqlite3


class Database:
    def __init__(self, db_name="snake_game.db"):
       #initialize the database connection
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        #create tables for the database
        self.cursor.execute(
   CREATE TABLE games (
    id INT PRIMARY KEY AUTO_INCREMENT,
    start_time DATETIME,
    end_time DATETIME,
    score INT,
    level INT,
    game_over_reason VARCHAR(255)
);

CREATE TABLE snake_segments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    game_id INT,
    x_position INT,
    y_position INT,
    segment_number INT,
    FOREIGN KEY (game_id) REFERENCES games(id)
);

CREATE TABLE food (
    id INT PRIMARY KEY AUTO_INCREMENT,
    game_id INT,
    x_position INT,
    y_position INT,
    FOREIGN KEY (game_id) REFERENCES games(id)
);
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
