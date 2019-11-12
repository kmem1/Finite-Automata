class NFA:
    def __init__(self, size, initial_s, final_s):
        self.size = size
        self.inputs = []
        if not (self.isLegalState(initial_s) and self.isLegalState(final_s)):
            raise Exception('StateError: state must be in range(0,size-1)')
        self.initial = initial_s
        self.final = final_s
        self.transTable = []
        for i in range(size):
            self.transTable.append([None for s in range(size)])

    def copy(self):
        new_nfa = NFA(0,0,0)
        new_nfa.size = self.size
        new_nfa.initial = self.initial
        new_nfa.final = self.final
        new_nfa.transTable = self.transTable
        return new_nfa

    def isLegalState(self, s):
        if s < 0 or s >= self.size:
            return False
        else:
            return True

    def addTrans(self, from_s, to_s, input_ch):
        if not (self.isLegalState(from_s) and self.isLegalState(to_s)):
            raise Exception('StateError: state must be in range(0,size-1)')
        self.transTable[from_s][to_s] = input_ch
        if input_ch != 'EPS':
            self.inputs.append(input_ch)

    def shiftStates(self, shift):
        if shift < 1:
            return self
        newSize = self.size + shift
        newTransTable = [[None for i in range(newSize)] for i in range(newSize)]

        for i in range(self.size):
            for j in range(self.size):
                newTransTable[i+shift][j+shift] = self.transTable[i][j]

        self.size = newSize
        self.initial += shift
        self.final += shift
        self.transTable = newTransTable

    def fillStates(self,other):
        for i in range(other.size):
            for j in range(other.size):
                self.transTable[i][j] = other.transTable[i][j]

        for i in other.inputs:
            if i not in self.inputs:
                self.inputs.append(i)

    def appendEmptyState(self):
        self.transTable.append([None for i in range(self.size + 1)])

        for i in range(self.size):
            self.transTable[i].append(None)

        self.size += 1

    def show(self):
        print('This NFA has {0} states: 0 - {1}'.format(self.size,self.size - 1))
        print('The initial state is {0}'.format(self.initial))
        print('The final state is {0}'.format(self.final))

        for from_s in range(self.size):
            for to_s in range(self.size):
                i = self.transTable[from_s][to_s]
                print('Transition from {0} to {1} on input {2}'.format(from_s,to_s,i))

    def move(self, states, input_c):
        result = []
        for state in states:
            for i in range(self.size):
                if self.transTable[state][i] == input_c:
                    if i not in result:
                        result.append(i)
        return result


if __name__ == "__main__":
    nfa = NFA(2,0,1)
    nfa.addTrans(0,1,'a')
    nfa.shiftStates(1)
    nfa1 = NFA(2,0,1)
    nfa1.addTrans(0,1,'b')
    nfa.fillStates(nfa1)
    nfa.appendEmptyState()
    nfa.addTrans(0,2,'a')
    nfa.show()
    print(nfa.move([0,1],'a'))
