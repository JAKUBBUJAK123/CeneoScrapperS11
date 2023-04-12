import requests
from bs4 import BeautifulSoup
import json

def get_cos(ancestor, selector = None , attribute =  None , return_list = False) :
    try:
        if return_list:
             [tag.text.strip() for tag in ancestor.select(selector)].copy()
        if not selector and attribute:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except AttributeError:
        return None


selectors = {
        "opinion_id": [ None , "data-entry-id"],
        "author": ["span.user-post__author-name"],
        "recommentadion": [ "span.user-post__author-recomendation"],
        "score": ["span.user-post__score-count"],
        "purhased": ["div.review-pz"],
        "published_at": ["span.user-post__published > time:nth-child(1)" , ],
        "purhased_at": ["span.user-post__published > time:nth-child(2)" , ] ,
        "thumbs_up": ["button.vote-yes > span"],
        "thumbs_down": ["button.vote-no > span"],
        'content': ['div.user-post__text'],
        'pros' : ["div.review-feature__col:has(> div.review-feature__title--positives) > div.review-feature__item" ,None , True],
        'cons' : ["div.review-feature__col:has(> div.review-feature__title--negatives) > div.review-feature__item" , None, True],
    }


# product_code = input("Podaj kod produtu")
product_code = "96685108"
page_no = 1
al_opinions = []
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
while(url):
    
    print(url)
    response = requests.get(url, allow_redirects=False)
    
    
    page = BeautifulSoup(response.text, "html.parser")
    opinions = page.select("div.js_product-review")


#opinion_id = ["data-entry-id"]
#author = "span.user-post__author-name"
#recommentadion = "span.user-post__source-count"
#score = "span.user-post__score-count"
#purhased = "div.reviev-pz"
#published_at = 'span.user-post__published > time:nth-child(1)["datetime"]'
#purhased_at = 'span.user-post__published > time:nth-child(2)["datetime]'
#thumbs_up = "span[id^=votes-yes]"
#content = "div.user-post__text"

    
    for opinion in opinions:
        single_option = {}
        for key, value in selectors.items():
            single_option[key] = get_cos(opinion, *value)

        al_opinions.append(single_option)
    
    url = f"https://www.ceneo.pl" + get_cos(page, 'a.pagination__next' , 'href')
print(len(al_opinions))


with open(f"./opinions/{product_code}.json" , 'w' , encoding='utf-8') as jf:
    json.dump(al_opinions, jf, indent=4 , ensure_ascii=False)
print(json.dumps(al_opinions , indent=4 , ensure_ascii=False))
