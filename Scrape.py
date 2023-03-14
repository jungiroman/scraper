import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Comment


def hide_header():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


def get_images(soup, url):
    imagetags = soup.find_all('img')
    images = pd.DataFrame(columns=['source', 'alt', 'url'])
    for image in imagetags:
        try:
            if int(image['height']) > 100:
                link = "https:" + image['src']
                if link.startswith("https://"):
                    new_row = {'source': url, 'alt': image['alt'], 'url': link}
                    images = images.append(new_row, ignore_index=True)
        except:
            pass
    return images


def get_text(soup, url):
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(soup):
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    texts = text_from_html(soup)
    return texts


def scrape(url):
    st.write("URL: " + url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    st.session_state['images'] = get_images(soup, url)
    st.session_state['text'] = get_text(soup, url)

    st.write(
        f'<iframe width=100%, height=600, src="{url}"></iframe>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Scrape App", page_icon=":random:", layout="wide")
    hide_header()
    reload_data = False
    st.title('Scrape App')

    url_input = st.text_input('Enter URL', value='https://en.wikipedia.org/wiki/Special:Random')
    if st.button('Scrape'):
        if url_input:
            scrape(url_input)
        else:
            st.info('Enter URL')


