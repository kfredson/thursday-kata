import Queue

def getAnswer(oper,left,right):
    if oper[0]=='/':
        #print ('ans','/',left,right,left/right)
        return left/right
    elif oper[0]=='*':
        #print ('ans','*',left,right,left*right)
        return left*right
    elif oper[0]=='+':
        #print ('ans','+',left,right,left+right)
        return left+right
    elif oper[0]=='-':
        #print ('ans','-',left,right,left-right)
        return left-right
    

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
            operParenStack.append((x,i,len(operParenStack)))
        elif x=='*' or x=='/':
            operParenStack.append((x,i,len(operParenStack)))
        elif (x=='-' or x=='+') and markNext:
            operParenStack.append((x,i,len(operParenStack)))
        if type(x)==type(1):
            markNext = True
        elif x==')':
            markNext = True
        else:
            markNext = False

    parent = [None]*len(operParenStack)
    leftChild = [None]*len(operParenStack)
    rightChild = [None]*len(operParenStack)

    precedence = {'-':0, '+':0, '/':1, '*':1, 'P':2, '(':-1}

    linkStack = []

    for x in operParenStack:
        if x[0]==')':
            s = linkStack.pop()
            while s[0]!='(':
                s = linkStack.pop()
            linkStack.append(('P',s[1],s[2]))
        else:
            cont = True
            while cont:
                if len(linkStack)==0:
                    linkStack.append(x)
                    cont = False
                else:
                    s = linkStack.pop()
                    if precedence[s[0]] < precedence[x[0]] or x[0]=='(':
                        linkStack.append(s)
                        linkStack.append(x)
                        parent[x[2]] = s[2]
                        rightChild[s[2]] = x[2]
                        cont = False
                    elif precedence[s[0]] == precedence[x[0]]:
                        parent[s[2]] = x[2]
                        leftChild[x[2]] = s[2]
                        cont = True
                    elif precedence[s[0]] > precedence[x[0]]:
                        cParent = parent[s[2]]
                        if cParent != None:
                            if precedence[operParenStack[cParent][0]] < precedence[x[0]]:
                                parent[s[2]] = x[2]
                                leftChild[x[2]] = s[2]
                        else:
                            parent[s[2]] = x[2]
                            leftChild[x[2]] = s[2]
    leftCalcAnswer = [None]*len(operParenStack)
    rightCalcAnswer = [None]*len(operParenStack)
    operPosition = -1
    for x in enumerate(lexerStack):
        if type(x[1])==type(1):
            while operPosition+1 < len(operParenStack) and operParenStack[operPosition+1][1] < x[0]: 
                operPosition += 1
            start = 0
            if operPosition > -1:
                start = operParenStack[operPosition][1]+1
            sign = 1
            for y in range(start,x[0]):
                if lexerStack[y]=='-':
                    sign *= -1
            if operPosition==-1:
                if len(operParenStack)==0:
                    return sign*x[1]
                else:
                    leftCalcAnswer[0] = sign*x[1]
            else:
                if operPosition < len(operParenStack)-1:
                    if rightChild[operPosition]==None:
                        rightCalcAnswer[operPosition] = sign*x[1]
                    elif leftChild[operPosition+1]==None:
                        leftCalcAnswer[operPosition+1] = sign*x[1]
                else:
                    rightCalcAnswer[operPosition] = sign*x[1]
    checkQueue = Queue.Queue()
    for x in range(len(operParenStack)):
        if x!=')':
            checkQueue.put(x)
    while not checkQueue.empty():
        x = checkQueue.get()
        if rightCalcAnswer[x]!=None and leftCalcAnswer[x]!=None:
            if parent[x]==None:
                return getAnswer(operParenStack[x],leftCalcAnswer[x],rightCalcAnswer[x])
            else:
                if leftChild[parent[x]]==x:
                    leftCalcAnswer[parent[x]] = getAnswer(operParenStack[x],leftCalcAnswer[x],rightCalcAnswer[x])
                    checkQueue.put(parent[x])
                elif rightChild[parent[x]]==x:
                    rightCalcAnswer[parent[x]] = getAnswer(operParenStack[x],leftCalcAnswer[x],rightCalcAnswer[x])
                    checkQueue.put(parent[x])
        elif operParenStack[x][0]=='(' and rightCalcAnswer[x]!=None:
            sign = 1
            if x > 0:
                prevOper = operParenStack[x-1]
                if prevOper[1] < operParenStack[x][1]-1:
                    for y in range(prevOper[1]+1,operParenStack[x][1]):
                        if lexerStack[y]=='-':
                            sign *= -1
            else:
                for y in range(operParenStack[x][1]):
                    if lexerStack[y]=='-':
                        sign *= -1
            if parent[x]==None:
                return sign*rightCalcAnswer[x]  
            elif leftChild[parent[x]]==x:
                leftCalcAnswer[parent[x]] = sign*rightCalcAnswer[x]
                checkQueue.put(parent[x])
            elif rightChild[parent[x]]==x:
                rightCalcAnswer[parent[x]] = sign*rightCalcAnswer[x]
                checkQueue.put(parent[x])

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

for x in range(1000):
    r = getRandomExpr(20)
    print r[0]
    print compute(r[0])
    print eval(r[0])
    if compute(r[0])!= eval(r[0]):
        raise Exception
