import requests
import threading
import os
from bs4 import BeautifulSoup

URL = 'https://bunsuke.substack.com/archive?sort=search&search=%23'


def load_file(file_name: str) -> list:
    """"""
    if not os.path.exists(file_name):
        return list()
    with open(file_name, 'r') as file:
        loaded_file = file.readlines()

    return loaded_file


def parse_articles(articles: list, index: int) -> None:
    """"""
    name = str(index) + ' - '
    article = requests.get(URL + name)
    soup = BeautifulSoup(article.content, 'html.parser')

    link = soup.find('a', class_='post-preview-title newsletter')
    if link and link.text.startswith('#' + name):
        if link.text not in articles:
            articles.append(link.text)
            print(link['href'])
            parse_article(link['href'])
        else:
            print(link['href'] + ' (skipped)')


def parse_article(URL: str):
    """"""
    article = requests.get(URL)
    content = BeautifulSoup(article.content, 'html.parser')
    retreive_vocabulary(content)


def retreive_vocabulary(content: BeautifulSoup):
    """"""
    vocabulary_list = content.find('ul')

    if vocabulary_list:
        for item in vocabulary_list.find_all('li'):
            word = parse_list_item(item)
            if not vocabulary_contains(word):
                vocabulary.append(word)
            else:
                skipped_vocabulary.append(word)


def vocabulary_contains(word: list) -> bool:
    """"""
    for vocab in vocabulary:
        if vocab[0] == word[0]:
            return True
    return False


def parse_list_item(list_item) -> list:
    """"""
    paragraph = list_item.find('p').text
    return [word for word in paragraph.split('\u3000') if word]


def format_vocabulary(items: list) -> str:
    """"""
    if len(items) == 2:
        return f'{items[0]}\t📖 {items[1]}\n'
    return f'{items[0]}\t{items[1]} 📖 {items[2]}\n'


def save_vocabulary(file_name: str) -> None:
    """"""
    with open(file_name, 'a+') as file:
        formatted_vocab = [format_vocabulary(vocab) for vocab in vocabulary]
        file.writelines(formatted_vocab)


skipped_vocabulary = []
articles = load_file('articles.txt')
vocabulary = load_file('vocabulary.txt')

if __name__ == '__main__':

    if not os.path.exists('data'):
        os.makedirs('data')

    article_number = 100
    for index in range(30, article_number):
        parse_articles(articles, index)

    with open('vocabulary.txt', 'a+') as file:
        formatted_vocab = ['\t'.join(vocab) + '\n' for vocab in vocabulary]
        file.writelines(formatted_vocab)

    save_vocabulary('data/Vocabulaire.txt')

    # print(f'\nVocabulary: {vocabulary}')
    print(f'\nArticles:  {articles}')
    print(f'\nNumber of articles:  {len(articles)} ({article_number})')
    print(
        f'Vocabulary:          {len(vocabulary)} ({len(skipped_vocabulary)} skipped)')
