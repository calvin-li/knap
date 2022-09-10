class State:
    def __init__(self, row, num_evs):
        self.evs = row[3:3+num_evs]
        self.pvs = row[-num_evs - 1:]

        def _convert_to_numbers(cell):
            return int(cell.replace(',', ''))

        self.evs = [_convert_to_numbers(x) for x in self.evs]
        self.pvs = [_convert_to_numbers(x) for x in self.pvs]

        self.name = row[2]
        self.ev_total = sum(self.evs)
        self.pv_total = sum(self.pvs)

