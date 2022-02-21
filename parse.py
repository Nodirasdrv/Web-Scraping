import requests
from bs4 import BeautifulSoup
import csv


URL = "https://cars.kg/offers/?vendor=57fa24ee2860c45a2a2c08e0"

HEADERS = {
    "user-agent": "Mozilla/5.0 (Macintosh;"
                  " Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/98.0.4758.102 Safari/537.36",
    "accept": "*/*",
}
DOMEN = "https://cars.kg/"


def get_html(url, params=None):
    request = requests.get(url=url,
                           headers=HEADERS,
                           params=params)

    return request


def get_content_page(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("a", class_="catalog-list-item")
    cars = []
    for item in items:
        cars.append(
            {
                "title": item.find("span",
                                   class_="catalog-item-caption").get_text().replace("\n", ""),
                "description": item.find("span",
                                         class_="catalog-item-descr").get_text(),
                "mileage": item.find("span", class_="catalog-item-mileage").get_text(),
                "image": DOMEN + item.find("img").get("src"),
                "price": int(item.find("span",
                                       class_="catalog-item-price").get_text().replace("$", "")) * 84,

            }
        )
    return cars


def download_csv(washing_car):
    with open("cars_list.csv", "w") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Название", "Описание", "Картинка", "Цена", "Пробег"])
        for car in washing_car:
            writer.writerow([car["title"], car["description"],
                             car["image"], car["price"], car["mileage"]]
                            )


def parse_cars():
    html_ = get_html(URL)

    if html_.status_code == 200:
        washing_car = get_content_page(html_.text)
        download_csv(washing_car)
    else:
        print("connect error")


parse_cars()

