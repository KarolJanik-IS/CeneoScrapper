#import bibliotek
import requests
from bs4 import BeautifulSoup
#adres URL strony z opiniami
url = "https://www.ceneo.pl/76891706#tab=reviews"
#pobranie kodu HTML strony z adresu URL
page_response = requests.get(url)
page_tree = BeautifulSoup(page_response.text, 'html.parser')
# print(page_tree.prettify())
#wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom
opinions = page_tree.select("li.review-box")
# print(type(opinions))
for opinion in opinions:
    opinion_id = opinion["data-entry-id"]
    # print(opinion_id)
    author = opinion.select('div.reviewer-name-line').pop().string.strip()
    try:
        recomendation = opinion.select('div.product-review-summary > em').pop().string.strip()
    except IndexError:
        recomendation = None
    stars = opinion.select('span.review-score.count')
    try:
        purchased = opinion.select('div.product-review-pz').pop().string
    except IndexError:
        purchased = None
    useful =  opinion.select('button.vote-yes').pop()["data-total-vote"]
    useless =  opinion.select('button.vote-no').pop()["data-total-vote"]
    content = opinion.select('p.product-review-body').pop().get_text()
    # useful = useful_button["data-total-vote"]
    #useful = opinion.select('button.vote-yes')
    print(useful)
    print(useless)
    try:
        cons = opinion.select('div.cons-cell > ul').pop().get_text()
    except IndexError:
        cons = None
    try:
        pros = opinion.select('div.pros-cell > ul').pop().get_text()
    except IndexError:
        pros = None
    date = opinion.select('span.review-time > time')
    review_date = date.pop(0)["datetime"]
    try:
        purchase_date = date.pop(0)["datetime"]
    except IndexError:
        purchase_date = None
    # print(review_date, purchase_date)
    print(opinion_id, author, recomendation, stars, content, pros, cons, useful, useless, purchased, purchase_date, review_date)
# print(opinion)
#ekstrakcja składowych dla pierwszej opinii z listy

# # CeneoScraper
# # Etap 1 - pobranie pojedynczeej opinii 
# - opinia: .li.review-box
# - identyfikator: ["data-entry-id"]
# - autor: div.reviewer-name-line
# - rekomendacja: div.product-review-summary > em
# - liczba gwiazdek: span.review-score.count
# - czy potwierdzona zakupem: div.product-review-pz
# - data wystawienia: span.review-time > time["datetime"] - pierwsze wystąpienie
# - data zakupu: span.review-time > time["datetime"] - drugie wystąpienie
# - przydatna: button.votes-yes["data-total-vote"]
# - nieprzydatna:button.votes-no["data-total-vote"]
# - treść: p.product-review-body
# - wady: div.cons-cell > ul
# - zalety: div.pros-cell > ul