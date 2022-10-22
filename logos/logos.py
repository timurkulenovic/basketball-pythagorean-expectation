# script to download teams logos
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
from PIL import Image

wiki = "https://en.wikipedia.org"
games = pd.read_csv("../data/euroleague_games.csv")
teams = games["H_Team"].unique()
print("Total of:", len(teams))


def write_from_url_to_file(url, team, size=100):
    format_ = url.split(".")[-1]
    filename = f'img/{team.replace(" ", "_")}.{format_}'
    urllib.request.urlretrieve(f"https:{url}", filename)

    image = Image.open(filename)
    width, height = image.size
    new_width, new_height = 0, 0
    if width >= height:
        ratio = width / height
        new_height = size
        new_width = int(ratio * size)
    elif height > width:
        ratio = height / width
        new_width = size
        new_height = int(ratio * size)

    img_resized = image.resize((new_width, new_height))
    img_resized.save(filename)


def exceptions(team):
    exceptions_dict = {
        "Barcelona": "//pngimg.com/uploads/fcb_logo/fcb_logo_PNG25.png",
        "Rhein": "//www.rheinstars-koeln.de/wp-content/themes/enfold-child/assets/img/logo_rheinstars_navigation.png",
        "Cibona": "//upload.wikimedia.org/wikipedia/en/3/3a/KK_Cibona_logo.png",
        "Caja Laboral": "//upload.wikimedia.org/wikipedia/en/6/6a/Saski_Baskonia.png",
        "Lottomatica Roma": "//upload.wikimedia.org/wikipedia/en/5/5a/Virtus_Roma_logo.png"
    }

    key = next((key for key in exceptions_dict.keys() if key in team), None)
    if key is not None:
        write_from_url_to_file(exceptions_dict[key], team)
        return True
    else:
        return False


def download_image(team, string="basketball"):
    if not exceptions(team):
        team_search = f'{team.replace(" ", "+")}+{string}'
        team_search_link = f"{wiki}/w/index.php?go=Go&search={team_search}&title=Special:Search&ns0=1"
        res = requests.get(team_search_link)
        bs_res = BeautifulSoup(res.text, "html.parser")
        if bs_res.find("div", {"class": "mw-search-result-heading"}):
            href_article = bs_res.find("div", {"class": "mw-search-result-heading"}).find("a").get("href")
            article = requests.get(f"{wiki}{href_article}")
            bs_article = BeautifulSoup(article.text, "html.parser")
        else:
            bs_article = bs_res

        if bs_article.find("td", {"class": "infobox-image"}):
            href_img = bs_article.find("td", {"class": "infobox-image"}).find("a").find("img").get("src")
            write_from_url_to_file(href_img, team)
        elif string == "basketball":
            download_image(team, string="")
        else:
            print("Cant download")
            exit(0)


for i, team_i in enumerate(teams):
    print(i, team_i)
    download_image(team_i)
