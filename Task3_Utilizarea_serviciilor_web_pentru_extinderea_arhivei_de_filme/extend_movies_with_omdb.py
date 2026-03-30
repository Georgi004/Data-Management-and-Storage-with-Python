import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor


movies = pd.read_csv("movies.csv")

movies["imdb_rating"] = None
movies["actors"] = None
movies["imdb_votes"] = None
movies["found_in_omdb"] = False

API_KEY = "60b77343"
BASE_URL = "https://www.omdbapi.com/"


def fetch_omdb_data(row):
    title = row["title"]
    year = row["release_year"]
    params = {"t": title, "y": year, "apikey": API_KEY}
    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        data = response.json()
        if data.get("Response") == "True":
            return (row.name, data.get("imdbRating"), data.get("Actors"), data.get("imdbVotes"))
        else:
            print(f"Warning: {title} - {data.get('Error')}")

    except Exception as e:
        print(f"Eroare la {title}: {e}")

    return(row.name, None, None, None)

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_omdb_data, [row for _, row in movies.iterrows()]))

for idx, rating, actors, votes in results:
    movies.at[idx, "imdb_rating"] = rating
    movies.at[idx, "actors"] = actors
    movies.at[idx, "imdb_votes"] = votes
    if rating is not None:
        movies.at[idx, "found_in_omdb"] = True

movies["imdb_rating"] = pd.to_numeric(movies["imdb_rating"], errors = "coerce")

movies.to_xml("movies_extended.xml", index = False)

not_found = movies[movies["found_in_omdb"] == False]
if not not_found.empty:
    print("\nFilme negasite in OMDb:")
    print(not_found[["title", "release_year"]])

top10 =  movies[movies["imdb_rating"].notna()].sort_values(by = "imdb_rating", ascending=False).head(10)
print("\nTop 10 filme dupa IMDB:\n")
print(top10[["title", "release_year", "imdb_rating", "actors", "imdb_votes"]])

