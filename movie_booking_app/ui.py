import tkinter as tk
from tkinter import messagebox
from database import create_tables, get_user_booked_movie_ids, get_user_bookings, login_user, register_user
from booking import book_movie, list_movies, search_movies

current_user = None


def launch_app():
    root = tk.Tk()
    root.title("Movie Booking App")
    root.geometry("700x550")
    root.configure(bg="#f0f8ff")

    create_tables()
    login_screen(root)

    root.mainloop()


def clear_root(root):
    for widget in root.winfo_children():
        widget.destroy()


def main_screen(root):
    clear_root(root)
    root.configure(bg="#f0f8ff")

    user_id, username = current_user

    top = tk.Frame(root, bg="#f0f8ff")
    top.pack(fill="x", pady=10, padx=10)

    tk.Label(top, text=f"Welcome, {username}", font=("Arial", 15, "bold"), bg="#f0f8ff").pack(side="left")
    tk.Button(top, text="Logout", font=("Arial", 11), bg="#f44336", fg="white", command=lambda: login_screen(root)).pack(side="right")

    search_frame = tk.Frame(root, bg="#f0f8ff")
    search_frame.pack(fill="x", padx=10, pady=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
    search_entry.pack(side="left", padx=5)

    movie_frame = tk.Frame(root, bg="#f0f8ff")
    movie_frame.pack(fill="both", expand=True, padx=10, pady=5)

    booking_frame = tk.Frame(root, bg="#f0f8ff")
    booking_frame.pack(fill="x", padx=10, pady=10)

    booking_label = tk.Label(booking_frame, text="", font=("Arial", 11), bg="#f0f8ff", justify="left")
    booking_label.pack(anchor="w")

    def refresh_bookings():
        bookings = get_user_bookings(user_id)
        if bookings:
            booking_label.config(text="Your bookings: " + ", ".join(bookings[:8]))
        else:
            booking_label.config(text="Your bookings: none")

    def render_movies(movies):
        for widget in movie_frame.winfo_children():
            widget.destroy()

        booked_movie_ids = get_user_booked_movie_ids(user_id)

        tk.Label(movie_frame, text="Available Movies", font=("Arial", 16), bg="#f0f8ff").pack(pady=5)
        if not movies:
            tk.Label(movie_frame, text="No movies found.", font=("Arial", 12), bg="#f0f8ff").pack(pady=15)
            return

        for movie_id, title, seats in movies:
            row = tk.Frame(movie_frame, bg="#f0f8ff")
            row.pack(fill="x", pady=4)

            tk.Label(row, text=f"{title} ({seats} seats)", font=("Arial", 12), bg="#f0f8ff", anchor="w").pack(side="left")
            is_booked = movie_id in booked_movie_ids
            tk.Button(
                row,
                text="Booked" if is_booked else "Book",
                font=("Arial", 10),
                bg="#4caf50" if is_booked else "#ff9800",
                fg="white",
                command=lambda m_id=movie_id: book(root, m_id),
            ).pack(side="right")

    def search_action():
        keyword = search_entry.get().strip()
        if not keyword:
            render_movies(list_movies())
            return
        render_movies(search_movies(keyword))

    tk.Button(search_frame, text="Search", font=("Arial", 11), command=search_action, bg="#3f51b5", fg="white").pack(side="left", padx=5)
    tk.Button(search_frame, text="Show All", font=("Arial", 11), command=lambda: render_movies(list_movies()), bg="#607d8b", fg="white").pack(side="left")

    render_movies(list_movies())
    refresh_bookings()


def login_screen(root):
    global current_user
    current_user = None
    clear_root(root)

    root.configure(bg="#f0f8ff")

    frame = tk.Frame(root, bg="#f0f8ff")
    frame.pack(expand=True)

    tk.Label(frame, text="Movie Booking Login", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=15)
    tk.Label(frame, text="Username", font=("Arial", 14), bg="#f0f8ff").pack(pady=6)
    username_entry = tk.Entry(frame, font=("Arial", 14), width=25)
    username_entry.pack(pady=4)

    tk.Label(frame, text="Password", font=("Arial", 14), bg="#f0f8ff").pack(pady=6)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 14), width=25)
    password_entry.pack(pady=4)

    def login():
        global current_user
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        user = login_user(username, password)
        if user:
            current_user = user
            main_screen(root)
            return
        messagebox.showerror("Error", "Invalid credentials.")

    tk.Button(frame, text="Login", command=login, font=("Arial", 12), width=18, bg="#4caf50", fg="white").pack(pady=10)
    tk.Button(
        frame,
        text="Register",
        command=lambda: register_screen(root),
        font=("Arial", 12),
        width=18,
        bg="#2196f3",
        fg="white",
    ).pack(pady=5)


def register_screen(root):
    clear_root(root)

    root.configure(bg="#f0f8ff")

    frame = tk.Frame(root, bg="#f0f8ff")
    frame.pack(expand=True)

    tk.Label(frame, text="Create Account", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=15)
    tk.Label(frame, text="Create Username", font=("Arial", 14), bg="#f0f8ff").pack(pady=6)
    username_entry = tk.Entry(frame, font=("Arial", 14), width=25)
    username_entry.pack(pady=4)

    tk.Label(frame, text="Create Password", font=("Arial", 14), bg="#f0f8ff").pack(pady=6)
    password_entry = tk.Entry(frame, show="*", font=("Arial", 14), width=25)
    password_entry.pack(pady=4)

    def sign_up():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not username or not password:
            messagebox.showerror("Error", "Username and password are required.")
            return

        success = register_user(username, password)
        if success:
            messagebox.showinfo("Success", "Account created. Please login.")
            login_screen(root)
        else:
            messagebox.showerror("Error", "Username already exists or input is invalid.")

    tk.Button(frame, text="Sign Up", command=sign_up, font=("Arial", 12), width=18, bg="#673ab7", fg="white").pack(pady=10)
    tk.Button(
        frame,
        text="Back to Login",
        command=lambda: login_screen(root),
        font=("Arial", 12),
        width=18,
        bg="#9e9e9e",
        fg="white",
    ).pack(pady=5)


def book(root, movie_id):
    global current_user
    if book_movie(current_user[0], movie_id):
        messagebox.showinfo("Success", "Seat booked successfully.")
        main_screen(root)
    else:
        messagebox.showerror("Error", "No seats available for this movie.")
