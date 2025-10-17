# main.py
from database import LibraryDatabase
from app import App

def main():
    db_handler = LibraryDatabase()
    app = App(db_handler)
    app.mainloop()

if __name__ == "__main__":
    main()