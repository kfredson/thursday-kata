

def initialize(n):
    x = n
    totalSize = 1
    while x != 0:
        x /= 2
        totalSize *= 2
    tree = []
    sSize = totalSize
    cSum = 0
    currentVal = n
    idx = 0
    while sSize != 0:
        tree.append(min(currentVal,sSize))
        cSum += sSize
        currentVal -= sSize
        if currentVal < 0:
            currentVal = 0
        if cSum==totalSize:
            sSize /= 2
            cSum = 0
            currentVal = n
        idx += 1
    return tree
            


def getNthElement(n, tree):
    cTotal = tree[0]
    cPos = 0
    while 2*cPos+2 < len(tree):
        nextVal2 = tree[2*cPos+2]
        if cTotal-nextVal2 >= n:
            cPos = 2*cPos+1
            cTotal = cTotal-nextVal2
        else:
            cPos = 2*cPos+2
    return cPos-(len(tree)/2)+1
    
    

def remove(n, tree):
    startPos = (len(tree)/2)+n-1
    while startPos!=0:
        tree[startPos] = tree[startPos]-1
        startPos = ((startPos+1)/2)-1
    tree[startPos] = tree[startPos]-1


def reconstructQueue(people):
    answer = [None]*len(people)
    people.sort(key = lambda x: (x[0],-x[1]))
    tree = initialize(len(people))
    for x in people:
        idx = getNthElement(x[1]+1,tree)
        answer[idx-1] = x
        remove(idx,tree)
    return answer
	
def reconstructQueue2(people):
	res = []     
	people.sort(key=lambda x:(-x[0],x[1]))
	for x,y in people:
		res.insert(y,[x,y])        
	return res


testSize = 500000
import random
heights = []
for x in xrange(testSize):
    heights.append(random.randint(1,1000))
queue = []
for x in enumerate(heights):
    count = 0
    for y in range(x[0]):
        if heights[y] >= x[1]:
            count += 1
    queue.append((x[1],count))

queue.sort(key = lambda x: random.randint(1,1000))
queue1 = list(queue)
queue2 = list(queue)
