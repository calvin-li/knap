import requests
import json

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
    start = 1824
    end = 2020
    elections = []
    for year in range(start, end + 4, 4):
        with open(f"csv_data/{year}.csv", "r") as csv:
            elections.append(Election.create_from_csv(year, csv.readlines()))

        """ commenting out; already done
        elections.append(extract_from_html(year))
        """

    reports = []
    for election in elections:
        reports.append(election.knapsack_solve())
        """
        to_csv(election)
        """

    for report in reports:
        to_json(report)
        print(json.dumps(report, indent=4))

    with open("reports/all.json", "w") as all_file:
        all_file.write(json.dumps(reports, indent=4))

    return


def extract_from_html(year):
    with open(f"raw_data/{year}.html") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")
    datatable = soup.find(is_datatable)
    return Election.create_from_html(year, datatable)


def to_csv(election: Election):
    with open(f"csv_data/{election.year}.csv", "w") as csv:
        evs = ["EV"] * election.num_evs
        for i in range(2):
            evs[i] += f"-{election.candidates[i]}"
        csv.write(f"State,{','.join(evs)},{','.join(election.candidates)}")
        for state in election.states:
            ev_string = ",".join([str(x) for x in state.evs])
            pv_string = ",".join([str(x) for x in state.pvs])
            csv.write(f"\n{state.name},{ev_string},{pv_string}")


def to_json(report):
    with open(f"reports/{report['year']}.json", "w") as json_file:
        json_file.write(json.dumps(report, indent=4))


if __name__ == '__main__':
    main()

