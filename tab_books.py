# tab_books.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class BooksTab(ttk.Frame):
    def __init__(self, parent, db_handler, main_app):
        super().__init__(parent)
        self.db_handler = db_handler
        self.main_app = main_app

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        top_frame = ttk.Frame(self)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(10, 20), padx=20)
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=0)
        top_frame.grid_columnconfigure(2, weight=1)

        ttk.Button(top_frame, text="Import from CSV", command=lambda: self.import_csv('books')).grid(row=0, column=0, sticky="nw")

        form = ttk.LabelFrame(top_frame, text="Book Details", padding=20)
        form.grid(row=0, column=1, sticky="n")
        
        # --- WIDGET CHANGE: Made Entry fields wider and taller ---
        ttk.Label(form, text="Title:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.title_entry = ttk.Entry(form, width=50, font=(main_app.FONT_FAMILY, 11))
        self.title_entry.grid(row=0, column=1, padx=10, pady=8, ipady=4)
        
        ttk.Label(form, text="Author:").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.author_entry = ttk.Entry(form, width=50, font=(main_app.FONT_FAMILY, 11))
        self.author_entry.grid(row=1, column=1, padx=10, pady=8, ipady=4)
        
        ttk.Label(form, text="ISBN:").grid(row=2, column=0, sticky="w", padx=10, pady=8)
        self.isbn_entry = ttk.Entry(form, width=50, font=(main_app.FONT_FAMILY, 11))
        self.isbn_entry.grid(row=2, column=1, padx=10, pady=8, ipady=4)
        
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=3, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Add Book", command=self.add_book).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Update Book", command=self.update_book).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Delete Book", command=self.delete_book).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(top_frame, text="Export to CSV", command=lambda: self.export_csv('books')).grid(row=0, column=2, sticky="ne")
        
        tree_frame = ttk.LabelFrame(self, text="All Books", padding=15)
        tree_frame.grid(row=1, column=0, sticky="nsew", pady=10, padx=20)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        
        cols = ('ID', 'Title', 'Author', 'ISBN', 'Status')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=5)
        self.tree.column('ID', width=50, anchor='center'); self.tree.column('Title', width=300); self.tree.column('Author', width=200); self.tree.column('ISBN', width=150, anchor='center'); self.tree.column('Status', width=100, anchor='center')
        for col in cols: self.tree.heading(col, text=col)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind('<<TreeviewSelect>>', self.on_item_select)
        
        self.refresh_books_list()

    def refresh_books_list(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for i, book in enumerate(self.db_handler.get_all_books()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=book, tags=(tag,))

    def add_book(self):
        if self.db_handler.add_book(self.title_entry.get(), self.author_entry.get(), self.isbn_entry.get()):
            messagebox.showinfo("Success", "Book added successfully."); self.main_app.refresh_all_tabs()
        else: messagebox.showerror("Error", "A book with this ISBN already exists.")

    def update_book(self):
        if not self.tree.selection(): messagebox.showerror("Error", "Please select a book to update."); return
        book_id = self.tree.item(self.tree.selection()[0])['values'][0]
        self.db_handler.update_book(book_id, self.title_entry.get(), self.author_entry.get(), self.isbn_entry.get())
        messagebox.showinfo("Success", "Book updated successfully."); self.main_app.refresh_all_tabs()
        
    def delete_book(self):
        if not self.tree.selection(): messagebox.showerror("Error", "Please select a book to delete."); return
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this book?"):
            book_id = self.tree.item(self.tree.selection()[0])['values'][0]
            self.db_handler.delete_book(book_id)
            messagebox.showinfo("Success", "Book deleted successfully.")
            self.main_app.refresh_all_tabs()

    def on_item_select(self, event):
        if not self.tree.selection(): return
        item = self.tree.item(self.tree.selection()[0])['values']
        self.title_entry.delete(0, tk.END); self.title_entry.insert(0, item[1])
        self.author_entry.delete(0, tk.END); self.author_entry.insert(0, item[2])
        self.isbn_entry.delete(0, tk.END); self.isbn_entry.insert(0, item[3])

    def import_csv(self, table_name):
        filepath = filedialog.askopenfilename(title=f"Select CSV", filetypes=[("CSV files", "*.csv")])
        if not filepath: return
        rows = self.db_handler.import_from_csv(table_name, filepath)
        messagebox.showinfo("Import Complete", f"Successfully added {rows} new records."); self.main_app.refresh_all_tabs()

    def export_csv(self, table_name):
        filepath = filedialog.asksaveasfilename(title=f"Save as CSV", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not filepath: return
        if self.db_handler.export_to_csv(table_name, filepath): messagebox.showinfo("Export Complete", "Data exported successfully.")
        else: messagebox.showerror("Export Error", "An error occurred.")