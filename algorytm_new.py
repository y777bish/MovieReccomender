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
from wordcloud import WordCloud, STOPWORDS
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

# %%

movies = pd.read_csv('movies_5000.csv')
credits = pd.read_csv('credits_5000.csv')
# %%

movies.head()
# %%

# changing the genres column from json to string
movies['genres'] = movies['genres'].apply(json.loads)
for index,i in zip(movies.index,movies['genres']):
    list1 = []
    for j in range(len(i)):
        list1.append((i[j]['name'])) # the key 'name' contains the name of the genre
    movies.loc[index,'genres'] = str(list1)

# changing the keywords column from json to string
movies['keywords'] = movies['keywords'].apply(json.loads)
for index,i in zip(movies.index,movies['keywords']):
    list1 = []
    for j in range(len(i)):
        list1.append((i[j]['name']))
    movies.loc[index,'keywords'] = str(list1)
    
# changing the production_companies column from json to string
movies['production_companies'] = movies['production_companies'].apply(json.loads)
for index,i in zip(movies.index,movies['production_companies']):
    list1 = []
    for j in range(len(i)):
        list1.append((i[j]['name']))
    movies.loc[index,'production_companies'] = str(list1)

# changing the cast column from json to string
credits['cast'] = credits['cast'].apply(json.loads)
for index,i in zip(credits.index,credits['cast']):
    list1 = []
    for j in range(len(i)):
        list1.append((i[j]['name']))
    credits.loc[index,'cast'] = str(list1)

# changing the crew column from json to string    
credits['crew'] = credits['crew'].apply(json.loads)
def director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
credits['crew'] = credits['crew'].apply(director)
credits.rename(columns={'crew':'director'},inplace=True)
# %%

movies = movies.merge(credits,left_on='id',right_on='movie_id',how='left')
movies = movies[['id','original_title','genres','cast','vote_average','director','keywords']]
# %%

movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['genres'] = movies['genres'].str.split(',')
# %%


# ------>WYŚWIETLANIE TOP GENRES<-------------
plt.subplots(figsize=(12,10))
list1 = []
for i in movies['genres']:
    list1.extend(i)
ax = pd.Series(list1).value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9,color=sns.color_palette('hls',10))
for i, v in enumerate(pd.Series(list1).value_counts()[:10].sort_values(ascending=True).values): 
    ax.text(.8, i, v,fontsize=12,color='white',weight='bold')
plt.title('Top Genres')
plt.show()
# %%


# -------> Formatowanie movies oraz połączenie movies['genres'] i movies.index <-----------
for i,j in zip(movies['genres'],movies.index):
    list2=[]
    list2=i
    list2.sort()
    movies.loc[j,'genres']=str(list2)
movies['genres'] = movies['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['genres'] = movies['genres'].str.split(',')
# %%



# -------> Dodawanie kategorii filmów do listy genreList <-----------
genreList = []
top_genres = pd.Series(list1).value_counts()[:10].index.tolist()

for index, row in movies.iterrows():
    genres = row["genres"]

    for genre in genres:
        if genre in top_genres:
            genreList.append(genre)

genreList = list(set(genreList))  # Usunięcie powtórzeń za pomocą zbioru i konwersja z powrotem na listę
print(genreList)


# %%

def binary(genre_list):
    binaryList = []
    
    for genre in genreList:
        if genre in genre_list:
            binaryList.append(1)
        else:
            binaryList.append(0)
    
    return binaryList
# %%
# -----> Dodawanie nowej kolumny do ramki danych movies o nazwie 'genres_bin' <-------
movies['genres_bin'] = movies['genres'].apply(lambda x: binary(x))
movies['genres_bin'].head()
# %%


# -----> Formatowanie kolumny 'cast' <---------
movies['cast'] = movies['cast'].str.strip('[]').str.replace(' ','').str.replace("'",'').str.replace('"','')
movies['cast'] = movies['cast'].str.split(',')
# %%


# ------> Tworzenie oraz wyświetlanie wykresu 'Actors with highest appearance' <----------
plt.subplots(figsize=(12,10))
list1=[]
for i in movies['cast']:
    list1.extend(i)
ax=pd.Series(list1).value_counts()[:15].sort_values(ascending=True).plot.barh(width=0.9,color=sns.color_palette('muted',40))
for i, v in enumerate(pd.Series(list1).value_counts()[:15].sort_values(ascending=True).values): 
    ax.text(.8, i, v,fontsize=10,color='white',weight='bold')
plt.title('Actors with highest appearance')
plt.show()
# %%


# ----> Połączenie dwóch sekcji danych w jedną, formatowanie 'cast', ponowne połączenie oraz formatowanie <----------
for i,j in zip(movies['cast'],movies.index):
    list2 = []
    list2 = i[:4]
    movies.loc[j,'cast'] = str(list2)
movies['cast'] = movies['cast'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['cast'] = movies['cast'].str.split(',')
for i,j in zip(movies['cast'],movies.index):
    list2 = []
    list2 = i
    list2.sort()
    movies.loc[j,'cast'] = str(list2)
movies['cast']=movies['cast'].str.strip('[]').str.replace(' ','').str.replace("'",'')
# %%



# -----> Dodawanie danych do listy CastList(lista aktorów) <---------
castList = []
top_casts = pd.Series(list1).value_counts().drop('').index.tolist()[:10]
top_casts = [actor.replace('Jr.', 'Robert Downey Jr.') for actor in top_casts]
print(top_casts)

for index, row in movies.iterrows():
    cast = row["cast"]

    for i in cast:
        if i in top_casts:
            castList.append(i)


# Definicja funkcji 'binary' z poprawioną nazwą parametru
def binary(cast_list):
    binaryList = []

    for actor in top_casts:
        if actor in cast_list:
            binaryList.append(1)
        else:
            binaryList.append(0)

    return binaryList


# Dodanie nowej kolumny 'cast_bin' do ramki danych 'movies'
movies['cast_bin'] = movies['cast'].apply(lambda x: binary(x))
movies['cast_bin'].head()


# %%

def xstr(s):
    if s is None:
        return ''
    return str(s)
movies['director'] = movies['director'].apply(xstr)
# %%


# ------> Tworzenie wykresu 'Directors with highest movies' <-------
plt.subplots(figsize=(12,10))
list1=[]
for i in movies['director']:
    list1.extend(i)
ax = movies[movies['director']!=''].director.value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9,color=sns.color_palette('muted',40))
for i, v in enumerate(movies[movies['director']!=''].director.value_counts()[:10].sort_values(ascending=True).values): 
    ax.text(.5, i, v,fontsize=12,color='white',weight='bold')
plt.title('Directors with highest movies')
plt.show()
# %%


# ------> Tworzenie listy 'director' <--------
top_directors = movies['director'].explode().value_counts().drop('').index[:10].tolist()
directorList = []
print(top_directors)
for index, row in movies.iterrows():
    cast = row["director"]
    for i in cast:
        if i in top_directors:
            directorList.append(i)


# Tworzenie soft set dla directorList
def binary(director_list):
    binaryList = []
    for direct in top_directors:
        if direct in director_list:
            binaryList.append(1)
        else:
            binaryList.append(0)
    return binaryList


# Dodanie nowej kolumny do ramki danych 'movies' o nazwie 'director_bin'
movies['director_bin'] = movies['director'].apply(lambda x: binary(x))
movies.head()

# %%
# ------> Tworzenie oraz wyświetlanie wykresu <------
plt.subplots(figsize=(12,12))
stop_words = set(stopwords.words('english'))
stop_words.update(',',';','!','?','.','(',')','$','#','+',':','...',' ','')

words=movies['keywords'].dropna().apply(nltk.word_tokenize)
word=[]
for i in words:
    word.extend(i)
word=pd.Series(word)
word=([i for i in word.str.lower() if i not in stop_words])
wc = WordCloud(background_color="black", max_words=2000, stopwords=STOPWORDS, max_font_size= 60,width=1000,height=1000)
wc.generate(" ".join(word))
plt.imshow(wc)
plt.axis('off')
fig=plt.gcf()
fig.set_size_inches(10,10)
plt.show()
# %%

movies['keywords'] = movies['keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'').str.replace('"','')
movies['keywords'] = movies['keywords'].str.split(',')
for i,j in zip(movies['keywords'],movies.index):
    list2 = []
    list2 = i
    movies.loc[j,'keywords'] = str(list2)
movies['keywords'] = movies['keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['keywords'] = movies['keywords'].str.split(',')
for i,j in zip(movies['keywords'],movies.index):
    list2 = []
    list2 = i
    list2.sort()
    movies.loc[j,'keywords'] = str(list2)
movies['keywords'] = movies['keywords'].str.strip('[]').str.replace(' ','').str.replace("'",'')
movies['keywords'] = movies['keywords'].str.split(',')
# %%
top_words = movies['keywords'].explode().value_counts().drop('').index[:10].tolist()
words_list = []
print(top_words)
for index, row in movies.iterrows():
    keywords = row["keywords"]
    
    for keyword in keywords:
        if keyword in top_words:
            words_list.append(keywords)
# %%
# ------> Tworzenie soft set dla kategorii filmów <------

def binary(words):
    binaryList = []
    for keyword in top_words:
        if keyword in words_list:
            binaryList.append(1)
        else:
            binaryList.append(0)
    return binaryList
# %%

movies['words_bin'] = movies['keywords'].apply(lambda x: binary(x))
movies = movies[(movies['vote_average']!=0)] #removing the movies with 0 score and without drector names 
movies = movies[movies['director']!='']
# %%



# ------> Wyświetlanie danych <------
# ------> Zmiana 14.06.2023 - Nie musimy wprowadzać id, tylko nazwę <----------
def Soft_Set(row):
    genA = row['genres_bin']
    scorA = row['cast_bin']
    directA = row['director_bin']
    wordsA = row['words_bin']
    return [genA, scorA, directA, wordsA]
if 'Soft-Set' not in movies.columns:
    movies['Soft-Set'] = movies.apply(Soft_Set, axis=1)


def find_most_similar_film(query_film, movies):
    distances = []

    for _, row in movies.iterrows():
        soft_set = row['Soft-Set']
        distance = np.sqrt(np.sum(np.square(np.array(soft_set) - np.array(query_film))))
        distances.append(distance)

    nearest_indices = np.argsort(distances)[0:2]
    similar_films = movies.loc[nearest_indices, 'original_title'].tolist()

    return similar_films
query_film = movies.loc[movies['original_title'] == 'Grease', 'Soft-Set'].values[0]
print(find_most_similar_film(query_film, movies))