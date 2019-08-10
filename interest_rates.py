import random


def gcd(a,b):
    a = abs(a)
    b = abs(b)
    while a > 0 and b > 0:
        if a > b:
            a = a%b
        else:
            b = b%a
    return a+b

def reduce_frac(frac1):
    if (frac1[1]==0):
        raise Exception('Invalid fraction (divide by zero)')
    if frac1[0]==0:
        return (0,1)
    else:
        d = gcd(frac1[0],frac1[1])
        #Normalize fraction to make denominator positive
        if frac1[1] < 0:
            d = -d
        return (frac1[0]/d,frac1[1]/d)

def normalize(frac1):
    if frac1[1] < 0:
        return (-frac1[0],-frac1[1])
    return frac1

def plus(frac1,frac2):
    return reduce_frac((frac1[0]*frac2[1]+frac2[0]*frac1[1],frac1[1]*frac2[1]))

def mult(frac1,frac2):
    return reduce_frac((frac1[0]*frac2[0],frac1[1]*frac2[1]))

def LTOE(frac1, frac2):
    frac1 = normalize(frac1)
    frac2 = normalize(frac2)
    return frac2[1]*frac1[0] <= frac1[1]*frac2[0]

def LT(frac1,frac2):
    frac1 = normalize(frac1)
    frac2 = normalize(frac2)
    return frac2[1]*frac1[0] < frac1[1]*frac2[0]

def equals(frac1, frac2):
    return frac2[1]*frac1[0] == frac1[1]*frac2[0]


def getApproximate(relPrecision, frac):
    if (relPrecision[0]==0) or relPrecision[0]*relPrecision[1] < 0:
        raise Exception('Precision must be a positive fraction')
    sign = 1
    if (frac[0]*frac[1] < 0):
        sign = -1
    frac_pos = (abs(frac[0]),abs(frac[1]))
    integerPart = frac_pos[0]/frac_pos[1]

    counter = 0
    compare1 = frac_pos[0]*relPrecision[0]
    compare2 = frac_pos[1]*relPrecision[1]
    while compare1 < compare2:
        compare1 = compare1 << 1
        counter += 1

    remainder = 2*(frac_pos[0]%frac_pos[1])
    currentSum = integerPart
    currentDenom = 1
    actualSum = currentSum
    actualDenom = currentDenom
    for x in range(counter):
        currentSum = currentSum << 1
        currentDenom = currentDenom << 1
        if remainder >= frac_pos[1]:
            currentSum += 1
            remainder = remainder%frac_pos[1]
            actualSum = currentSum
            actualDenom = currentDenom
        remainder = remainder << 1
    if LT(plus((1,1),relPrecision),mult((frac[1],frac[0]),(sign*actualSum,actualDenom))) or LT(plus((1,1),relPrecision),mult(frac,(actualDenom,sign*actualSum))):
        raise Exception('Crap')
    return (sign*actualSum,actualDenom)

def getE(precision):
    if (precision[0]==0) or precision[0]*precision[1] < 0:
        raise Exception('Precision must be a positive fraction')
    invPrecision = plus((3,1),precision)
    invPrecision = plus((1,3),(-invPrecision[1],invPrecision[0]))
    eInv = getEInverse(invPrecision)
    return (eInv[1],eInv[0])

def getEInverse(precision):
    if (precision[0]==0) or precision[0]*precision[1] < 0:
        raise Exception('Precision must be a positive fraction')
    currentFactor = 2
    currentFactorial = 2
    while LTOE(precision,(1,currentFactorial)):
        currentFactor += 1
        currentFactorial *= currentFactor
    sign = 1
    if currentFactor%2==1:
        sign = -1
    cSum = sign
    cProduct = 1
    for x in range(currentFactor,0,-1):
        cProduct *= x
        sign *= -1
        cSum += sign*cProduct
        #print cProduct
    return reduce_frac((cSum,currentFactorial))


#Calculate e^a to within precision.
#a can be any rational number with |a| < 1 and
#precision can be any positive rational number.
def getExp(precision,a):
    precision = reduce_frac(precision)
    a = reduce_frac(a)
    if (precision[0]==0) or precision[0]*precision[1] < 0:
        raise Exception('Precision must be a positive fraction')
    #Special case that a=0
    if a[0]==0:
        return (1,1)
    inverted = 0
    if a[0] > 0:
        inverted = 1
        a = (-a[0],a[1])
    currentValue = (1,1)
    currentIndex = 1
    currentSummand = (1,1)
    while (True):
        lastVal = currentValue
        #Power series term a^n/n!
        currentSummand = reduce_frac((currentSummand[0]*a[0],currentSummand[1]*a[1]*currentIndex))
        currentValue = plus(currentValue,currentSummand)
        currentIndex += 1
        if inverted==0:
            if LTOE((abs(currentSummand[0]),abs(currentSummand[1])),precision):
                return currentValue
        else:
            #Need to check lastVal and currentVal are both positive,
            #otherwise can't bound the interval between their reciprocals
            if (lastVal[0]*lastVal[1] > 0 and currentValue[0]*currentValue[1] > 0):
                diff = plus((lastVal[1],lastVal[0]),(-abs(currentValue[1]),abs(currentValue[0])))
                diff = (abs(diff[0]),abs(diff[1]))
                if LTOE(diff,precision):
                    return (currentValue[1],currentValue[0])

#Get integer upper bound for abs(a^b)
#where a is a rational number and
#b is a non-negative integer

#Idea here: rewrite a^b as e^(b*ln(a))
#Get upper bound for ln(a) by doing
#ln(floor(a)) and using derivative of
#ln(x) at floor(a) = 1/floor(a)
#so ln(a) < ln(floor(a))+frac(a)/floor(a)
def getUpperBoundPower(a,b):
    product = 1
    frac_pos = (abs(a[0]),abs(a[1]))
    int_part = frac_pos[0]/frac_pos[1]
    frac_part = frac_pos[0]%frac_pos[1]
    power = int_part
    if int_part==0:
        return 1
    bCopy = b
    while b > 0:
        if b%2==1:
            product *= power
        power = power*power
        b = (b >> 1)
    adj_int_part = (bCopy*frac_part)/(frac_pos[1]*int_part)
    adj_frac_part = (bCopy*frac_part)%(frac_pos[1]*int_part)
    if adj_frac_part != 0:
        adj_int_part += 1
    return power*(3**adj_int_part)


def getLargeExp(precision, b):
    precision = reduce_frac(precision)
    b = reduce_frac(b)
    if (precision[0]==0) or precision[0]*precision[1] < 0:
        raise Exception('Precision must be a positive fraction')
    if (b[0]==0):
        return (1,1)
    frac_pos = (abs(b[0]),abs(b[1]))
    int_part = frac_pos[0]/frac_pos[1]
    frac_part = frac_pos[0]%frac_pos[1]
    int_part_roundup = int_part
    if (frac_part>0):
        int_part_roundup += 1
    ub = 0
    if (b[0]>0):
        ub = (getUpperBoundPower((27183,10000),int_part_roundup),1)
    else:
        ub = (1,2**int_part)
    #If upper bound is less than precision, it's technically right to return the upper bound as the answer
    if LTOE(ub, precision):
        return ub
    diff = plus(ub,(-precision[0],precision[1]))
    relPrecision = mult(ub,(diff[1],diff[0]))
    relPrecisionRoot = plus((1,1),mult(plus((-1,1),(relPrecision[1],relPrecision[0])),(1,int_part_roundup)))
    #print relPrecisionRoot
    fPrecision = (relPrecisionRoot[1],relPrecisionRoot[0])
    #print fPrecision
    currentProduct = (1,1)
    currentFactor = 0
    lastFactor = 0
    if b[0]>0:
        currentFactor = getE(plus((-3*fPrecision[1],fPrecision[0]),(3,1)))
        lastFactor = getExp(plus((-3*fPrecision[1],fPrecision[0]),(3,1)),(frac_part,frac_pos[1]))
    else:
        currentFactor = getEInverse(plus((-fPrecision[1],fPrecision[0]*2),(1,2)))
        lastFactor = getExp(plus((-fPrecision[1],fPrecision[0]*2),(1,2)),(-frac_part,frac_pos[1]))
    fPrecision = plus((-1,1),fPrecision)
    while int_part > 0:
        if int_part%2==1:
            tempProduct = mult(currentFactor,currentProduct)
            tempProductApprox = getApproximate(fPrecision,tempProduct)
            if tempProductApprox[1] < tempProduct[1]:
                currentProduct = tempProductApprox
            else:
                currentProduct = tempProduct
        currentFactor = (currentFactor[0]**2,currentFactor[1]**2)
        currentFactorApprox = getApproximate(fPrecision,currentFactor)
        if (currentFactorApprox[1] < currentFactor[1]):
            currentFactor = currentFactorApprox
        int_part = (int_part >> 1)
    return mult(currentProduct,lastFactor)

def getLargeIntegerPower(precision, a, b):
    if (b <= 0):
        if (a[0]==0):
            raise Exception('Divide by zero or trying to calculate 0^0')
        elif a[1]==0:
            raise Exception('Invalid fraction (divide by zero)')
        elif b==0:
            return (1,1)
        ub = getUpperBoundPower((a[1],a[0]),-b)
        plusBound = plus((ub,1),precision)
        neededPrecision = plus((1,ub),(-plusBound[1],plusBound[0]))
        return getLargeIntegerPower(neededPrecision,(a[1],a[0]),-b)
    ub = getUpperBoundPower(a,b)
    ub = (ub,1)
    diff = plus(ub,(-precision[0],precision[1]))
    relPrecision = mult(ub,(diff[1],diff[0]))
    relPrecisionRoot = plus((1,1),mult(plus((-1,1),(relPrecision[1],relPrecision[0])),(1,b)))
    print relPrecisionRoot
    fPrecision = (relPrecisionRoot[1],relPrecisionRoot[0])
    print fPrecision
    currentProduct = (1,1)
    currentFactor = a
    fPrecision = plus((-1,1),fPrecision)
    nr_roundings_p = 0
    nr_roundings_a = 0
    roundingsFactorP = 0
    roundingsFactorA = 0
    while b > 0:
        if b%2==1:
            tempProduct = mult(currentFactor,currentProduct)
            nr_roundings_p += roundingsFactorP+1
            tempProductApprox = getApproximate(fPrecision,tempProduct)
            if tempProductApprox[1] < tempProduct[1]:
                currentProduct = tempProductApprox
                nr_roundings_a += roundingsFactorA+1
            else:
                currentProduct = tempProduct
        currentFactor = (currentFactor[0]**2,currentFactor[1]**2)
        currentFactorApprox = getApproximate(fPrecision,currentFactor)
        roundingsFactorP = roundingsFactorP*2+1
        roundingsFactorA = roundingsFactorA*2
        if (currentFactorApprox[1] < currentFactor[1]):
            currentFactor = currentFactorApprox
            roundingsFactorA += 1
        print currentFactor
        print currentProduct
        print toDecimal(currentProduct,10)
        print "upeer bound: "+str(ub[0])
        b = (b >> 1)
    print "potential roundings: "+str(nr_roundings_p)
    print "actual roundings: "+str(nr_roundings_a)
    return currentProduct



def toDecimal(frac,num_digits_after_decimalpoint):
    sign = ''
    if (frac[0]*frac[1] < 0):
        sign = '-'
    frac_pos = (abs(frac[0]),abs(frac[1]))
    integerPart = frac_pos[0]/frac_pos[1]
    remainder = 10*(frac_pos[0]%frac_pos[1])
    s = ''
    while len(s) < num_digits_after_decimalpoint:
        if remainder >= frac_pos[1]:
            s = s+str(remainder/frac_pos[1])
            remainder = remainder%frac_pos[1]
        else:
            s = s+'0'
        remainder *= 10
    return sign+str(integerPart)+'.'+s


def getRandomPrincipal():
    randVal = random.randint(-100000000,100000000)
    #Min/max of (-/+)100 million, then divide by 100 to get cent values
    return (randVal,100)

def getRandomInterestRate():
    randVal = random.randint(-10000,10000)
    return (randVal,10000)

#Return random time period in units of years
def getRandomTimePeriod():
    randVal = random.randint(1,7)
    if randVal==1:
        return ((1,365),"1 day")
    elif randVal==2:
        return ((30,365),"30 days")
    elif randVal==3:
        return ((90,365),"90 days")
    elif randVal==4:
        return ((1,1),"1 year")
    elif randVal==5:
        return ((20,12),"20 months")
    elif randVal==6:
        return ((7,1),"7 years")
    else:
        return ((1000,1),"1000 years")

#Return type of compounding in units of years (or continuous)
def getRandomCompounding():
    randVal = random.randint(1,5)
    if randVal==1:
        return (None,'Continuous')
    elif randVal==2:
        return ((1,365),'Daily')
    elif randVal==3:
        return ((1,12),'Monthly')
    elif randVal==4:
        return ((1,4),'Quarterly')
    else:
        return ((1,1),'Annual')


if __name__=='__main__':
    principal = getRandomPrincipal()
    rate = getRandomInterestRate()
    period = getRandomTimePeriod()
    compounding = getRandomCompounding()

    print "Calculating interest with the following parameters: "
    print "Principal: "+toDecimal(principal,2)+" moneys"
    print "Rate: "+toDecimal((rate[0]*100,rate[1]),2)+" percent"
    print "Period: "+period[1]
    print "Compounding: "+compounding[1]

    if compounding[1]=='Continuous':
        multiplier = getExp((1,100000000000000),mult(period[0],(rate[0],100*rate[1])))
        ans = mult(multiplier,principal)
        print "Final value: "+toDecimal(ans,2)
        print "Amount earned/lost on interest: "+toDecimal(plus(ans,(-principal[0],principal[1])),2)
    else:
        base = plus((1,1),mult(compounding[0],rate))
        numPeriods = (period[0][0]*compounding[0][1])/(period[0][1]*compounding[0][0])
        print "Number of periods: "+str(numPeriods)
        multiplier = getLargeIntegerPower((1,100000000000000),base,numPeriods)
        ans = mult(multiplier,principal)
        print "Final value: "+toDecimal(ans,2)
        print "Amount earned/lost on interest: "+toDecimal(plus(ans,(-principal[0],principal[1])),2)
