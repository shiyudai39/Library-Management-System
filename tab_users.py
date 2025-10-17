# tab_users.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class UsersTab(ttk.Frame):
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

        ttk.Button(top_frame, text="Import from CSV", command=lambda: self.import_csv('users')).grid(row=0, column=0, sticky="nw")

        form = ttk.LabelFrame(top_frame, text="User Details", padding=20)
        form.grid(row=0, column=1, sticky="n")

        # --- WIDGET CHANGE: Made Entry fields wider and taller ---
        ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.name_entry = ttk.Entry(form, width=50, font=(main_app.FONT_FAMILY, 11))
        self.name_entry.grid(row=0, column=1, padx=10, pady=8, ipady=4)

        ttk.Label(form, text="Email:").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.email_entry = ttk.Entry(form, width=50, font=(main_app.FONT_FAMILY, 11))
        self.email_entry.grid(row=1, column=1, padx=10, pady=8, ipady=4)
        
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=2, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Add User", command=self.add_user).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Delete User", command=self.delete_user).pack(side=tk.LEFT, padx=10)

        ttk.Button(top_frame, text="Export to CSV", command=lambda: self.export_csv('users')).grid(row=0, column=2, sticky="ne")
        
        tree_frame = ttk.LabelFrame(self, text="All Users", padding=15)
        tree_frame.grid(row=1, column=0, sticky="nsew", pady=10, padx=20)
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        cols = ('ID', 'Name', 'Email')
        self.tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=5)
        for col in cols: self.tree.heading(col, text=col)
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        self.refresh_users_list()

    def refresh_users_list(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for i, user in enumerate(self.db_handler.get_all_users()):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=user, tags=(tag,))

    def add_user(self):
        if self.db_handler.add_user(self.name_entry.get(), self.email_entry.get()):
            messagebox.showinfo("Success", "User added successfully."); self.main_app.refresh_all_tabs()
        else: messagebox.showerror("Error", "A user with this email already exists.")

    def delete_user(self):
        if not self.tree.selection(): messagebox.showerror("Error", "Please select a user to delete."); return
        if messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?"):
            user_id = self.tree.item(self.tree.selection()[0])['values'][0]
            self.db_handler.delete_user(user_id)
            messagebox.showinfo("Success", "User deleted successfully.")
            self.main_app.refresh_all_tabs()
    
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