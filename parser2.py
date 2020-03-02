class computeStack:

    def __init__(self,parent):
        self.stackType = None

        self.operators = []
        self.nodes = []
        self.parent = parent

    def __str__(self):
        return "stackType: "+str(self.stackType)+" operators: "+str(self.operators)+" numbers: "+str(self.numbers)

def evaluate(cStack):
    if cStack.stackType==None or cStack.stackType="parens":
        mult = 1
        for x in cStack.operators:
            if x==[-1]:
                mult *= -1
        return mult*evaluate(cStack.nodes[0])
    else:
        if stackType=='pm':
            initialVal = cStack.nodes[0]
            
        else:
            
        
    
def compute(s):
    lexerStack = []
    currentNumber = ''
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

    operParenStack = []

    markNext = False
    for i,x in enumerate(lexerStack):
        if x=='(' or x==')':
            operParenStack.append((x,i))
        elif x=='*' or x=='/':
            operParenStack.append((x,i))
        elif (x=='-' or x=='+') and markNext:
            operParenStack.append((x,i))
        if type(x)==type(1):
            markNext = True
        elif x==')':
            markNext = True
        else:
            markNext = False

    print operParenStack
    cStack = computeStack(None)
    currentIndex = -1
    origStack = cStack

    for x in operParenStack:
        lastIndex = currentIndex
        currentIndex = x[1]
        cType = cStack.stackType
        if x[0]=='(':
            cStack = computeStack(cStack)
            cStack.parent.nodes.append(cStack)
            cStack.stackType = "parens"
            cStack.operators = lexerStack[lastIndex+1:currentIndex]
            cStack = computeStack(cStack)
            cStack.parent.nodes.append(cStack)
        elif x[0]=='-' or x[0]=='+':
            if cType=='pm' or cType==None:
                cStack.operators.append(x[0])
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
                cStack.stackType = 'pm'
            else:
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
                cStack = cStack.parent
        elif x[0]=='*' or x[1]=='/':
            if cType=='dm' or cType==None:
                cStack.operators.append(x[0])
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
                cStack.stackType = 'dm'
            else:
                cStack = computeStack(cStack)
                cStack.parent.nodes.append(cStack)
                cStack.stackType='pm'
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
                cStack.operators.append(x[0])
        elif x[0]==')':
            if lastIndex+1 < currentIndex:
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
            cStack = cStack.parent.parent
    if currentIndex+1 < len(lexerStack):
        origStack.nodes.append(lexerStack[currentIndex+1:])
    return origStack


