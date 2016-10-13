# Current smoothest A:
# 1003176071112866192112901008112932095113848799
#
# Current minimum smoothness:
# 68
#
# Our minimum number: 112866192112901008112932095113848799
#

# Read in data
path = '/home/josephnasante/crypto/data2.txt'
input = file(path,'r')
inputValues = input.readline().split(" ")
input.close()

# Define variables
smoothestA = int(inputValues[0])
minSmoothness = int(inputValues[1])
minA = int(inputValues[2])
maxA = int(inputValues[3])
A = minA
maxSearchSpace = 2^600

# Set up fields
R.<x> = GF(2)[]
Q.<a> = QuotientRing(R, x^609 + x^31 + 1)
poly = a^607 + a^105 + 1

#increments
increment = 10^36
expIncrement = poly^increment
noFrogs = 4 # edit here for number of leap frogging computers
searchCycleIncrement = (maxA-minA) * noFrogs

print("Number of frogs: " + str(noFrogs))

while A <= maxSearchSpace:
    ans = poly^A

    print("Beginning new cycle. start: " + str(minA) + ", end: " + str(maxA))

    i = 0
    while A <= maxA:
    #for i in range (0, 100):
        # Factorization & smoothness calculation
        factorization = lift(ans).factor()
        smoothness = factorization[len(factorization)-1][0].degree()
        
        # Have we found a minimum?
        if (smoothness < minSmoothness):
            minSmoothness = smoothness
            smoothestA = A

            # print result
            print("new min with: " + str(smoothestA))
            print("current min: " + str(minSmoothness))
            
            f = file(path,'w')
            f.write(str(smoothestA) + " ")
            f.write(str(minSmoothness) + " ")
            f.write(str(minA) + " ")
            f.write(str(maxA))
            f.close()
        
        # increment A
        A += increment
        ans = ans*expIncrement
        
        # make sure it's still alive
        if i % 50000 == 0:
            print("time step: " + str(i))
        i+= 1
    
    print("Finished cycle. start: " + str(minA) + ", end: " + str(maxA))
    
    # Increment seach space and begin cycle again
    minA += searchCycleIncrement
    maxA += searchCycleIncrement
    A = minA
    
    f = file(path,'w')
    f.write(str(smoothestA) + " ")
    f.write(str(minSmoothness) + " ")
    f.write(str(minA) + " ")
    f.write(str(maxA))
    f.close()