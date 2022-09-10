from State import State


class Election:
    def __init__(self, datatable):
        header = datatable.find("thead").find("tr")
        header = Election.get_cell_text(header)
        self.num_candidates = header.count("EV")
        self.candidates = header[-self.num_candidates-1:-1]
        self.states = self.extract_state_info(datatable)

    @staticmethod
    def get_cell_text(row):
        return [x.text for x in row.find_all("td")]

    def extract_state_info(self, datatable):
        rows = datatable.tbody.find_all("tr")
        cells = [self.get_cell_text(s) for s in rows]
        states = [State(s, self.num_candidates) for s in cells]

        return states
