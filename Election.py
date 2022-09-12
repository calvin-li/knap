from math import inf

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

    def knapsack_solve(self):
        """
        Finds minimum number of popular votes needed for #2 by EV to get majority
        """
        if self.year == 1876:
            self.states.append(State.create_from_csv("Colorado,3,0,0,0", 2))

        class Item:
            def __init__(self, name, weight, value):
                self.name = name
                self.weight = weight
                self.value = value

        winner_index = 0
        ru_index = ru_ev_index = 1
        if self.year == 1824:
            """1824 was weird/stolen"""
            winner_index = 1
            ru_index = ru_ev_index = 0
        elif self.year in [1876, 1888, 2000, 2016]:
            """Winning candidate did not win popular vote"""
            winner_index = 1
            ru_index = 0

        winner = self.candidates[winner_index]
        runner_up = self.candidates[ru_index]

        total_pvs = total_evs = ru_evs = 0
        items = []

        for state in self.states:
            total_pvs += state.pv_total
            total_evs += state.ev_total
            ru_evs += state.evs[ru_ev_index]

            state_winning_pvs = max(state.pvs)
            state_winner_index = state.pvs.index(state_winning_pvs)
            ru_didnt_win = state.evs[ru_ev_index] == 0 and ru_index != state_winner_index
            pv_state = state.pv_total > 0

            if pv_state and ru_didnt_win:
                ru_pvs = state.pvs[ru_index]
                pv_short = (state_winning_pvs - ru_pvs)//2 + 1

                items.append(
                    Item(
                        state.name,
                        pv_short,
                        state.ev_total
                    ))

        evs_short = total_evs//2 + 1 - ru_evs

        if len(items) == 0:
            print(f"something weird happened in {self.year}")
            return None

        return self._solve(items, evs_short)

    @staticmethod
    def _solve(items, target_value):
        total_weight = sum([i.weight for i in items])
        dp_table = []
        ans_table = []
        for _ in range(len(items)):
            dp_table.append([inf] * target_value)
            ans_table.append([set()] * target_value)

        for i, item in enumerate(items):
            for j in range(target_value):
                if i == 0:
                    if j < item.value:
                        dp_table[i][j] = item.weight
                        ans_table[i][j] = {(item.name, item.weight)}
                else:
                    weight_using_item = item.weight + (0 if j < item.value else dp_table[i-1][j-item.value])
                    names_using_item = {(item.name, item.weight)}
                    if j >= item.value:
                        names_using_item = names_using_item.union(ans_table[i - 1][j - item.value])
                    weight_not_using_item = dp_table[i-1][j]

                    if weight_not_using_item < weight_using_item:
                        dp_table[i][j] = weight_not_using_item
                        ans_table[i][j] = ans_table[i-1][j]
                    else:
                        dp_table[i][j] = weight_using_item
                        ans_table[i][j] = names_using_item

                    dp_table[i][j] = min(dp_table[i-1][j], weight_using_item)

        return dp_table[-1][-1], ans_table[-1][-1]
