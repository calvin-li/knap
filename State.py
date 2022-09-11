class State:
    def __init__(self):
        self.evs: [int] = []
        self.pvs: [int] = []
        self.name: str = ""
        self.ev_total: int = sum(self.evs)
        self.pv_total: int = sum(self.pvs)

    @staticmethod
    def create_from_html(row, num_evs, num_candidates):
        new_state = State()
        new_state.evs = row[3:3 + num_evs]
        new_state.pvs = row[-num_candidates:]

        def _convert_to_numbers(cell):
            return int(cell.replace(',', ''))

        new_state.evs = [_convert_to_numbers(x) for x in new_state.evs]
        new_state.pvs = [_convert_to_numbers(x) for x in new_state.pvs]

        new_state.name = row[2]
        new_state.ev_total = sum(new_state.evs)
        new_state.pv_total = sum(new_state.pvs)

        return new_state

    @staticmethod
    def create_from_csv(csv_line, num_evs):
        data = csv_line.strip().split(",")
        new_state = State()
        new_state.name = data[0]
        new_state.evs = [int(x) for x in data[1:num_evs+1]]
        new_state.pvs = [int(x) for x in data[1 + num_evs:]]
        new_state.ev_total = sum(new_state.evs)
        new_state.pv_total = sum(new_state.pvs)

        return new_state
