from sys import exit

inList = list(str(raw_input(">")))
fracList = []  # list of all fractions
cmdList = []  # list of the commands that are to be applied to the fractions
tmparr = []
inFrac = False
blockCmd = True
nextIsNeg = False
tmparrPos = 0
temparrLoop = 0
fracPos = 0
inFracMulti = ""


def restructCmd(find, rep):
    # Function for restructuring the cmdList while calculating
    for i in range(len(cmdList)):
        if(cmdList[i] == find):
            cmdList[i] = rep


def ggt(a, b):
    # Function for getting the GCD for reducing the fraction
    if(a > b):
        a, b = b, a
    rest = a % b
    while rest > 0:
        rest = a % b
        a = b
        b = rest
    return a


def add(frac1, frac2):
    if(frac1[1] == frac2[1]):
        return(frac1[0] + frac2[0], frac1[1])
    return(frac1[0]*frac2[1] + frac2[0]*frac1[1], frac1[1]*frac2[1])


def subtract(frac1, frac2):
    if(frac1[1] == frac2[1]):
        return(frac1[0] - frac2[0], frac1[1])
    return(frac1[0]*frac2[1] - frac2[0]*frac1[1], frac1[1]*frac2[1])


def multiply(frac1, frac2):
    return (frac1[0]*frac2[0], frac1[1]*frac2[1])


def divide(frac1, frac2):
    return (frac1[0]*frac2[1], frac1[1]*frac2[0])


for i in range(len(inList)):
    tmparr.append("")
for i in range(len(inList)):
    if(inFrac):
        if(inList[i] == ')'):
            inFrac = False
            blockCmd = False
            for e in range(temparrLoop, tmparrPos, 2):
                # loop through the temp array and append to the frac List
                if(len(inFracMulti) == 0):
                    fracList.append([int(tmparr[e]), int(tmparr[e+1])])
                else:
                    fracList.append(
                        [(int(inFracMulti)*int(tmparr[e+1]))+int(tmparr[e]), int(tmparr[e+1])])
            tmparrPos += 1
            temparrLoop += 2
            inFracMulti = ""
            continue
        if(inList[i] == '/'):
            tmparrPos += 1
            continue
        if(inList[i] == '-'):
            try:
                int(inList[i+1])
                tmparr[tmparrPos] += str("-")
                continue
            except ValueError:
                print("Invalid character: '-' before "+str(inList[i+1]))
                exit(-1)
        try:
            int(inList[i])
            tmparr[tmparrPos] += str(inList[i])
        except ValueError:
            print("Invalid character: "+str(inList[i]))
            exit(-1)
    if(inList[i] == '('):
        inFrac = True
        continue
    if(inList[i] == '+'):
        if(blockCmd):
            print("Illegal character '" +
                  str(inList[i])+"' after '"+str(inList[i-1]+"'"))
            exit(-1)
        cmdList.append(fracPos)
        cmdList.append('+')
        cmdList.append(fracPos+1)
        fracPos += 1
        blockCmd = True
        continue
    if(inList[i] == '-'):
        if(blockCmd):
            print("Illegal character '" +
                  str(inList[i])+"' after '"+str(inList[i-1]+"'"))
            exit(-1)
        cmdList.append(fracPos)
        cmdList.append('-')
        cmdList.append(fracPos+1)
        fracPos += 1
        blockCmd = True
        continue
    if(inList[i] == '*'):
        if(blockCmd):
            print("Illegal character '" +
                  str(inList[i])+"' after '"+str(inList[i-1]+"'"))
            exit(-1)
        cmdList.append(fracPos)
        cmdList.append('*')
        cmdList.append(fracPos+1)
        fracPos += 1
        blockCmd = True
        continue
    if(inList[i] == '/'):
        if(blockCmd):
            print("Illegal character '" +
                  str(inList[i])+"' after '"+str(inList[i-1]+"'"))
            exit(-1)
        cmdList.append(fracPos)
        cmdList.append('/')
        cmdList.append(fracPos+1)
        fracPos += 1
        blockCmd = True
        continue
    if(inList[i] == " "):
        continue
    try:
        if(not inFrac):
            inFracMulti += str(int(inList[i]))
    except ValueError:
        print("Unknown character: "+str(inList[i]))
        exit(-1)

# Check for division through zero
for i in range(len(fracList)):
    if(fracList[i][1] == 0):
        print("(%i,%i) is invalid: Division by 0 is not allowed" %
              (fracList[i][0], fracList[i][1]))
        exit(-1)


# Multiplication and division
for i in range(0, len(cmdList), 3):
    if(cmdList[i+1] == '*'):
        retTup = multiply((fracList[cmdList[i]][0], fracList[cmdList[i]][1]),
                          (fracList[cmdList[i+2]][0], fracList[cmdList[i+2]][1]))
        fracList[cmdList[i]][0] = retTup[0]
        fracList[cmdList[i]][1] = retTup[1]
        restructCmd(cmdList[i+2], cmdList[i])
    if (cmdList[i+1] == '/'):
        retTup = divide((fracList[cmdList[i]][0], fracList[cmdList[i]][1]),
                        (fracList[cmdList[i+2]][0], fracList[cmdList[i+2]][1]))
        fracList[cmdList[i]][0] = retTup[0]
        fracList[cmdList[i]][1] = retTup[1]
        restructCmd(cmdList[i+2], cmdList[i])

#Adding and subtracting
for i in range(0, len(cmdList), 3):
    if(cmdList[i+1] == '+'):
        retTup = add((fracList[cmdList[i]][0], fracList[cmdList[i]][1]),
                     (fracList[cmdList[i+2]][0], fracList[cmdList[i+2]][1]))
        fracList[cmdList[i]][0] = retTup[0]
        fracList[cmdList[i]][1] = retTup[1]
        restructCmd(cmdList[i+2], cmdList[i])
    if (cmdList[i+1] == '-'):
        retTup = subtract((fracList[cmdList[i]][0], fracList[cmdList[i]][1]),
                          (fracList[cmdList[i+2]][0], fracList[cmdList[i+2]][1]))
        fracList[cmdList[i]][0] = retTup[0]
        fracList[cmdList[i]][1] = retTup[1]
        restructCmd(cmdList[i+2], cmdList[i])

num = ggt(fracList[0][0], fracList[0][1])
reduced = False
if(num == 1 or num == 0):
    reduced = False
else:
    reduced = True
barCount = 0
reducedBarCount = 0
upperSpacer = ""
lowerSpacer = ""
if(len(str(int(fracList[0][0]))) > len(str(int(fracList[0][1])))):
    barCount = len(str(int(fracList[0][0])))
    lowerSpacer = (
        len(str(int(fracList[0][0])))-len(str(int(fracList[0][1]))))*" "
else:
    barCount = len(str(int(fracList[0][1])))
    upperSpacer = (
        len(str(int(fracList[0][1])))-len(str(int(fracList[0][0]))))*" "
if(reduced):
    if(len(str(int(fracList[0][0]/num))) > len(str(int(fracList[0][1]/num)))):
        reducedBarCount = len(str(int(fracList[0][0]/num)))
    else:
        reducedBarCount = len(str(int(fracList[0][1]/num)))
# Output
print("\n" + 100*"-")
if(reduced):
    print(8*" " + str(int(fracList[0][0])) + upperSpacer + " (Reduced with " +
          str(num)+")  " + str(int(fracList[0][0]/num)))
    print("Result: "+barCount*"-"+" "+(15+len(str(num)))
          * "-"+"> "+reducedBarCount*"-")
    print(8*" " + str(int(fracList[0][1]))+lowerSpacer + (18 +
                                                          len(str(num))) * " " + str(int(fracList[0][1]/num)))
else:
    if(fracList[0][0] == 0):
        print("\nResult: 0\n")
    else:
        print(8*" " + str(int(fracList[0][0])))
        print("Result: "+barCount*"-")
        print(8*" " + str(int(fracList[0][1])))
print(100*"-")
