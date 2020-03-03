class computeStack:

    def __init__(self,parent):
        self.stackType = None

        self.operators = []
        self.nodes = []
        self.parent = parent

    def __str__(self):
        return "stackType: "+str(self.stackType)+" operators: "+str(self.operators)+" numbers: "+str(self.nodes)

def evaluate(node):
    print node
    if type(node)==type([1]):
        mult = 1
        for x in node:
            if x=='-':
                mult *= -1
            elif x=='+':
                pass
            else:
                mult *= x
        return mult
    elif node.stackType==None or node.stackType=="parens":
        mult = 1
        for x in node.operators:
            if x=='-':
                mult *= -1
        return mult*evaluate(node.nodes[0])
    else:
        if node.stackType=='pm':
            cVal = evaluate(node.nodes[0])
            for x in enumerate(node.operators):
                if x[1]=='-':
                    cVal -= evaluate(node.nodes[x[0]+1])
                else:
                    cVal += evaluate(node.nodes[x[0]+1])
            return cVal
        else:
            cVal = evaluate(node.nodes[0])
            for x in enumerate(node.operators):
                if x[1]=='/':
                    cVal /= evaluate(node.nodes[x[0]+1])
                else:
                    cVal *= evaluate(node.nodes[x[0]+1])
            return cVal
        
    
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
                print 'A'
                cStack.operators.append(x[0])
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
                cStack.stackType = 'pm'
            else:
                print 'B'
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
                cStack = cStack.parent
                cStack.operators.append(x[0])
        elif x[0]=='*' or x[0]=='/':
            if cType=='dm' or cType==None:
                print 'C'
                cStack.operators.append(x[0])
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
                cStack.stackType = 'dm'
            else:
                print 'D'
                cStack = computeStack(cStack)
                cStack.parent.nodes.append(cStack)
                cStack.stackType='dm'
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
                cStack.operators.append(x[0])
        elif x[0]==')':
            if lastIndex+1 < currentIndex:
                cStack.nodes.append(lexerStack[lastIndex+1:currentIndex])
            cStack = cStack.parent.parent
    if currentIndex+1 < len(lexerStack):
        origStack.nodes.append(lexerStack[currentIndex+1:])
    return origStack
