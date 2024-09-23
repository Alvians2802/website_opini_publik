import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import nltk
nltk.download('punkt')

def header():
    st.markdown(
        """
        <style>
        .center {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="center"><h1>Sentimen Analisis Opini Publik Kemenkeu</h1></div>', unsafe_allow_html=True)

def display_wordcloud(df):
    tweet_text = ' '.join(df['Tweet'].astype(str).tolist())
    wordcloud = WordCloud(width=800, height=550, background_color='white').generate(tweet_text)
    plt.figure(figsize=(12, 15))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt, use_container_width=True)

def display_sentiment_distribution(df):
    sentiment_counts = df['sentimen'].value_counts()
    fig = px.pie(sentiment_counts, values=sentiment_counts.values, names=sentiment_counts.index)
    fig.update_layout(width=800, height=300)
    st.plotly_chart(fig, use_container_width=True)

def display_top_usernames(df):
    top_usernames = df['username'].value_counts().head(10)
    fig = px.bar(top_usernames, x=top_usernames.index, y=top_usernames.values,
                 labels={'x': 'Username', 'y': 'Count'})
    fig.update_layout(width=800, height=550, xaxis={'categoryorder': 'total descending'})
    st.plotly_chart(fig, use_container_width=True)

def display_top_locations(df):
    top_locations = df['location'].value_counts().head(10)
    fig = px.bar(top_locations, y=top_locations.index, x=top_locations.values, orientation='h',
                 labels={'y': 'Location', 'x': 'Count'})
    fig.update_layout(width=800, height=550, yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

def app():
    st.title("Data Twitter Opini Publik Kementerian Keuangan")

    # Sidebar menu
    menu = ['Data', 'Visualisasi']
    choice = st.sidebar.selectbox('Menu', menu)

    # Logic when "Data" is selected from menu
    if choice == 'Data':
        # Load dataset
        df = pd.read_excel("Dataset_twitter.xlsx")  # Ganti dengan nama file Excel benar
        st.write(df)

    elif choice == 'Visualisasi':
        # Load dataset
        df = pd.read_excel("Dataset_twitter.xlsx")  # Ganti dengan nama file Excel benar
        st.subheader("Pilih Jenis Visualisasi")
        
        # Opsi visualisasi
        visualization_choice = st.selectbox("Pilih Visualisasi", ['Word Cloud', 'Sentiment Distribution', 'Top Usernames'])

        if visualization_choice == 'Word Cloud':
            st.subheader("Word Cloud")
            display_wordcloud(df)

        elif visualization_choice == 'Sentiment Distribution':
            st.subheader("Distribusi Sentimen")
            display_sentiment_distribution(df)

        elif visualization_choice == 'Top Usernames':
            st.subheader("Top Usernames")
            display_top_usernames(df)


if __name__ == "__main__":
    app()

