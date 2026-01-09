import sqlite3
from datetime import datetime

class LibraryBackend:
    def __init__(self, db_name="library.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Books Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                title TEXT NOT NULL,
                                author TEXT NOT NULL,
                                isbn TEXT UNIQUE NOT NULL,
                                category TEXT,
                                quantity INTEGER DEFAULT 1,
                                available INTEGER DEFAULT 1
                            )''')
            # Members Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                email TEXT UNIQUE NOT NULL,
                                joined_date TEXT
                            )''')
            # Transactions Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                book_id INTEGER,
                                member_id INTEGER,
                                issue_date TEXT,
                                return_date TEXT,
                                status TEXT DEFAULT 'Issued',
                                FOREIGN KEY(book_id) REFERENCES books(id),
                                FOREIGN KEY(member_id) REFERENCES members(id)
                            )''')
            conn.commit()

    # Book Operations
    def add_book(self, title, author, isbn, category, quantity):
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("INSERT INTO books (title, author, isbn, category, quantity, available) VALUES (?, ?, ?, ?, ?, ?)",
                             (title, author, isbn, category, quantity, quantity))
                return True, "Book added successfully!"
        except sqlite3.IntegrityError:
            return False, "ISBN already exists."

    def get_books(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute("SELECT * FROM books")
            return cursor.fetchall()

    def search_books(self, query):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ?", 
                                 (f'%{query}%', f'%{query}%'))
            return cursor.fetchall()

    # Member Operations
    def add_member(self, name, email):
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute("INSERT INTO members (name, email, joined_date) VALUES (?, ?, ?)",
                             (name, email, datetime.now().strftime("%Y-%m-%d")))
                return True, "Member added successfully!"
        except sqlite3.IntegrityError:
            return False, "Email already registered."

    def get_members(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute("SELECT * FROM members")
            return cursor.fetchall()

    # Transaction Operations
    def issue_book(self, book_id, member_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Check availability
            cursor.execute("SELECT available FROM books WHERE id = ?", (book_id,))
            res = cursor.fetchone()
            if not res or res[0] <= 0:
                return False, "Book not available."
            
            # Issue
            cursor.execute("INSERT INTO transactions (book_id, member_id, issue_date) VALUES (?, ?, ?)",
                           (book_id, member_id, datetime.now().strftime("%Y-%m-%d")))
            cursor.execute("UPDATE books SET available = available - 1 WHERE id = ?", (book_id,))
            conn.commit()
            return True, "Book issued successfully!"

    def return_book(self, transaction_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT book_id, status FROM transactions WHERE id = ?", (transaction_id,))
            res = cursor.fetchone()
            if not res or res[1] == 'Returned':
                return False, "Invalid transaction or already returned."
            
            book_id = res[0]
            cursor.execute("UPDATE transactions SET return_date = ?, status = 'Returned' WHERE id = ?",
                           (datetime.now().strftime("%Y-%m-%d"), transaction_id))
            cursor.execute("UPDATE books SET available = available + 1 WHERE id = ?", (book_id,))
            conn.commit()
            return True, "Book returned successfully!"

    def get_transactions(self):
        with sqlite3.connect(self.db_name) as conn:
            query = '''SELECT t.id, b.title, m.name, t.issue_date, t.return_date, t.status 
                       FROM transactions t
                       JOIN books b ON t.book_id = b.id
                       JOIN members m ON t.member_id = m.id'''
            cursor = conn.execute(query)
            return cursor.fetchall()
