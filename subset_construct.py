from NFA import *
from DFA import *


def build_eps_closure(nfa, states):
    unchecked_stack = []
    eps_closure = []
    try:
        unchecked_stack = states[:]
        eps_closure = states[:]
    except TypeError:
        unchecked_stack.append(states)
        eps_closure.append(states)

    while (len(unchecked_stack) != 0):
        t = unchecked_stack.pop()
        for i in range(len(nfa.transTable[t])):
            if nfa.transTable[t][i] == 'EPS':
                unchecked_stack.append(i)
                if i not in eps_closure:
                    eps_closure.append(i)

    return sorted(eps_closure)


def init_state_func():
    next = -1

    def gen_new_state():
        nonlocal next
        next += 1
        return next

    return gen_new_state


gen_new_state = init_state_func()

def get_key(dict, value):
    res = None
    for key,val in dict.items():
        if val == value:
            res = key
    return res

def subset_construct(nfa):
    dfa = DFA()
    checked_states = []

    marked_states = []
    unmarked_states = []

    dfa_state_num = {}

    first = build_eps_closure(nfa, nfa.initial)
    unmarked_states.append(first)

    dfa_initial = gen_new_state()
    dfa_state_num[dfa_initial] = first
    dfa.start = dfa_initial

    while(len(unmarked_states) != 0):
        a_state = unmarked_states.pop()
        marked_states.append(a_state)

        try:
            for state in a_state:
                if state == nfa.final:
                    dfa.final.append(get_key(dfa_state_num, a_state))
        except TypeError:
            if a_state == nfa.final:
                dfa.final.append(get_key(dfa_state_num, a_state))

        for i in nfa.inputs:
            next = build_eps_closure(nfa, nfa.move(a_state, i))

            if (next not in unmarked_states) and (next not in marked_states):
                unmarked_states.append(next)
                dfa_state_num[gen_new_state()] = next

            if get_key(dfa_state_num, a_state) in checked_states:
                dfa.transTable[get_key(dfa_state_num, a_state)][i] = get_key(dfa_state_num, next)
            else:
                checked_states.append(get_key(dfa_state_num, a_state))
                dfa.transTable[get_key(dfa_state_num, a_state)] = {}
                dfa.transTable[get_key(dfa_state_num, a_state)][i] = get_key(dfa_state_num, next)

    return dfa