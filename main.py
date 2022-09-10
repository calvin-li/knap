import requests

from bs4 import BeautifulSoup

from Election import Election


def get_data(year):
    url = f"https://uselectionatlas.org/RESULTS/data.php?year={year}&datatype=national&def=1&f=0&off=0&elect=0"
    request = requests.get(url)
    with open(f"raw_data/{year}.html", "w") as file:
        file.write(request.content.decode())
        print(f"Downloaded {year}")


def is_datatable(tag):
    if tag.name == "table":
        return "id" in tag.attrs and tag.attrs["id"].startswith("datatable")


def main():
    elections = []
    start = 1824
    end = 2020
    for year in range(start, end + 4, 4):
        with open(f"raw_data/{year}.html") as file:
            html = file.read()

        soup = BeautifulSoup(html, "html.parser")
        datatable = soup.find(is_datatable)
        election = Election(datatable)
        elections.append(election)

    return


if __name__ == '__main__':
    main()

