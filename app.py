import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine
import matplotlib.pyplot as plt 
import streamlit as st

DATABASE_URL = "postgresql://readonly_student.tyxjmbptftftcqgozyfc:StudentRead123!@aws-1-us-east-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DATABASE_URL)

query = """
    SELECT
        t."name",
        t.album_id,
        a.title AS album_title,
        a2."name" AS artist_name,
        g."name" AS genre_name,
        mt."name" AS media_name,
        t.bytes,
        t.composer,
        t.genre_id,
        t.media_type_id,
        t.milliseconds,
        t.track_id,
        t.unit_price
    FROM track t
    JOIN album a
        ON t.album_id = a.album_id
    JOIN artist a2
        ON a2.artist_id = a.artist_id
    JOIN genre g
        ON g.genre_id = t.genre_id
    JOIN media_type mt
        ON mt.media_type_id = t.media_type_id"""

df = pd.read_sql(query, engine)

track_count_by_genre = df.groupby('genre_name').agg(num_tracks=('track_id', 'count')).reset_index()


artist_name = df.groupby('artist_name')["track_id"].count().sort_values("media_type_id", ascending=False)
art100 =artist_name.head(100)

print(track_count_by_genre)

fig, ax = plt.subplots()
sns.barplot(data=track_count_by_genre.sort_values('num_tracks', ascending=False), y='genre_name', x='num_tracks', ax=ax)

st.pyplot(fig)

artist = st.selectbox('Select an artist', df['artist_name'].unique())

filtered_df = df[df['artist_name'] == artist]

st.dataframe(filtered_df[['name', 'album_title', 'artist_name', 'genre_name']])


#displaying top hundred media by its artist name 
fig, ax1 =plt.subplots()
sns.barplot( data = art100, x ="artist_name", y ="track_id", ax =ax1)
st.pyplot(fig)



