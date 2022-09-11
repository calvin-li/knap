from State import State


class Election:
    def __init__(self):
        self.year: int = 0
        self.num_evs: int = 0
        self.candidates: [str] = []
        self.states: [State] = []

    @staticmethod
    def create_from_html(year, datatable):
        new_election = Election()
        new_election.year = year

        header = datatable.find("thead").find("tr")
        header = Election.get_cell_text(header)
        first_candidate = header.index("Other") + 1

        new_election.num_evs = header.count("EV")
        new_election.candidates = header[first_candidate:]
        new_election.states = new_election.extract_state_info(datatable)

        return new_election

    @staticmethod
    def get_cell_text(row):
        return [x.text for x in row.find_all("td")]

    def extract_state_info(self, datatable):
        rows = datatable.tbody.find_all("tr")
        cells = [self.get_cell_text(s) for s in rows]
        states = [State.create_from_html(s, self.num_evs, len(self.candidates)) for s in cells]

        return states

    @staticmethod
    def create_from_csv(year, csv_lines):
        new_election = Election()

        new_election.year = year

        header = csv_lines[0].strip().split(",")
        new_election.num_evs = len([x for x in header if x.startswith("EV")])
        new_election.candidates = header[new_election.num_evs+1:]
        new_election.states = [State.create_from_csv(x, new_election.num_evs) for x in csv_lines[1:]]

        return new_election
