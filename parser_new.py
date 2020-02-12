class computeStack:

    def __init__(self):
        self.stackType = None

        self.operators = []
        self.numbers = []

    def __str__(self):
        return "stackType: "+str(self.stackType)+" operators: "+str(self.operators)+" numbers: "+str(self.numbers)
        
    def collapseStack(self):
        if self.stackType=='UNARY_NUMBER':
            multiplier = 1
            if (self.operators.count('-'))%2 == 1:
                multiplier = -1
            return self.numbers[0]*multiplier
        elif self.stackType=='MULT_DIV':
            ans = self.numbers[1]
            for x in range(len(self.numbers)-1):
                if self.operators[x]=='/':
                    if self.numbers[x]==0:
                        raise Exception('Divide by zero')
                    ans = self.numbers[x]/ans
                elif self.operators[x]=='*':
                    ans = self.numbers[x]*ans
            return ans
        elif self.stackType=='PLUS_MINUS':
            ans = self.numbers[1]
            for x in range(len(self.numbers)-1):
                if self.operators[x]=='+':
                    ans = self.numbers[x]+ans
                elif self.operators[x]=='-':
                    ans = ans-self.numbers[x]
            return ans
        elif self.stackType=='CHRISBROWN':
            return 7
        elif self.stackType==None:
            return self.numbers[0]

def createOrAppendNumber(stack,number):
    if len(stack)==0:
        stack.append(computeStack())
    stack[-1].numbers.append(number)

def compute(s):
    lexerStack = []
    currentNumber = ''
    s = s.lower().replace('chrisbrown','&')
    for x in s:
        if x in '0123456789':
            currentNumber = currentNumber + x
        elif x==' ':
            pass
        else:
            if currentNumber != '':
                lexerStack.append(int(currentNumber))
                currentNumber = ''
            lexerStack.append(x)
    if currentNumber != '':
        lexerStack.append(int(currentNumber))
    print lexerStack
    stackOfStacks = []
    startFunction = False
    #Stack type None means that either stack was just created (such as by paren or beginning of parse)
    #Or only a single number is on the stack with no operations
    for x in lexerStack:
        for y in stackOfStacks:
            print str(y)
        #First step: determine if token should trigger a collapse of the current stack
        if x==')':
            createOrAppendNumber(stackOfStacks,stackOfStacks.pop().collapseStack())
        elif len(stackOfStacks) > 0 and (x=='-' or x=='+') and stackOfStacks[-1].stackType=='MULT_DIV':
            if len(stackOfStacks[-1].numbers)==len(stackOfStacks[-1].operators)+1:
                createOrAppendNumber(stackOfStacks,stackOfStacks.pop().collapseStack())
        #Next step: determine action for current character (begin new stack or add to current stack)
        if x=='(':
            stackOfStacks.append(computeStack())
            if startFunction==True:
                stackOfStacks[-1].stackType = 'CHRISBROWN'
                startFunction = False
        elif x=='-' or x=='+':
            if len(stackOfStacks)==0:
                stackOfStacks.append(computeStack())
            if stackOfStacks[-1].stackType==None:
                if len(stackOfStacks[-1].numbers)==1:
                    stackOfStacks[-1].stackType='PLUS_MINUS'
                    stackOfStacks[-1].operators.append(x)
                else:
                    stackOfStacks[-1].stackType='UNARY_NUMBER'
                    stackOfStacks[-1].operators.append(x)
            elif stackOfStacks[-1].stackType=='MULT_DIV':
                if len(stackOfStacks[-1].numbers)==len(stackOfStacks[-1].operators):
                    newStack = computeStack()
                    newStack.stackType = 'UNARY_NUMBER'
                    newStack.operators.append(x)
                    stackOfStacks.append(newStack)
                else:
                    raise Exception("This should not happen")
            elif stackOfStacks[-1].stackType=='UNARY_NUMBER':
                if len(stackOfStacks[-1].numbers)==0:
                    stackOfStacks[-1].operators.append(x)
                else:
                    raise Exception("This should not happen")
            elif stackOfStacks[-1].stackType=='PLUS_MINUS':
                if len(stackOfStacks[-1].numbers)==len(stackOfStacks[-1].operators):
                    newStack = computeStack()
                    newStack.stackType = 'UNARY_NUMBER'
                    newStack.operators.append(x)
                    stackOfStacks.append(newStack)
                else:
                    stackOfStacks[-1].operators.append(x)
        elif x=='*' or x=='/':
            if stackOfStacks[-1].stackType==None:
                stackOfStacks[-1].stackType='MULT_DIV'
                stackOfStacks[-1].operators.append(x)
            elif stackOfStacks[-1].stackType=='MULT_DIV':
                stackOfStacks[-1].operators.append(x)
            elif stackOfStacks[-1].stackType=='UNARY_NUMBER':
                raise Exception('This should not happen')
            elif stackOfStacks[-1].stackType=='PLUS_MINUS':
                #Backtrack
                newNum = stackOfStacks[-1].numbers.pop()
                newStack = computeStack()
                newStack.stackType = 'MULT_DIV'
                newStack.numbers.append(newNum)
                newStack.operators.append(x)
                stackOfStacks.append(newStack)
        elif x=='&':
            #Special Chris Brown function!
            startFunction = True
        #Last case: x is integer
        elif type(x)==type(3):
            print 'Got integer'
            print x
            createOrAppendNumber(stackOfStacks,x)
            for y in stackOfStacks:
                print str(y)
            if stackOfStacks[-1].stackType=='UNARY_NUMBER':
                createOrAppendNumber(stackOfStacks,stackOfStacks.pop().collapseStack())
        elif x!=')':
            print "Unrecognized input: "+x
            return None
    currentNum = None
    while len(stackOfStacks) > 0:
        if currentNum != None:
            stackOfStacks[-1].numbers.append(currentNum)
        s = stackOfStacks.pop()
        currentNum = s.collapseStack()
    return currentNum


#Testing: create a random valid arithmetic expression and verify that the code returns same thing as Python "eval"
import random
def getRandomExpr(depth):
    exprTypes = ['UNARY_NUMBER','MULT_DIV','PLUS_MINUS','PARENS','NUMBER']
    if depth==0 or random.randint(0,4)==4:
        return [str(random.randint(-10000,10000)),None]
    else:
        exprType = exprTypes[random.randint(0,3)]
        if exprType=='PARENS':
            return ['('+getRandomExpr(depth-1)[0]+')','PARENS']
        elif exprType=='UNARY_NUMBER':
            n = getRandomExpr(depth-1)
            numPlusMinus = random.randint(1,10)
            prefix = ''
            for x in range(numPlusMinus):
                if random.randint(0,1)==0:
                    prefix = prefix + '-'
                else:
                    prefix = prefix + '+'
            if n[1]=='PARENS' or n[1]==None:
                return [prefix+n[0],'UNARY_NUMBER']
            else:
                return [prefix+'('+n[0]+')','UNARY_NUMBER']
        elif exprType=='MULT_DIV':
            numFactors= random.randint(2,10)
            cAns = getRandomExpr(depth-1)[0]
            for x in range(numFactors-1):
                md = '/'
                if random.randint(0,1)==0:
                    md = '*'
                cAns = cAns+md+getRandomExpr(depth-1)[0]
                return [cAns,'MULT_DIV']
        elif exprType=='PLUS_MINUS':
            numTerms = random.randint(2,10)
            cAns = getRandomExpr(depth-1)[0]
            for x in range(numTerms-1):
                pm = '+'
                if random.randint(0,1)==0:
                    pm = '-'
                cAns = cAns+pm+getRandomExpr(depth-1)[0]
                return [cAns,'PLUS_MINUS']
