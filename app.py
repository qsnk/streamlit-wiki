import requests
from bs4 import BeautifulSoup
import streamlit as st
import wikipedia
from wikipedia import WikipediaPage

def get_languages() -> dict:
    languages: dict = dict()
    response = requests.get('https://meta.wikimedia.org/wiki/List_of_Wikipedias')
    if response.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
        rows: list = soup.find('table', {'class': 'list-of-wikipedias-table'}).find('tbody').find_all('tr')[1:]
        for row in rows:
            cells: list = row.find_all('td')
            lang: str = cells[1].text
            wiki: str = cells[3].text
            languages.update({lang: wiki})

        return languages


languages: dict = get_languages()
page: WikipediaPage | str | None = None

with st.sidebar:
    st.title(body='Search params')
    wiki = st.selectbox(label='Choose a language', options=languages.keys())
    wikipedia.set_lang(languages[wiki])
    text = st.text_input(label='Enter a text to search for')
    if text:
        results: list = wikipedia.search(text)
        select: str = st.selectbox(label='Search results', options=results)
        if st.button(label='Search'):
            try:
                page: WikipediaPage = wikipedia.page(title=select)
            except:
                page: str = 'Troubles to get page from wikipedia. Try another query!'

st.title('Wiki')

if not page:
    st.header('<- Search for some page')

if type(page) == str:
    st.header(page)

if type(page) == WikipediaPage:
    st.header(page.title)
    st.html(page.html())
