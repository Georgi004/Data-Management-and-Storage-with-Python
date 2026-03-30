import pickle
import os

MOVIES_FILE = "movies.pkl"

class Movie:
    def __init__(self, title, release_year, genre, imdb_url):
        self.title = title
        self.release_year = release_year
        self.genre = genre
        self.imdb_url = imdb_url

    def __str__(self):
        return f"{self.title}, {self.release_year}\n{self.genre}\n{self.imdb_url}"
    


def load_movies():
    if os.path.exists(MOVIES_FILE):
        with open(MOVIES_FILE, "rb") as f:
            return pickle.load(f)
    return []


def save_movies(movies):
    with open(MOVIES_FILE, "wb") as f:
        pickle.dump(movies, f)


def add_movie():
    title = input("Movie title: ")
    release_year = input("Movie release year: ")
    genre = input("Movie genre: ")
    imdb_url = input("Movie IMBD URL: ")

    movie = Movie(title, release_year, genre, imdb_url)
    movies = load_movies()
    movies.append(movie)
    save_movies(movies)


def view_movies():
    movies = load_movies()
    if not movies:
        print("\nNo movies in the watchlist yet!\n")
    else:
        print()
        for movie in movies:
            print(movie, "\n")

def main():
    print("********WELCOME TO MOVIE WATCHLIST APP*******")

    while True:
        print("Add new movie(1)")
        print("Show All movies(2)")
        print("Exit(3)")
        choice = input()

        if choice == "1":
            add_movie()
        elif choice == "2":
            view_movies()
        elif choice == "3":
            print("Have a nice day!")
            break
        else:
            print("Invalid option, please try again!")

if __name__ == "__main__":
    main()