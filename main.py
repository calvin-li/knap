import requests
from bs4 import BeautifulSoup


def get_data(year):
    url = f"https://uselectionatlas.org/RESULTS/data.php?year={year}&datatype=national&def=1&f=0&off=0&elect=0"
    request = requests.get(url)
    with open(f"raw_data/{year}.html", "w") as file:
        file.write(request.content.decode())
        print(f"Downloaded {year}")


def extract_table(year):
    html = []
    with open(f"raw_data/{year}.html") as file:
        html = file.read()

    print(html)


def main():
    start = 1824
    end = 2020
    for year in range(start, end + 4, 4):
        extract_table(year)
        return


if __name__ == '__main__':
    main()

