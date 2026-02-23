from database import book_seat, get_movies

def list_movies():
    return get_movies()

def book_movie(user_id, movie_id):
    return book_seat(user_id, movie_id)