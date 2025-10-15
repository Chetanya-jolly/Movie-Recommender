import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval

# Load datasets
df1 = pd.read_csv("tmdb_5000_credits.csv")
df2 = pd.read_csv("tmdb_5000_movies.csv")

# Rename columns in df1 for clarity
df1.columns = ['id','title','cast','crew']

# Merge with suffixes so movies.csv's 'title' stays as 'title'
df2 = df2.merge(df1, on='id', suffixes=('','_credits'))

# Drop the duplicated title column from credits
df2.drop(columns=['title_credits'], inplace=True)

# Parse JSON-like fields into Python objects
features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)

# Extract director
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

# Extract top 3 names from a list of dicts
def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        return names[:3] if len(names) > 3 else names
    return []

# Clean data: lowercase & remove spaces
def clean_data(x):
    if isinstance(x, list):
        return [i.replace(" ", "").lower() for i in x]
    elif isinstance(x, str):
        return x.replace(" ", "").lower()
    return ''

# Apply feature extraction
df2['director'] = df2['crew'].apply(get_director)
for feature in ['cast', 'keywords', 'genres']:
    df2[feature] = df2[feature].apply(get_list)
df2['director'] = df2['director'].apply(clean_data)

# Create the "soup" feature
def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

df2['soup'] = df2.apply(create_soup, axis=1)

# Vectorize and compute cosine similarity
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Reset index and build reverse mapping (title → index)
df2 = df2.reset_index(drop=True)
indices = pd.Series(df2.index, index=df2['title'].str.lower()).drop_duplicates()

# Recommendation function
def get_recommendations(title):
    title = title.lower()
    if title not in indices:
        raise ValueError(f"Movie '{title}' not found!")
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df2['title'].iloc[movie_indices].tolist()