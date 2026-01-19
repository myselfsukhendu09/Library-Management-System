
import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, stock INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER, type TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute("SELECT count(*) FROM books")
    if c.fetchone()[0] == 0:
        books = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', 5),
            ('1984', 'George Orwell', 3),
            ('To Kill a Mockingbird', 'Harper Lee', 4),
            ('The Hobbit', 'J.R.R. Tolkien', 7)
        ]
        c.executemany("INSERT INTO books (title, author, stock) VALUES (?, ?, ?)", books)
    conn.commit()
    conn.close()

def get_catalog():
    conn = sqlite3.connect('library.db')
    df = pd.read_sql_query("SELECT * FROM books", conn)
    conn.close()
    return df

def get_stats():
    conn = sqlite3.connect('library.db')
    books_count = pd.read_sql_query("SELECT SUM(stock) as total FROM books", conn).iloc[0]['total']
    titles_count = pd.read_sql_query("SELECT COUNT(*) as total FROM books", conn).iloc[0]['total']
    conn.close()
    return books_count, titles_count
