import streamlit as st
import nltk
import re
from textblob import TextBlob
from gensim.parsing.preprocessing import remove_stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS



def hide_header():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


def process_text(text):
    text = text.lower()
    text = re.sub(r'[.,"\'-?:!;’‘]', '', text)
    text = remove_stopwords(text)
    text = " ".join([word.lemmatize() for word in TextBlob(text).words])
    return text


def prep(text):
    text = process_text(text)
    stemmer = PorterStemmer()

    # Get list of stopwords
    stop_words = set(stopwords.words("english"))

    # Preprocess the headlines

        # Tokenize the headline
    text_tokens = word_tokenize(text)

        # Remove stopwords and stem the tokens
    text_tokens = [stemmer.stem(token) for token in text_tokens if token not in stop_words]

        # Join the preprocessed tokens back into a single headline
    text = " ".join(text_tokens)

    # Pass the preprocessed headlines to the LDA model
    return text

def draw_wordcloud(text):
    width = 1200
    height = 600
    wordcloud = WordCloud(width=width, height=height, random_state=1, mode='RGBA',
                          background_color=None, colormap='Pastel1',
                          collocations=False, stopwords=STOPWORDS)

    wordcloud_image = wordcloud.generate(text).to_image()
    st.image(wordcloud_image)


def analyse_text(text):
    text = prep(text)
    draw_wordcloud(text)



if __name__ == "__main__":
    st.set_page_config(page_title="Scrape App - Text analysis", page_icon="🤖", layout="wide")
    hide_header()
    st.title('Text analysis')
    if 'text' in st.session_state:
        analyse_text(st.session_state.text)
    else:
        st.warning('No data. Go to main page first')
