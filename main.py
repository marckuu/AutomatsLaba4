matrix = [['q0', 'q1'],
          ['q2', 'q1'],
          ['q0', 'q3'],
          ['q4', 'q3'],
          ['q5', 'q3'],
          ['q5', 'q3']]

colNames = ['0', '1']
strNames = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']
startClasses = [['q0', 'q1', 'q2'], ['q3', 'q4', 'q5']]





def findVal(q, val, matrix, strNames, colNames):
    strindx = strNames.index(q)
    colIndx = colNames.index(val)

    return matrix[strindx][colIndx]


def findClasses(startClasses, matrix, strNames, colNames):
    resClass = []
    counter = 0
    temp = []
    for a in startClasses:
        if len(a) == 1:
            resClass.append([])
            resClass[-1].append(a[0])
            continue
        counter2 = 0
        counter += 1
        for j in colNames:
            for i in a:
                counter3 = 0
                flag = False
                flag3 = False
                res = findVal(i, j, matrix, strNames, colNames)
                for k in a:
                    if res == k:
                        flag = True
                if flag:
                        counter2 += 1
                        counter3 += 1
                        temp.append(i)
                        flag3 = True
                else:
                    resClass.append([])
                    resClass[-1].append(i)

                    if not (counter2 == a.index(i)):
                        resClass.append([])
                        temp.reverse()
                        for t in range((len(a) - a.index(i)) + 1):
                            resClass[-1].append(temp[t])

        if counter2 == (len(colNames)*len(a)):
            resClass.append([])
            for d in a:
                resClass[-1].append(d)
        elif flag3:
            resClass.append([])
            temp.reverse()
            for i in range(counter3):
                resClass[-1].append(temp[-i])
        temp = []
    return resClass



def buildGraph(matrix, resClasses, strNames, colNames):
    resMatrix = []
    for i in range(len(matrix)):
        resMatrix.append([0]*len(matrix[0]))
    for j in colNames:
        for i in resClasses:
            if len(i) == 1:
                res = findVal(i[0], j, matrix, strNames, colNames)
                strIndx = i[0][1:]
                strIndx = int(strIndx)
                colIndx = colNames.index(j)
                resMatrix[strIndx][colIndx] = res
            else:
                res = findVal(i[0], j, matrix, strNames, colNames)
                for k in i:
                        if k == res:
                            strIndx = i[0][1:]
                            strIndx = int(strIndx)
                            colIndx = colNames.index(j)
                            resMatrix[strIndx][colIndx] = i[0]
    return resMatrix



print(findClasses(startClasses, matrix, strNames, colNames))
resClasses = findClasses(startClasses, matrix, strNames, colNames)
print(findClasses(resClasses, matrix, strNames, colNames))
resClasses2 = findClasses(resClasses, matrix, strNames, colNames)
print(buildGraph(matrix, resClasses2, strNames, colNames))

