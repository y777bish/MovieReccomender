# In[1]:

import numpy as np
import random as rd
import seaborn as sns
import math
import pandas as pd #przetwarzanie danych
import statistics
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# %%

c = pd.read_csv(r'titles.csv', sep=',')
credits = pd.read_csv(r'credits.csv', sep=',')
print(c)
# print(credits)
# %%

titles = pd.merge(c,credits)
c

# %%

titles.iloc[13]
# %%

titles.size
# %%

titles.index
# %%

titles.columns
# %%

titles.dtypes
# %%

titles['genres'] = titles['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
titles['genres'] = titles['genres'].str.split(',')
# %%

plt.subplots(figsize=(12,10))
list1 = []
for i in titles['genres']:
    list1.extend(i)
ax = pd.Series(list1).value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9,color=sns.color_palette('hls',10))
for i, v in enumerate(pd.Series(list1).value_counts()[:10].sort_values(ascending=True).values):
    ax.text(.8, i, v, fontsize=12, color='white',weight='bold')
plt.title('Top Genres')
plt.show()
# %%

for i, j in zip(titles['genres'],titles.index):
    list2 = []
    list2 = i
    list2.sort()
    titles.loc[j,'genres']=str(list2)
titles['genres'] = titles['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')
titles['genres'] = titles['genres'].str.split(',')
# %%

genreList = []
for index, row in titles.iterrows():
    genres = row["genres"]

    for genre in genres:
        if genre not in genreList:
            genreList.append(genre)
genreList[:10]
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

titles['genres_bin'] = titles['genres'].apply(lambda x: binary(x))
titles['genres_bin'].head()
# %%
