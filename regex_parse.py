from NFA import *
from subset_construct import *

class Scanner:
    def init(self, data_):
        self.data = _preprocess(data_)
        self.next = 0

    def peek(self):
        return self.data[self.next] if self.next < len(self.data) else 0

    def pop(self):
        cur = self.peek()
        if( self.next < len(self.data) ):
            self.next += 1
        return cur

    def get_pos(self):
        return self.next

# global scanner
my_scanner = Scanner()

class ParseNode:
    def __init__(self, type_, data_, left_, right_):
        self.type = type_
        self.data = data_
        self.left = left_
        self.right = right_

def _preprocess(data):
    out = ''

    c = data[0]
    up = data[1]
    k = 0

    for i,j in zip(range(len(data) - 1), range(1,len(data))):
        c = data[i]
        up = data[j]
        k = i

        out += c

        if((c.isalnum() or c == ')' or c == '*' or c == '?') and
            (up != ')' and up != '|' and up != '*' and up != '?')):
            out += '.'

    if k != len(data):
        out += up

    return out

def print_tree(node, offset):
    if node == 0:
        return

    print(' ' * offset, end='')

    type_ = node.type
    if type_ == 'CHR':
        print(node.data)
    elif type_ == 'ALTER':
        print('|')
    elif type_ == 'CONCAT':
        print('.')
    elif type_ == 'QUESTION':
        print('?')
    elif type_ == 'STAR':
        print('*')

    print_tree(node.left, offset + 4)
    print_tree(node.right, offset + 4)

def tree_to_nfa(tree):
    type_ = tree.type
    if type_ == 'CHR':
        return build_nfa_basic(tree.data)
    elif type_ == 'ALTER':
        return build_nfa_alter(tree_to_nfa(tree.left), tree_to_nfa(tree.right))
    elif type_ == 'CONCAT':
        return build_nfa_concat(tree_to_nfa(tree.left), tree_to_nfa(tree.right))
    elif type_ == 'QUESTION':
        return build_nfa_alter(tree_to_nfa(tree.left), build_nfa_basic('EPS'))
    elif type_ == 'STAR':
        return build_nfa_star(tree_to_nfa(tree.left))

#Parser
def _chr():
    data = my_scanner.peek()
    
    if data == 0 or data.isalnum():
        return ParseNode('CHR', my_scanner.pop(),0,0)
    
    raise Exception

def _atom():
    atom_node = ParseNode('CHR', my_scanner.peek(), 0,0)
    
    if my_scanner.peek() == '(':
        my_scanner.pop()
        atom_node = _expr()
        
        if my_scanner.pop() != ')':
            raise Exception("Need ')' ")
            
    else:
        atom_node = _chr()
    
    return atom_node

def _rep():
    atom_node = _atom()
    
    if my_scanner.peek() == '*':
        my_scanner.pop()
        return ParseNode('STAR', 0, atom_node, 0)
    elif my_scanner.peek() == '?':    
        my_scanner.pop()
        return ParseNode('QUESTION', 0, atom_node, 0)
    else:
        return atom_node

def _concat():
    left = _rep()
    
    if my_scanner.peek() == '.':
        my_scanner.pop()
        right = _concat()
        return ParseNode('CONCAT', 0, left, right)
    else:
        return left
        
def _expr():
    left = _concat()

    if my_scanner.peek() == '|':
        my_scanner.pop()
        right = _expr()
        return ParseNode('ALTER', 0, left, right)
    else:
        return left
    
if __name__ == '__main__':
    my_scanner.init('(a|b)*abb')

    n = _expr()
    if my_scanner.peek() != 0:
        raise Exception('Parse error: unexpected char')

    nfa = tree_to_nfa(n)
    dfa = subset_construct(nfa)
    print(dfa.simulate('abababababbbabb'))