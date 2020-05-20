import requests
from bs4 import BeautifulSoup
from enum import Enum, auto
from app import utils

# def extract_feature(opinion, selector, attribute = None):
#     try:
#         if not attribute:
#             return opinion.select(selector).pop().get_text().strip()
#         else:
#             return opinion.select(selector).pop()[attribute]
#     except IndexError:
#         return None

class Product:
    def __init__(self, product_id=None, name=None, opinions = []):
        self.product_id = product_id
        self.name = name
        self.opinions = opinions
    def __str__(self):
        # print(self.opinions)
        # return f'product id: {self.product_id}\n nazwa: {self.name}\n'+'\n'.join(self.opinions)
        # print(self.opinions)
        return f'product id: {self.product_id}\n nazwa: {self.name}\n\n'+'\n'.join(str(opinion) for opinion in self.opinions)
    def extract_product(self):
        page_response = requests.get("https://www.ceneo.pl/"+self.product_id)
        page_tree = BeautifulSoup(page_response.text, 'html.parser')
        self.name = page_tree.select("h1.product-name").pop().get_text().strip()
        try:
            opinions_count = int(page_tree.select("a.product-reviews-link > span").pop().get_text().strip())
        except IndexError:
            opinions_count = 0
        if opinions_count > 0:
            url_prefix = "https://www.ceneo.pl"
            url_postfix = "#tab=reviews"
            url = url_prefix+"/"+self.product_id+url_postfix
            opinions_list = []
            while url:
                print(url)
                #pobranie kodu HTML strony z adresu URL
                page_response = requests.get(url)
                page_tree = BeautifulSoup(page_response.text, 'html.parser')

                #wybranie z kodu strony fragmentów odpowiadających poszczególnym opiniom
                opinions = page_tree.select("div.js_product-review")
                print(len(opinions))
                #ekstrakcja składowyh dla pojedynczej opinii z listy
                for opinion in opinions: 
                    op = Opinion()
                    op.extract_opinion(opinion)
                    opinions_list.append(op)
                try:
                    url = url_prefix+page_tree.select("a.pagination__next").pop()["href"]
                except IndexError:
                    url = None
                print(len(opinions_list))
            self.opinions = opinions_list
            print(len(self.opinions))
    def __repr__(self):
        pass
    def save_product(self):
        pass
        # print(opinions_count)
        # while url is not None:
        #     page_response = requests.get(url)
        #     page_tree = BeautifulSoup(page_response.text, 'html.parser')

        #     opinions = page_tree.select("li.js_product-review")
        #     for opinion in opinions:
            # abs
        #         features = {key:extract_feature(opinion, *args)
        #                     for key, args in selectors.items()}
        #         features["opinion_id"] = int(opinion["data-entry-id"])
        #         features["purchased"] = True if features["purchased"] == "Opinia potwierdzona zakupem" else False
        #         features["useful"] = int(features["useful"])
        #         features["useless"] = int(features["useless"])
        #         features["content"] = remove_whitespaces(features["content"])
        #         try:
        #             features["pros"] = remove_whitespaces(features["pros"])
        #         except:
        #             pass
        #         try:
        #             features["cons"] = remove_whitespaces(features["cons"])
        #         except:
        #             pass
                
        #         opinions_list.append(features)

        #     try:
        #         url = url_prefix+page_tree.select("a.pagination__next").pop()["href"]
        #     except IndexError:
        #         url = None
        

class Opinion:
    #lista składowych opinii wraz z selektorami i atrybutami
    selectors = {
        "author": ['span.user-post__author-name'],
        "recommendation":['span.user-post__author-recomendation > em'],
        "stars":['span.user-post__score-count'],
        "content": ['div.user-post__text'],
        "pros": ['div.review-feature__col:has(div.review-feature__title--positives)'],
        "cons":['div.review-feature__col:has(div.review-feature__title--negatives)'], 
        "useful":['button.vote-yes', "data-total-vote"],
        "useless":['button.vote-no', "data-total-vote"],
        "purchased":['div.review-pz'],
        "purchase_date":['span.user-post__published > time:nth-of-type(1)',"datetime"],
        "review_date":['span.user-post__published > time:nth-of-type(2)',"datetime"]
    }
    #konstruktor (inicjalizator) obiektu klasy
    def __init__(self, opinion_id=None, author=None, recommendation=None, stars=None, content=None, pros=None, cons=None, useful=None, useless=None, purchased=None, purchase_date=None, review_date=None):
        self.opinion_id = opinion_id
        self.author = author
        self.recommendation = recommendation
        self.stars = stars
        self.content = content
        self.pros = pros
        self.cons = cons
        self.useful = useful
        self.useless = useless
        self.purchased = purchased
        self.purchase_date = purchase_date
        self.review_date = review_date
#reprezentacja tekstowa obiektu klasy
    def __str__(self):
        return f'opinion id: {self.opinion_id}\nauthor: {self.author}\npros: {self.pros}\n'

    #reprezentacja słownikowa obiektu
    def __repr__(self):
        pass
    #
    def extract_opinion(self, opinion):
        for key, args in self.selectors.items():
            setattr(self, key, utils.extract_feature(opinion, *args))
        self.opinion_id = int(opinion["data-entry-id"])
        pass
    def transform_opinion(self):
        features["purchased"] = True if features["purchased"] == "Opinia potwierdzona zakupem" else False
        features["useful"] = int(features["useful"])
        features["useless"] = int(features["useless"])
        features["content"] = remove_whitespaces(features["content"])
        features["pros"] = remove_whitespaces(features["pros"])
        features["cons"] = remove_whitespaces(features["cons"])
        pass

    # def extract_opinion(self,opinion):
    #     for key, args in self.selectors.items():
    #         setattr(self, key, utils.extract_feature(opinion,*args))
    #     self.opinion_id = int(opinion["data-entry-id"])
    #     # self.author = utils.extract_feature(opinion, *self.selectors['author'])
        
    #     # features = {key:extract_feature}
    #     pass

    # def transform_opinion(self):
    #     pass

    # def extract_opinion(self, opinion):
    #     selectors = self.selectors
    #     features = {key:utils.extract_feature(opinion, *args)
    #                 for key, args in selectors.items()}
    #     self.opinion_id = int(opinion["data-entry-id"])
    #     pass
    # def transform_opinion(self):
    #     features["purchased"] = True if features["purchased"] == "Opinia potwierdzona zakupem" else False
    #     features["useful"] = int(features["useful"])
    #     features["useless"] = int(features["useless"])
    #     features["content"] = remove_whitespaces(features["content"])
    #     features["pros"] = remove_whitespaces(features["pros"])
    #     features["cons"] = remove_whitespaces(features["cons"])
    #     pass
    # product = Product("39562616")
# opinion = Opinion()
# print(opinion.selectors)
product = Product("79688141")
product.extract_product()
print(product)
    # product.extract_product
    # product = 
    # def __init__(self, *args, **kwargs):
    #     super(CLASS_NAME, self).__init__(*args, **kwargs)