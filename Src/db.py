import sqlite3       


def main():
    db = None
    try:
        # Open DB
        db = sqlite3.connect("sqlite.db")
        
        # Set db cursor
        cur = db.cursor()
        
        # Execute db query cmd
        table = """CREATE TABLE IF NOT EXISTS METADATA (
            title VARCHAR(100),
            duration INTEGER, 
            url VARCHAR(100), 
            sound_url VARCHAR(255),
            PRIMARY KEY (title)
        );"""
        
        cur.execute(table)
        db.commit()
        
        # SAMPLE DATA
        name = "Video from YT"
        url = "yt.c/123"
        dur = 40
        s_url = "s.yt.c/l=123"
        
        # INSERT DATA
        dat = """
            INSERT INTO METADATA (title, duration, url, sound_url)
            VALUES (?, ?, ?, ?)
            """
        
        cur.execute(dat, (name, dur, url, s_url))
        db.commit()
        
        cur.execute("SELECT * FROM METADATA")
        result = cur.fetchall()
        for row in result:
            print(row)
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if db:
            db.close()
