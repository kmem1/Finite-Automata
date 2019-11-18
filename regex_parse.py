import NFA

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


my_scanner = Scanner()

class ParseNode:
    def __init__(self, type_, data_, left_, right_):
        self.type = type_
        self.data = data_
        self.left = left_
        self.right = right_

def chr_():
    data = my_scanner.peek()

    if(data.isalnum() or data == 0):
        return ParseNode('CHR', my_scanner.pop(), 0, 0)

    raise Exception

def _preprocess(data):
    out = ''

    c = data[0]
    up = data[1]

    for i,j in zip(range(len(data) - 1), range(1,len(data))):
        c = data[i]
        up = data[j]

        out += c

        if((c.isalnum() or c == ')' or c == '*' or c == '?') and
            (up != ')' and up != '|' and up != '*' and up != '?')):
            out += '.'

    if c != data[-1]:
        out += up

    return out

def _chr():
    data = my_scanner.peek()
    
    if data.isalnum() or data == 0:
        return ParseNode('CHR', my_scanner.pop(),0,0)
    
    raise Exception

def _atom():
    atom_node = ParseNode()
    
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
    

