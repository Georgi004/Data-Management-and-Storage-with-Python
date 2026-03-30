import pandas as pd


movies = pd.read_csv("movies.csv")

movies["box_office"] = pd.to_numeric(movies["box_office"], errors = "coerce")
movies["budget"] = pd.to_numeric(movies["budget"], errors = "coerce")

movies["bilant"] = movies["box_office"] - movies["budget"]

columns_to_keep = ["title", "release_year", "genre", "director", "bilant", "country"]
movies = movies[columns_to_keep]

tari = {
    "USA": "top10_usa.xlsx",
    "Russia": "top10_russia.xlsx",
    "England": "top10_england.xlsx",
    "South Korea": "top10_southkorea.xlsx"
}


for tara, fisier in tari.items():
    subset = movies[movies["country"] == tara].copy()
    subset = subset.sort_values(by="bilant", ascending=False)

    top10 = subset.head(10).copy()
    top10 = top10.drop(columns=["country"])
    top10.to_excel(fisier, index=False)

print("Fisierele Excel au fost generate cu succes!")