import tkinter as tk

from tkinter import ttk, messagebox

from datetime import datetime

import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class ExpenseTrackerApp:

    def __init__(self, root):

        self.root = root

        self.root.title("💸 Personal Expense Tracker - FuzzuTech")

        self.root.geometry("600x450")

        self.root.config(bg="#121212")



        self.expenses = []  # List to store expenses as tuples (date, category, amount)



        title = tk.Label(root, text="Personal Expense Tracker", font=("Arial", 20, "bold"), fg="#00ff99", bg="#121212")

        title.pack(pady=10)



        form_frame = tk.Frame(root, bg="#121212")

        form_frame.pack(pady=10)



        tk.Label(form_frame, text="Date (YYYY-MM-DD):", fg="white", bg="#121212", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        tk.Label(form_frame, text="Category:", fg="white", bg="#121212", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        tk.Label(form_frame, text="Amount (₹):", fg="white", bg="#121212", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")



        self.date_var = tk.StringVar()

        self.category_var = tk.StringVar()

        self.amount_var = tk.StringVar()



        self.date_entry = tk.Entry(form_frame, textvariable=self.date_var, font=("Arial", 12), width=20)

        self.date_entry.grid(row=0, column=1, pady=5)

        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))



        categories = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Other']

        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, values=categories, state="readonly", font=("Arial", 12), width=18)

        self.category_combo.grid(row=1, column=1, pady=5)

        self.category_combo.current(0)



        self.amount_entry = tk.Entry(form_frame, textvariable=self.amount_var, font=("Arial", 12), width=20)

        self.amount_entry.grid(row=2, column=1, pady=5)



        add_btn = tk.Button(root, text="Add Expense", font=("Arial", 14, "bold"), bg="#00ff99", fg="#000", command=self.add_expense)

        add_btn.pack(pady=10)



        self.expense_listbox = tk.Listbox(root, font=("Arial", 12), width=60, height=8)

        self.expense_listbox.pack(pady=10)



        plot_btn = tk.Button(root, text="Show Monthly Summary", font=("Arial", 14, "bold"), bg="#00ff99", fg="#000", command=self.show_summary)

        plot_btn.pack(pady=5)



    def add_expense(self):

        date_str = self.date_var.get()

        category = self.category_var.get()

        amount_str = self.amount_var.get()



        try:

            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            amount = float(amount_str)

            if amount <= 0:

                raise ValueError("Amount must be positive")

        except Exception as e:

            messagebox.showerror("Invalid Input", f"Error: {e}")

            return



        self.expenses.append((date_obj, category, amount))

        self.expense_listbox.insert(tk.END, f"{date_obj.date()} | {category} | ₹{amount:.2f}")



        # Clear amount field only (date and category remain)

        self.amount_var.set("")



    def show_summary(self):

        if not self.expenses:

            messagebox.showinfo("No Data", "Add some expenses first!")

            return



        # Aggregate monthly expenses by category

        summary = {}

        for date_obj, category, amount in self.expenses:

            month = date_obj.strftime("%Y-%m")

            key = (month, category)

            summary[key] = summary.get(key, 0) + amount



        # Prepare data for plotting current month

        current_month = datetime.now().strftime("%Y-%m")

        categories = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Other']

        amounts = [summary.get((current_month, cat), 0) for cat in categories]



        # Plotting in a new Tkinter window

        plot_win = tk.Toplevel(self.root)

        plot_win.title("Monthly Expense Summary")

        plot_win.geometry("600x400")



        fig, ax = plt.subplots(figsize=(6,4))

        ax.bar(categories, amounts, color="#00ff99")

        ax.set_title(f"Expenses for {current_month}", fontsize=14, fontweight="bold")

        ax.set_ylabel("Amount (₹)")

        ax.set_xlabel("Category")

        ax.grid(axis='y', linestyle='--', alpha=0.7)



        canvas = FigureCanvasTkAgg(fig, master=plot_win)

        canvas.draw()

        canvas.get_tk_widget().pack()



if __name__ == "__main__":

    root = tk.Tk()

    app = ExpenseTrackerApp(root)

    root.mainloop()