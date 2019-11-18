from NFA import *

def build_eps_closure(nfa, states):
    unchecked_stack = states[:]
    eps_closure = states[:]

    while(len(unchecked_stack) != 0):
        t = unchecked_stack.pop()
        for i in range(len(nfa.transTable[t])):
            if nfa.transTable[t][i] == 'EPS':
                unchecked_stack.append(i)
                if i not in eps_closure:
                    eps_closure.append(i)

    return sorted(eps_closure)


