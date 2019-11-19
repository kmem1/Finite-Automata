class DFA:
    def __init__(self):
        # {state: {input: state1 from state by input}} - example of transition table with one element
        self.transTable = {}
        self.start = 0
        self.final = []

    def simulate(self, input):
        cur_state = self.start
        for i in input:
            if (cur_state not in self.transTable) or (i not in self.transTable[cur_state]):
                return 'REJECT'

            cur_state = self.transTable[cur_state][i]

        if cur_state in self.final:
            return 'ACCEPT'
        else:
            return 'REJECT'

    def show(self):
        print('DFA start state: ', self.start)
        print('DFA final state(s): ', self.final)
        print('Transitions: ')
        for trans in self.transTable:
            for input in self.transTable[trans]:
                print('[', trans, ',', input, '] =', self.transTable[trans][input])

if __name__ == '__main__':
    dfa = DFA()
    dfa.transTable = {3: {'i': 5, 'a': 4}, 4: {'b': 7}}
    dfa.start = 3
    dfa.final = [7]
    dfa.show()