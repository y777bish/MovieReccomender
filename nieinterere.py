# %%

import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import seaborn as sns
import numpy as np
import json
import warnings
warnings.filterwarnings('ignore')
import base64
import io
from matplotlib.pyplot import imread
import codecs
from IPython.display import HTML

# %%

movies = pd.read_csv(r"titles.csv")
credits = pd.read_csv(r"credits.csv")

# %%

movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['genres'] = movies['genres'].str.split(',')

# %%

for i,j in zip(movies['genres'],movies.index):
    list2=[]
    list2=i
    list2.sort()
    movies.loc[j,'genres']=str(list2)
movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['genres'] = movies['genres'].str.split(',')

# %%

genreList = []
for index, row in movies.iterrows():
    genres = row["genres"]

    for genre in genres:
        if genre not in genreList:
            genreList.append(genre)
genreList[:10]  # now we have a list with unique genres

# %%

def binary(genre_list):
    # binaryList = []

    # for genre in genreList:
    #     if genre in genre_list:
    #         binaryList.append(1)
    #     else:
    #         binaryList.append(0)
    return [1 if genre in genre_list else 0 for genre in genreList]

#%%

movies['genres_bin'] = movies['genres'].apply(lambda x: binary(x))
movies['genres_bin'].head()

# %%

# Soft-Set similarity between movies:

movies = pd.read_csv('titles.csv')
def similar_by(movies, movie_title, column_name):
    selected_movie_data = movies.loc[movies['title'] == movie_title]

    if selected_movie_data.empty:
        return None

    genres = selected_movie_data.iloc[0][column_name]
    similar_movies = movies[movies[column_name] == genres]
    similar_movies = similar_movies[similar_movies['title'] != movie_title]


    if similar_movies.empty:
        return None

    return similar_movies['title'].tolist()

# %%

movie_title = "Masha and the Bear"
common_genre = similar_by(movies, movie_title, "genres")
print(common_genre)

# %%

if common_genre:
    print(f"Similar movies to '{movie_title}':")
    for movie in common_genre:
        print(movie)
else:
    print(f"No similar movies found for '{movie_title}'")

# %%

actor_counts = credits['person_id'].value_counts()

# Wybranie 14 najczęściej występujących aktorów
top_actors = actor_counts.head(10)
print(top_actors)
# Teoretyczna próba przypisania imienia i nazwiska aktorów występujących w 

# for i in zip(credits['name'])

# # Dołącz nazwy aktorów do top_actors na podstawie 'person_id'
# top_actors_with_names = top_actors.merge(actor_mapping, on='person_id', how='left')

# # Wyświetl wynik
# print(top_actors_with_names)

# %%

# Wyświetlenie wykresu słupkowego
sns.barplot(x=top_actors.index, y=top_actors.values)
sns.set(style="whitegrid")
plt.xticks(rotation=90)
plt.xlabel('Actor ID')
plt.ylabel('Count')
plt.title('Top 14 Actors by Frequency')
plt.show()

# %%
