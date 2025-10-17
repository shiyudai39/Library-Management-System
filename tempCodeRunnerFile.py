# app.py
import tkinter as tk
from tkinter import ttk
from tab_books import BooksTab
from tab_users import UsersTab
from tab_transactions import TransactionsTab

class App(tk.Tk):
    def __init__(self, db_handler):
        super().__init__()
        self.db_handler = db_handler
        self.title("Library Management System")
        self.geometry("1200x800")
        self.configure(bg="#916060")

        self.setup_styles()
        
        header_frame = ttk.Frame(self, style='Header.TFrame')
        header_frame.pack(fill=tk.X)
        ttk.Label(header_frame, text="Library Management System", style='Header.TLabel').pack(pady=25)

        notebook = ttk.Notebook(self, style='TNotebook')
        notebook.pack(pady=10, padx=25, fill='both', expand=True)
        
        # Create instances of each tab
        self.books_tab = BooksTab(notebook, self.db_handler, self)
        self.users_tab = UsersTab(notebook, self.db_handler, self)
        self.transactions_tab = TransactionsTab(notebook, self.db_handler, self)
        
        notebook.add(self.books_tab, text='Manage Books')
        notebook.add(self.users_tab, text='Manage Users')
        notebook.add(self.transactions_tab, text='Issue / Return Books')

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        BG, FRAME_BG, TEXT, ACCENT, ACCENT_HOVER, BORDER, TREE_HEADER, ODD, EVEN = '#ffffff', '#f7f7f7', '#333333', '#009688', '#00796b', '#dcdcdc', '#e0e0e0', '#ffffff', '#f7f7f7'
        FONT = "Roboto"
        self.style.configure('.', background=BG, foreground=TEXT, font=(FONT, 11))
        self.style.configure('Header.TFrame', background=BG)
        self.style.configure('Header.TLabel', font=(FONT, 26, 'bold'), foreground=ACCENT, background=BG)
        self.style.configure('TFrame', background=BG)
        self.style.configure('TNotebook', background=BG, borderwidth=0)
        self.style.configure('TNotebook.Tab', font=(FONT, 12, 'bold'), padding=[20, 10], borderwidth=0, background=FRAME_BG)
        self.style.map('TNotebook.Tab', background=[('selected', ACCENT)], foreground=[('selected', 'white')])
        self.style.configure('TLabelFrame', bordercolor=BORDER, font=(FONT, 14, 'bold'), background=FRAME_BG)
        self.style.configure('TLabelFrame.Label', foreground=TEXT, background=FRAME_BG)
        self.style.configure('TEntry', fieldbackground=BG, bordercolor=BORDER, foreground=TEXT, insertwidth=1)
        self.style.configure('TButton', font=(FONT, 11, 'bold'), padding=10, background=ACCENT, foreground='white', borderwidth=0)
        self.style.map('TButton', background=[('active', ACCENT_HOVER)])
        self.style.configure('Treeview', rowheight=30, fieldbackground=BG)
        self.style.configure('Treeview.Heading', font=(FONT, 11, 'bold'), background=TREE_HEADER, foreground=TEXT, relief='flat')
        self.style.map('Treeview.Heading', relief=[('active','groove'),('pressed','sunken')])
        self.style.map('Treeview', background=[('selected', ACCENT)])
        self.style.configure("oddrow.Treeview", background=ODD)
        self.style.configure("evenrow.Treeview", background=EVEN)

    def refresh_all_tabs(self):
        """Refreshes the data in all tabs to ensure UI is up-to-date."""
        self.books_tab.refresh_books_list()
        self.users_tab.refresh_users_list()
        self.transactions_tab.refresh_transactions_tab()