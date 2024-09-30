import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt

#load data
file_path="C:/Users/Pratham.m/Downloads/netflix_titles.csv"
netflix_data=pd.read_csv(file_path)

#Data Preprocessing
netflix_data['date_added']=pd.to_datetime(netflix_data['date_added'],errors='coerce')
netflix_data['director'].fillna('Unknown',inplace=True)
movies_data=netflix_data[netflix_data['type']=='Movie'].dropna(subset=['release_year','rating'])

#sidebar filters
st.sidebar.title("Filter Options")
selected_genre=st.sidebar.multiselect("Select Genre",options=movies_data['listed_in'].str.split(',').explode().unique())
selected_year=st.sidebar.slider("Select Release Year",int(movies_data['release_year'].min()),int(movies_data['release_year'].max()),(2000,2021))

#Apply Filters
if selected_genre:
    movies_data=movies_data[movies_data['listed_in'].apply(lambda x:any(genre in x for genre in selected_genre))]
    movies_data=movies_data[(movies_data['release_year']>=selected_year[0]) & (movies_data['release_year']<=selected_year[1])]
    
#Title
st.title("Netfilx Movies Data Visualization Dashboard")

#Movie Release Trend
st.subheader("Number of Movies Released Each year")
movies_per_year=movies_data['release_year'].value_counts().sort_index()
plt.figure(figsize=(10,6))
plt.bar(movies_per_year.index,movies_per_year.values,color='skyblue')
plt.xlable('Year')
plt.ylabel('Number of Movies')
st.pyplot(plt)

#Movie rating disctribution
st.subheader('Movies By Rating')
rating_distribution=movies_data['rating'].value_counts()
fig,ax=plt.subplots()
ax.pie(rating_distribution,labels=rating_distribution.index,autopct='%1.1f%%',colors=plt.cm.Paired.colors)
plt.title('Distribution of Movies BY Rating')
st.pyplot(fig)

#top Genres
st.subheader("Top Movie Genres")
genres=movies_data['listed_in'].str.split(',').explode().str.strip()
top_genres=genres.value_counts().head(10)
plt.bar(top_genres.index,top_genres.values,color='lightgreen')
plt.xlabel('Genre')
plt.ylabel('Number of Movies') 
st.pyplot(plt)

#Add some interactions
st.sidebar.subheader("About")
st.sidebar.info("This dashboard allows users to explore Netfilx Movies dataset, Filtered by genre,year and other options")