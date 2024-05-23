# HW3
# REMINDER: The work in this assignment must be your own original work and must be completed alone.

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        # YOUR CODE STARTS HERE
        return len(self) == 0

    def __len__(self): 
        # YOUR CODE STARTS HERE
        current = self.top
        length = 0
        while current:
            length += 1
            current = current.next
        return length

    def push(self,value):
        # YOUR CODE STARTS HERE
        newNode = Node(value)
        newNode.next = self.top
        self.top = newNode

     
    def pop(self):
        # YOUR CODE STARTS HERE
        if self.isEmpty():
            return None
        else:
            value = self.top.value
            self.top = self.top.next
            return value

    def peek(self):
        # YOUR CODE STARTS HERE
        if not self.isEmpty():
            return self.top.value
        else:
            return None


#=============================================== Part II ==============================================

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        # YOUR CODE STARTS HERE
        try:
            float(txt)
            return True
        except ValueError:
            return False

    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack object for expression processing

            >>> x=Calculator()
            >>> x._getPostfix('2 ^ 4')
            '2.0 4.0 ^'
            >>> x._getPostfix('2')
            '2.0'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2 * 5.34 + 3 ^ 2 + 1 + 4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( 2.5 )')
            '2.5'
            >>> x._getPostfix('( 2 { 5.0 } )')
            '2.0 5.0 *'
            >>> x._getPostfix(' 5 ( 2 + { 5 + 3.5 } )')
            '5.0 2.0 5.0 3.5 + + *'
            >>> x._getPostfix ('( { 2 } )')
            '2.0'
            >>> x._getPostfix ('2 * ( [ 5 + -3 ] ^ 2 + { 1 + 4 } )')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('[ 2 * ( < 5 + 3 > ^ 2 + ( 1 + 4 ) ) ]')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('( { 2 * { { 5 + 3 } ^ 2 + ( 1 + 4 ) } } )')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2 * < -5 + 3 > ^ 2 + < 1 + 4 >')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('2 * 5 + 3 ^ - 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ( 1 + 4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ( 1 + 4 ]')
            >>> x._getPostfix(' ( 2 * { 5 + 3 ) ^ 2 + ( 1 + 4 ] }')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ) 1 + 4 (')
            >>> x._getPostfix('2 * 5% + 3 ^ + -2 + 1 + 4')
        '''

        # YOUR CODE STARTS HERE
        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        result = ''
        brackets = {'{': '}', '[': ']', '(': ')'}
        operator = ['^', '*', '/', '+', '-']
        precedence = {'^': 4, '*': 3, '/': 3, '+': 2, '-': 2, '(': 1}
        
         # replace brackets and split elements
        replaced_txt = txt.replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')').replace('<', '(').replace('>', ')')
        items = replaced_txt.split()
        
        # count and order brackets and return None if extra brackets left
        stack = []
        opening = '([{'
        closing = ')]}'
        
        for c in txt:
            if c in opening:
                stack.append(c)
            elif c in closing:
                if not stack or brackets[stack.pop()] != c:
                    return None
        if stack:
            return None
        
        # check if operator is in the list of valid operators
        for i in items:
            if not self._isNumber(i) and i not in ['^','*','/','+','-','(',')']: 
                return None

        # check if each operator/operand has the correct successor and expression is valid
        for i in range(len(items) - 1):
            if items[i] not in ['(', ')'] and items[i + 1] not in ['(', ')']:
                if self._isNumber(items[i]) == self._isNumber(items[i + 1]):
                    return None
                        
        # check other order test cases for brackets now
        if self._check_bracket_closings(items):
            for i in range(len(items)-1):
                current = items[i]
                if self._isNumber(current):
                    if items[i+1] == '(':
                        items.insert(i+1, '*')
                elif current == ')' and items[i+1] == '(':
                    items.insert(i+1, '*')
                elif current == ')' and self._isNumber(items[i+1]):
                    items.insert(i+1, '*')

            for item in items:
                if self._isNumber(item):
                    result += f"{float(item)} "
                elif item == '(':
                    postfixStack.push(item)
                elif item == ')':
                    while not postfixStack.isEmpty() and postfixStack.peek() != '(':
                        result += f"{postfixStack.pop()} "
                                
                    if not postfixStack.isEmpty() and postfixStack.peek() == '(':
                        postfixStack.pop()
                    else:
                        return None
                            
                elif item in precedence:
                    while not postfixStack.isEmpty() and postfixStack.peek() != '(' and precedence[item] <= precedence[postfixStack.peek()] and item != '^':
                        result += f"{postfixStack.pop()} "
                    postfixStack.push(item)
                else:
                    return None  # unsupported operator
                
            while not postfixStack.isEmpty():
                if postfixStack.peek() == '(' or postfixStack.peek() == '[' or postfixStack.peek() == '{' :
                    return None  # missing right parenthesis
                elif postfixStack.peek() == ')' or postfixStack.peek() == ']' or postfixStack.peek() == '}':
                    return None  # missing left parenthesis
                elif postfixStack.peek() in brackets.values():
                    return None # Mismatched brackets 
                elif postfixStack.peek() in operator and self._isNumber(result):
                    return None # one operator and one integer value, return None
                result += f"{postfixStack.pop()} "

                
            while not postfixStack.isEmpty():
                if postfixStack.peek() in brackets.values():
                    result += f"{postfixStack.pop()} "
                
            return result.strip()

    def _check_bracket_closings(self, op_list):
        
        dict1 = {}
        brackets = ['(', ')', '[', ']', '{', '}', '<', '>']
        
        for char in brackets:
            dict1[char] = 0
            
        for char in op_list:
            if char in dict1:
                dict1[char] += 1
        
        for i in range(0, len(brackets), 2):
            if dict1[brackets[i]] != dict1[brackets[i+1]]:
                return False
            
        return True

    @property
    def calculate(self):
        '''
            calculate must call _getPostfix
            calculate must create and use a Stack object to compute the final result as shown in the video lectures
            

            >>> x=Calculator()
            >>> x.setExpr('4 + 3 - 2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 + 3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('4 + 3.65 - 2 / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25 * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr(' 2 - 3 * 4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7 ^ 2 ^ 3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ( [ ( 10 - 2 * 3 ) ] )')
            >>> x.calculate
            12.0
            >>> x.setExpr('8 / 4 * { 3 - 2.45 * [ 4 - 2 ^ 3 ] } + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * [ 4 + 2 * < 5 - 3 ^ 2 > + 1 ] + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 + 3 * ( 2 + { 3.0 } * ( 5 ^ 2 - 2 * 3 ^ ( 2 ) ) * < 4 > ) * [ 2 / 8 + 2 * ( 3 - 1 / 3 ) ] - 2 / 3 ^ 2')
            >>> x.calculate
            1442.7777777777778
            >>> x.setExpr('( 3.5 ) [ 15 ]') 
            >>> x.calculate
            52.5
            >>> x.setExpr('3 { 5 } - 15 + 85 [ 12 ]') 
            >>> x.calculate
            1020.0
            >>> x.setExpr("( -2 / 6 ) + ( 5 { ( 9.4 ) } )") 
            >>> x.calculate
            46.666666666666664
            

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            >>> x.setExpr(" 4 + + 3 + 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 + 2")
            >>> x.calculate
            >>> x.setExpr('( ( 2 ) * 10 - 3 * [ 2 - 3 * 2 ) ]')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * ( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( * 10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
        '''

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None
        
        operator = ['^', '*', '/', '+', '-']
        calcStack = Stack()   # method must use calcStack to compute the expression
        result = self._getPostfix(self.__expr)
        if self._getPostfix(self.__expr) == None:
            return None


        for item in result.split():
            if self._isNumber(item):
                calcStack.push(float(item))
            elif item in operator:
                if len(calcStack) < 2:
                    return None
                operand2 = calcStack.pop()
                operand1 = calcStack.pop()
                if item == '^':
                    result = operand1 ** operand2
                elif item == '*':
                    result = operand1 * operand2
                elif item == '/':
                    result = operand1 / operand2
                elif item == '+':
                    result = operand1 + operand2
                elif item == '-':
                    result = operand1 - operand2
                else:
                    return None
                calcStack.push(result)

        if len(calcStack) == 1:
            return calcStack.pop()
        else:
            return None

#=============================================== Part III ==============================================

class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 [ x1 - 1 ];x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 [ x1 - 1 ]': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 [ x1 - 1 ]': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * { x1 / 2 };x1 = x2 * 7 / x1;return x1 ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * { x1 / 2 }': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        # YOUR CODE STARTS HERE
        if isinstance(word, str):
            return word.isalnum() and word[0].isalpha() and word  != ''

    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 ( x1 - 1 )')
            '7 ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        # YOUR CODE STARTS HERE
        #check self.states and awap values 
        opsbrackets = "{}<>[]()*^+/-"
        items = expr.split()
        
        for i in range(len(items)):
            item = items[i]
            if item not in opsbrackets:
                try:
                    # check valid number
                    float(item)
                except ValueError:
                    # check valid numeric expression
                    if '.' in item:
                        try:
                            # evaluate the item
                            eval(item, {}, {})
                        except:
                            if item in self.states:
                                items[i] = str(self.states[item])
                            else:
                                return None
                    elif item in self.states:
                        items[i] = str(self.states[item])
                    else:
                        return None

        return " ".join(items)

    
    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression
        # YOUR CODE STARTS HERE
        if not isinstance(self.expressions, str):
            return None

        result = {}
        for expr in self.expressions.split(';'):
            if 'return' in expr:
                expr_value = self._replaceVariables(expr.replace('return', ''))
                if expr_value is None:
                    return {}
                calcObj.setExpr(expr_value)
                cal_value = calcObj.calculate
                    
                if cal_value is None:   
                    return {}
                result['_return_'] = cal_value
                    
            else:
                leftv, rightv = expr.split('=')
                rightvalue = self._replaceVariables(rightv.strip())
                if rightvalue is None:
                    self.states = {}
                    return None
                    
                calcObj.setExpr(rightvalue)
                cal_value = calcObj.calculate
                    
                if cal_value is None:
                    return None
                    
                self.states[leftv.strip()] = cal_value
                result[expr] = self.states.copy()

        return result

def run_tests():
    import doctest

    #- Run tests in all docstrings
    #doctest.testmod(verbose=True)
    
    #- Run tests per class - Uncomment the next line to run doctest by function. Replace Stack with the name of the function you want to test
    #doctest.run_docstring_examples(Stack, globals(), name='HW3',verbose=True)   

if __name__ == "__main__":
    run_tests()