import sqlite3

conn = sqlite3.connect("scores.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS scores (
    name TEXT,
    score INTEGER,
    level INTEGER
    )
""")

def update_db(score, level=1):
    def view_score():
        print("(name, lvl, score)")
        for item in c.fetchall():
            print(item[1:])
        
    name = str(input("Please enter your name: "))
    run_scores = (name, level, score)
    c.execute("INSERT INTO scores (name, score, level) VALUES (?,?,?)", run_scores)

    c.execute("SELECT score, * FROM scores ORDER BY score")

    conn.commit()
    view_score()
    
    conn.close()