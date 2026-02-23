import tkinter as tk
from tkinter import messagebox
from database import register_user, login_user, add_movie, create_tables
from booking import list_movies, book_movie

current_user = None

def launch_app():
    root = tk.Tk()
    root.title("Movie Booking App")
    root.geometry("400x400")

    create_tables()
    login_screen(root)

    root.mainloop()

# --- Login / Register Screen ---
def login_screen(root):
    global current_user
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def login():
        global current_user
        user = login_user(username_entry.get(), password_entry.get())
        if user:
            current_user = user[0]
            main_screen(root)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register():
        success = register_user(username_entry.get(), password_entry.get())
        if success:
            messagebox.showinfo("Success", "Registered successfully")
        else:
            messagebox.showerror("Error", "Username already exists")

    tk.Button(root, text="Login", command=login).pack(pady=5)
    tk.Button(root, text="Register", command=register).pack(pady=5)

# --- Main Movie Booking Screen ---
def main_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Available Movies").pack()

    movies = list_movies()

    if not movies:
        add_movie("Interstellar", 5)
        add_movie("Inception", 3)
        add_movie("The Matrix", 4)
        movies = list_movies()

    for movie in movies:
        movie_id, title, seats = movie
        btn = tk.Button(root, text=f"{title} ({seats} seats)",
                        command=lambda m_id=movie_id: book(m_id))
        btn.pack(pady=2)

    tk.Button(root, text="Logout", command=lambda: login_screen(root)).pack(pady=10)

# --- Booking function ---
def book(movie_id):
    global current_user
    if book_movie(current_user, movie_id):
        messagebox.showinfo("Success", "Seat booked!")
    else:
        messagebox.showerror("Error", "No seats available")