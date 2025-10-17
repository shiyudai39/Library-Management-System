# database.py
import sqlite3
import pandas as pd
from datetime import date

class LibraryDatabase:
    def __init__(self, db_name="library_system.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.init_database()

    def init_database(self):
        # Book Table with Status
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                status TEXT NOT NULL DEFAULT 'Available'
            )
        ''')
        # User Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        # Transactions Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                user_id INTEGER,
                borrow_date TEXT,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        self.conn.commit()

    # --- Book Management ---
    def add_book(self, title, author, isbn):
        try:
            self.cursor.execute("INSERT INTO books (title, author, isbn, status) VALUES (?, ?, ?, 'Available')",
                               (title, author, isbn))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_all_books(self):
        self.cursor.execute("SELECT id, title, author, isbn, status FROM books")
        return self.cursor.fetchall()

    def update_book(self, book_id, title, author, isbn):
        self.cursor.execute("UPDATE books SET title = ?, author = ?, isbn = ? WHERE id = ?",
                       (title, author, isbn, book_id))
        self.conn.commit()

    def delete_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()

    def search_books(self, query):
        self.cursor.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?",
                       (f'%{query}%', f'%{query}%', f'%{query}%'))
        return self.cursor.fetchall()

    def get_available_books(self):
        self.cursor.execute("SELECT id, title, author FROM books WHERE status = 'Available'")
        return self.cursor.fetchall()

    # --- User Management ---
    def add_user(self, name, email):
        try:
            self.cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError:
            return None

    def get_all_users(self):
        self.cursor.execute("SELECT id, name, email FROM users")
        return self.cursor.fetchall()

    def search_users(self, query):
        self.cursor.execute("SELECT * FROM users WHERE name LIKE ? OR email LIKE ?", (f'%{query}%', f'%{query}%'))
        return self.cursor.fetchall()
        
    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()

    # --- Transaction Management ---
    def borrow_book(self, book_id, user_id):
        today = date.today().isoformat()
        # Record the transaction
        self.cursor.execute("INSERT INTO transactions (book_id, user_id, borrow_date) VALUES (?, ?, ?)",
                           (book_id, user_id, today))
        # Update book status
        self.cursor.execute("UPDATE books SET status = 'Borrowed' WHERE id = ?", (book_id,))
        self.conn.commit()

    def return_book(self, transaction_id, book_id):
        today = date.today().isoformat()
        # Update transaction with return date
        self.cursor.execute("UPDATE transactions SET return_date = ? WHERE id = ?", (today, transaction_id))
        # Update book status to Available
        self.cursor.execute("UPDATE books SET status = 'Available' WHERE id = ?", (book_id,))
        self.conn.commit()

    def get_borrowed_books_details(self):
        self.cursor.execute('''
            SELECT t.id, b.title, u.name, t.borrow_date, b.id
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            JOIN users u ON t.user_id = u.id
            WHERE t.return_date IS NULL
        ''')
        return self.cursor.fetchall()

    # --- Pandas Integration ---
    def export_to_csv(self, table_name, filepath):
        if table_name not in ['books', 'users']: return False
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", self.conn)
            df.to_csv(filepath, index=False)
            return True
        except Exception:
            return False

    def import_from_csv(self, table_name, filepath):
        if table_name not in ['books', 'users']: return 0
        try:
            df = pd.read_csv(filepath)
            # Ensure columns match for safety
            if table_name == 'books':
                df = df[['title', 'author', 'isbn']] # Select only relevant columns
            else: # users
                df = df[['name', 'email']]
            
            rows_added = 0
            for index, row in df.iterrows():
                if table_name == 'books':
                    if self.add_book(row['title'], row['author'], row['isbn']):
                        rows_added += 1
                else:
                    if self.add_user(row['name'], row['email']):
                        rows_added += 1
            return rows_added
        except Exception:
            return 0

    def __del__(self):
        self.conn.close()