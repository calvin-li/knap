import requests

from main import START_YEAR, END_YEAR

for year in range(START_YEAR, END_YEAR + 4, 4):
    url = f"https://uselectionatlas.org/RESULTS/data.php?year={year}&datatype=national&def=1&f=0&off=0&elect=0"
    request = requests.get(url)
    with open(f"raw_data/{year}.html", "w") as file:
        file.write(request.content.decode())
        print(f"Downloaded {year}")
