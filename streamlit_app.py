import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

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
        .table-wrapper {
            max-height: 400px;
            overflow-y: auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border: 1px solid #ddd;
            word-wrap: break-word;
            max-width: 200px;
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
    st.title("SATUKU")
    st.subheader("(Sentimen Analitik Kemenkeu)")

    st.write("""
    SATUKU adalah aplikasi yang dirancang untuk menganalisis sentimen publik terhadap Kementerian Keuangan (Kemenkeu) melalui data yang diperoleh dari media sosial platform X. Aplikasi ini menggunakan Machine Learning untuk mengidentifikasi dan membandingkan opini masyarakat, baik yang bersifat positif, negatif, maupun netral.""")

    menu = ['Data Periode Agustus 2023-2024', 'Visualisasi', 'Data Lainnya']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Data Periode Agustus 2023-2024':
        df = pd.read_excel("Dataset_twitter.xlsx")  # Ganti dengan nama file Excel benar
        
        st.subheader("Data Tweet")
        st.markdown('<div class="table-wrapper">', unsafe_allow_html=True)
        st.table(df.style.set_table_attributes('class="dataframe"').set_table_styles(
            [{'selector': 'td', 'props': [('word-wrap', 'break-word'), ('max-width', '200px')]}]
        ))
        st.markdown('</div>', unsafe_allow_html=True)

    elif choice == 'Visualisasi':
        df = pd.read_excel("Dataset_twitter.xlsx")  # Ganti dengan nama file Excel benar
        st.subheader("Pilih Jenis Visualisasi")
        
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

    elif choice == 'Data Lainnya':
        st.subheader("Unggah File Data Anda")
        
        uploaded_file = st.file_uploader("Pilih file Excel atau CSV", type=["csv", "xlsx"])

        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)

                st.success("Data berhasil diunggah!")
                st.write(df)

                st.subheader("Pilih Visualisasi untuk Data yang Diunggah")
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
            except Exception as e:
                st.error(f"Terjadi kesalahan dalam membaca file: {e}")

if __name__ == "__main__":
    app()
