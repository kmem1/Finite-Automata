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
        new_nfa = NFA(2,0,1)
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

def build_nfa_basic(inp):
    basic = NFA(2,0,1)
    basic.addTrans(0,1,inp)

    return basic

def build_nfa_alter(nfa1, nfa2):
    copy_nfa1 = nfa1.copy()
    copy_nfa2 = nfa2.copy()

    copy_nfa1.shiftStates(1)
    copy_nfa2.shiftStates(copy_nfa1.size)

    new_nfa = copy_nfa2.copy()
    new_nfa.fillStates(copy_nfa1)
    new_nfa.addTrans(0, copy_nfa1.initial, 'EPS')
    new_nfa.addTrans(0, copy_nfa2.initial, 'EPS')
    new_nfa.initial = 0

    new_nfa.appendEmptyState()
    new_nfa.final = new_nfa.size - 1

    new_nfa.addTrans(copy_nfa1.final, new_nfa.final, 'EPS')
    new_nfa.addTrans(copy_nfa2.final, new_nfa.final, 'EPS')

    return new_nfa

def build_nfa_concat(nfa1_c, nfa2_c):
    nfa1 = nfa1_c.copy()
    nfa2 = nfa2_c.copy()

    nfa2.shiftStates(nfa1.size - 1)
    nfa2.fillStates(nfa1)

    new_nfa = nfa2.copy()
    new_nfa.initial = nfa1.initial

    return new_nfa

def build_nfa_star(nfa):
    new_nfa = nfa.copy()

    new_nfa.shiftStates(1)
    new_nfa.appendEmptyState()

    new_nfa.addTrans(0, new_nfa.initial, 'EPS')
    new_nfa.addTrans(0, new_nfa.size - 1, 'EPS')
    new_nfa.addTrans(new_nfa.final, new_nfa.initial, 'EPS')
    new_nfa.addTrans(new_nfa.final, new_nfa.size - 1, 'EPS')

    new_nfa.initial = 0
    new_nfa.final = new_nfa.size - 1

    return new_nfa
