# Library Management System (Tkinter + SQLite)

A desktop-based Library Management System built with Python, Tkinter, and SQLite.  
This application allows library administrators to manage books, users, and transactions (borrowing and returning books) through a simple and elegant graphical interface.

## Features

- Book Management
  - Add, edit, search, and delete books
  - Track book status (Available / Borrowed)
  - Import and export book data to CSV

- User Management
  - Add, search, and delete users
  - Manage user information
  - Import and export user data to CSV

- Transaction Management
  - Borrow and return books
  - Track which user has borrowed which book
  - View currently borrowed books

- Interface Highlights
  - Modern Tkinter UI with custom styles
  - Organized into tabs for easy navigation
  - Responsive layout and clear color scheme

## Project Structure

```
├── app.py              # Main application with Tkinter UI
├── database.py         # SQLite database handler
├── requirements.txt    # Python dependencies
├── tab_books.py        # Books management tab (not included in upload)
├── tab_users.py        # Users management tab (not included in upload)
├── tab_transactions.py # Transactions tab (not included in upload)
└── README.md           # Project documentation
```

## Installation

1. Clone the Repository
```
git clone https://github.com/yourusername/library-management-system.git
cd library-management-system
```

2. Install Dependencies
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the Application
```
python app.py
```

## Database

- Uses SQLite (no external database required)
- Database file: library_system.db
- Automatically created on first run

## Import / Export CSV

You can import and export data using the database methods:
- export_to_csv(table_name, filepath)
- import_from_csv(table_name, filepath)

Example:
```
db = LibraryDatabase()
db.export_to_csv('books', 'books_backup.csv')
db.import_from_csv('users', 'users_list.csv')
```

## Technologies Used

| Component | Technology |
|------------|-------------|
| GUI | Tkinter |
| Database | SQLite3 |
| Data Handling | Pandas |
| Language | Python 3.x |

## Future Improvements

- Add login and user roles
- Generate PDF reports
- Cloud-based database support
- Search and filter improvements

