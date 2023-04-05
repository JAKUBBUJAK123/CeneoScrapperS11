import requests
from bs4 import BeautifulSoup


def get_cos(ancestor,selector = None , attribute =  None , return_list = False) :
    try:
        if return_list:
             [tag.text.strip() for tag in ancestor.select(selector)].copy()
        if not selector:
            return ancestor[attribute]
        if attribute:
            return ancestor.select_one(selector)[attribute].strip()
        return ancestor.select_one(selector).text.strip()
    except AttributeError:
        return None



# product_code = input("Podaj kod produtu")
product_code = "96685108"
url = f"https://www.ceneo.pl/{product_code}#tab=reviews"
response = requests.get(url)
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

al_opinions = []
for opinion in opinions:
    print(opinion["data-entry-id"])
    single_option = {
        "opinion_id": opinion["data-entry-id"],
        "author": opinion.select_one("span.user-post__author-name").text.strip(),
        "recommentadion": opinion.select_one("span.user-post__author-recomendation").text.strip(),
        "score": opinion.select_one("span.user-post__score-count").text.strip(),
        "purhased": opinion.select_one("div.review-pz").text.strip(),
        "published_at": opinion.select_one("span.user-post__published > time:nth-child(1)")['datetime'].strip(),
        "purhased_at": opinion.select_one("span.user-post__published > time:nth-child(2)")['datetime'].strip(),
        "thumbs_up": opinion.select_one("button.vote-yes > span").text.strip(),
        "thumbs_down": opinion.select_one("button.vote-no > span").text.strip(),
        'content': opinion.select_one('div.user-post__text').text.strip(),
        'pros' : [pros.text.strip() for pros in opinion.select("div.review-feature__col:has(> div.review-feature__title--positives) > div.review-feature__item")],
        'cons' : [cons.text.strip() for cons in opinion.select("div.review-feature__col:has(> div.review-feature__title--negatives) > div.review-feature__item")],
    }

    al_opinions.append(single_option)

print(al_opinions)
