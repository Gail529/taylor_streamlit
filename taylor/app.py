# -*- coding: utf-8 -*-


import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

#from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
PAGE_CONFIG = {"page_title":"Taylor","page_icon":":smiley:","layout":"centered"}
st.set_page_config(**PAGE_CONFIG)


#image = Image.open('tay_img.jpg')

df=pd.read_csv('song_df.csv')
song_df=df.filter(['song'])

#calculating the similarities scores
cols=song_df.columns
scores_df=df[['Positive','Negative','Anger','Anticipation','Disgust','Fear','Joy','Sadness','Surprise','Trust','acousticness','danceability','energy','liveness','loudness','speechiness','tempo','valence','popularity']]
cosine_sim=cosine_similarity(scores_df,scores_df)
indices=pd.Series(song_df.index, song_df['song']).drop_duplicates()

#function that will generate the recommendations
def get_recommendations(title,cosine_sim=cosine_sim):   
    index=indices[title]
    sim_scores = list(enumerate(cosine_sim[index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    song_indices = [i[0] for i in sim_scores]
    return df[['song','album']].iloc[song_indices]


choice = st.sidebar.text_input('Key in a Song')
st.sidebar.write("Select a song")
st.sidebar.dataframe(song_df,500,400)


col1,col2=st.beta_columns(2)

with col1:  
    st.header("Music Recommendation Engine")
    st.write("Get Recommendations for your favourite Taylor Swift songs based on your current emotional state.")
with col2:    
    st.image(image,width=300,height=200)


if choice:
    st.subheader("More songs like "+choice )
    recommendations=get_recommendations(choice)
    st.table(recommendations)

if not choice:
    st.header('Pick a song')
    st.subheader('recommendations will appear here :smiley:')

