import requests
import bs4
from http import HTTPStatus

TESTING = True


def get_html_from_url(url: str) -> bytes:
    req_data = requests.get(url)
    if int(req_data.status_code / 100) >= 4:
        print(f"Error: {req_data.status_code}")
        raise Exception

    return req_data.content


def main() -> None:
    global TESTING
    url = "https://manhuaus.com/manga/player-who-returned-10000-years-later/"

    if TESTING:
        with open("test.txt", "rb") as file:
            raw_html = file.read()
    else:
        raw_html = get_html_from_url(url)
    soup = bs4.BeautifulSoup(raw_html, "lxml")

    items = soup.find_all("li", {"class": "wp-manga-chapter"})
    print(len(items))
    print(items[0].a.text)


if __name__ == "__main__":
    main()
