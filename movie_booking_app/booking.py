from database import book_seat, get_movies, search_movies as db_search_movies

def list_movies():
    return get_movies()

def search_movies(keyword):
    return db_search_movies(keyword)

def book_movie(user_id, movie_id):
    return book_seat(user_id, movie_id)
