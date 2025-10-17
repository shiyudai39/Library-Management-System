# tab_transactions.py
import tkinter as tk
from tkinter import ttk, messagebox

class TransactionsTab(ttk.Frame):
    def __init__(self, parent, db_handler, main_app):
        super().__init__(parent)
        self.db_handler = db_handler
        self.main_app = main_app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        center_frame = ttk.Frame(self); center_frame.grid(row=0, column=0, pady=10)
        issue_frame = ttk.LabelFrame(center_frame, text="Issue a Book", padding=20)
        issue_frame.pack(pady=10, padx=20, ipadx=20, ipady=20)
        
        # --- WIDGET CHANGE: Made Comboboxes wider ---
        ttk.Label(issue_frame, text="Select Book:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.book_combo = ttk.Combobox(issue_frame, width=50, font=(main_app.FONT_FAMILY, 11))
        self.book_combo.grid(row=0, column=1, padx=10, pady=8)
        
        ttk.Label(issue_frame, text="Select User:").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.user_combo = ttk.Combobox(issue_frame, width=50, font=(main_app.FONT_FAMILY, 11))
        self.user_combo.grid(row=1, column=1, padx=10, pady=8)
        
        ttk.Button(issue_frame, text="Issue Book", command=self.issue_book).grid(row=2, columnspan=2, pady=20)
        
        return_frame = ttk.LabelFrame(self, text="Borrowed Books", padding=15)
        return_frame.grid(row=1, column=0, sticky="nsew", pady=10, padx=20)
        return_frame.grid_columnconfigure(0, weight=1)
        return_frame.grid_rowconfigure(0, weight=1)

        cols = ('Trans. ID', 'Book Title', 'User Name', 'Borrow Date', 'Book ID'); self.tree = ttk.Treeview(return_frame, columns=cols, show='headings', height=5)
        for col in cols: self.tree.heading(col, text=col)
        self.tree.column('Book ID', width=0, stretch=tk.NO)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        ttk.Button(return_frame, text="Return Selected Book", command=self.return_book, width=20).grid(row=0, column=1, padx=15)
        
        self.refresh_transactions_tab()

    def refresh_transactions_tab(self):
        available_books = self.db_handler.get_available_books()
        self.book_combo['values'] = [f"{b[0]} - {b[1]}" for b in available_books]
        all_users = self.db_handler.get_all_users()
        self.user_combo['values'] = [f"{u[0]} - {u[1]}" for u in all_users]
        
        for i in self.tree.get_children(): self.tree.delete(i)
        for i, item in enumerate(self.db_handler.get_borrowed_books_details()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=item, tags=(tag,))

    def issue_book(self):
        book_info = self.book_combo.get(); user_info = self.user_combo.get()
        if not book_info or not user_info: messagebox.showerror("Error", "Please select both a book and a user."); return
        book_id = int(book_info.split(' - ')[0]); user_id = int(user_info.split(' - ')[0])
        self.db_handler.borrow_book(book_id, user_id)
        messagebox.showinfo("Success", "Book issued successfully.")
        self.main_app.refresh_all_tabs()

    def return_book(self):
        if not self.tree.selection(): messagebox.showerror("Error", "Please select a borrowed book to return."); return
        item = self.tree.item(self.tree.selection()[0])['values']
        trans_id, book_id = item[0], item[4]
        self.db_handler.return_book(trans_id, book_id)
        messagebox.showinfo("Success", "Book returned successfully.")
        self.main_app.refresh_all_tabs()