#import bibliotek
import requests
import pprint
import json
from bs4 import BeautifulSoup
#adres URL strony z opiniami
url_prefix = "https://www.ceneo.pl"
product_id = input("Podaj kod produktu: ")
url_postfix = "/"+ product_id +"#tab=reviews"
url = url_prefix+url_postfix
opinions_list = []

#pobranie kodu HTML strony z adresu URL
while url is not None:
    page_response = requests.get(url)
    page_tree = BeautifulSoup(page_response.text, 'html.parser')
    # print(page_tree.prettify())
    #wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom
    opinions = page_tree.select("li.js_product-review")
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
        # print(useful)
        # print(useless)
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
        opinion_dict = {
            "opinion_id":opinion_id,
            "author":author,
            "recomendation":recomendation,
            "stars":stars,
            "content":content,
            "pros":pros,
            "cons":cons,
            "useful":useful,
            "useless":useless,
            "purchased":purchased,
            "purchase_date":purchase_date,
            "review_date":review_date
        }
        opinions_list.append(opinion_dict)
        # print(opinion_id, author, recomendation, stars, content, pros, cons, useful, useless, purchased, purchase_date, review_date)
    # print(opinion)
        # print(opinions_list)
    # print(opinions_list)
    # for opinion in opinions_list:
    #     # pprint.pformat(opinion)
    #     pprint.pprint(opinion)
    try:
        url = url_prefix+page_tree.select("a.pagination__next").pop()["href"]
    except IndexError:
        url = None
    print(url)
# filename = product_id+".json"
with open(product_id+".json",'w',encoding="utf-8") as fp:
    json.dump(opinions_list,fp,ensure_ascii=False,indent=4)
# print(opinions_list)
# for opinion in opinions_list:
#     # pprint.pformat(opinion)
#     pprint.pprint(opinion)