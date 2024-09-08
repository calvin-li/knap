import json


def all_to_csv():
    with open("reports/all.json", "r") as all_file:
        data = json.loads(all_file.read())

    csv = [",".join([
        "year",
        "original winner",
        "new winner",
        "flipped votes",
        "total votes",
        "percent votes flipped",
        "flipped states"
    ])]

    for d in data:
        row_data = [
            d["year"],
            d["original winner"],
            d["new winner"],
            d["flipped votes"],
            d["total votes"],
            d["percent votes flipped"]
        ]

        flipped_states = d["flipped states"]
        flipped_states = [f"{k}:{v}" for k, v in flipped_states.items()]
        row_data.append(";".join(flipped_states))

        csv.append(",".join([str(x) for x in row_data]))

    with open("all.csv", "w") as fp:
        fp.write("\n".join(csv))


if __name__ == '__main__':
    all_to_csv()
