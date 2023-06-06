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

movies = pd.read_csv(r"C:\projektSSI\MovieReccomender\movies.csv")
credits = pd.read_csv(r"C:\projektSSI\MovieReccomender\credits.csv")

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
    binaryList = []

    for genre in genreList:
        if genre in genre_list:
            binaryList.append(1)
        else:
            binaryList.append(0)

    return binaryList


movies['genres_bin'] = movies['genres'].apply(lambda x: binary(x))
movies['genres_bin'].head()

# def NearestFilm():
#     #string ChoosenFilm
#     #




def find_similar_movie(movie_title):
    movies = pd.read_csv('movies.csv')
    selected_movie_data = movies.loc[movies['title'] == movie_title]

    if selected_movie_data.empty:
        return None

    genres = selected_movie_data.iloc[0]['genres']
    similar_movies = movies[movies['genres'] == genres]
    similar_movies = similar_movies[similar_movies['title'] != movie_title]


    if similar_movies.empty:
        return None

    return similar_movies['title'].tolist()

movie_title = "Big Daddy"
similar_movies = find_similar_movie(movie_title)


if similar_movies:
    print(f"Similar movies to '{movie_title}':")
    for movie in similar_movies:
        print(movie)
else:
    print(f"No similar movies found for '{movie_title}'")