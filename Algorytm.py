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

movies = pd.read_csv(r"titles.csv")
credits = pd.read_csv(r"credits.csv")

# movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
# movies['genres'] = movies['genres'].str.split(',')
#
# plt.subplots(figsize=(12,10))
# list1 = []
# for i in movies['genres']:
#     list1.extend(i)
# ax = pd.Series(list1).value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9,color=sns.color_palette('hls',10))
# for i, v in enumerate(pd.Series(list1).value_counts()[:10].sort_values(ascending=True).values):
#     ax.text(.8, i, v,fontsize=12,color='white',weight='bold')
# plt.title('Top Genres')
# plt.show()



# STARA WERSJA!!
# ZbiorMiekki = movies.DataFrame({
#     'Genres':['drama', 'comedy', 'thriller', 'action', 'romance', 'documentation', 'crime', 'animation', 'family', 'fantasy']
# })

movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['genres'] = movies['genres'].str.split(',')


for i,j in zip(movies['genres'],movies.index):
    list2=[]
    list2=i
    list2.sort()
    movies.loc[j,'genres']=str(list2)
movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['genres'] = movies['genres'].str.split(',')



genreList = []
for index, row in movies.iterrows():
    genres = row["genres"]

    for genre in genres:
        if genre not in genreList:
            genreList.append(genre)
genreList[:10]  # now we have a list with unique genres


def binary(genre_list):
    # binaryList = []

    # for genre in genreList:
    #     if genre in genre_list:
    #         binaryList.append(1)
    #     else:
    #         binaryList.append(0)
    return [1 if genre in genre_list else 0 for genre in genreList]


movies['genres_bin'] = movies['genres'].apply(lambda x: binary(x))
movies['genres_bin'].head()

# def NearestFilm():
#     #string ChoosenFilm
#     #

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

movie_title = "Masha and the Bear"
common_genre = similar_by(movies, movie_title, "genres")
print(common_genre)

if common_genre:
    print(f"Similar movies to '{movie_title}':")
    for movie in common_genre:
        print(movie)
else:
    print(f"No similar movies found for '{movie_title}'")
