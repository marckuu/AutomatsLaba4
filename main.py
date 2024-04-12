from prettytable import PrettyTable
def determ(alphabet, alphabetQ, graphTable, startVertex, endVertex):
    def add(i, graphTable, eIndx, alphabetQ):
        res = []
        for k in graphTable[i][eIndx]:
            if k == '0':
                res.append('0')
                break
            res.append(k)
            nextIndx = alphabetQ.index(k)
            res2 = add(nextIndx, graphTable, eIndx, alphabetQ)
            for j in res2:
                if j == '0':
                    continue
                res.append(j)
        return res

    def countValue(alphabet, alphabetQ, graphTable, q, val):
        res = []
        stop = False
        isGo = False
        indxQ = alphabetQ.index(q)
        indxVal = alphabet.index(val)
        for a in alphabet:
            if a == 'E' or a == 'E':
                eIndx = alphabet.index(a)

        # 1
        if graphTable[indxQ][indxVal] != '0':
            res.append(graphTable[indxQ][indxVal])
            indxQ = alphabetQ.index(graphTable[indxQ][indxVal])
            isGo = True
        if isGo:
            tempRes = add(indxQ, graphTable, eIndx, alphabetQ)
            for k in tempRes:
                if k == '0':
                    continue
                res.append(k)

        # 2
        indxQ = alphabetQ.index(q)
        indxVal = alphabet.index(val)
        isGo1 = False
        isGo = False

        for d in graphTable[indxQ][eIndx]:
            if d != '0':
                indxQ = alphabetQ.index(d)
                isGo1 = True
            if isGo1:
                if graphTable[indxQ][indxVal] != '0':
                    res.append(graphTable[indxQ][indxVal])
                    #     indxQ = alphabetQ.index(graphTable[indxQ][indxVal])
                    isGo = True
            if isGo:
                for s in graphTable[indxQ][eIndx]:
                    while True:
                        if s == '0':
                            break
                        res.append(s)
                        indxQ = alphabetQ.index(s)
        return res

    def countValueForP(i, val, sTable, alphabet2):
        res = set()
        tempRes = sTable[i][alphabet2.index(val)]
        for i in tempRes:
            res.add(i)
        return res

    def tryСhain(p, val, pTable, alphabet2):
        indx = p[1:]
        indx = int(indx)
        while True:
            if pTable[indx][alphabet2.index(val)] == '0':
                return "1"
            else:
                return pTable[indx][alphabet2.index(val)]
    # Создание массива для Е-замыканий
    eTable = []
    for i in range(len(alphabetQ)):
        eTable.append([])

    # Нахождение Е-замыканий (Дописать в начале проверку на наличие эпсилонов)
    for a in alphabet:
        if a == 'E' or a == 'E':
            eIndx = alphabet.index(a)

    for i in range(len(alphabetQ)):
        eTable[i].append(alphabetQ[i])
        j = i
        if graphTable[j][eIndx][0] == '0':
            continue
        else:
            res = add(i, graphTable, eIndx, alphabetQ)
            for k in res:
                eTable[i].append(k)

    # Вывод таблицы с Е-замыканиями
    print("Е-замыкания:")
    for i in range(len(alphabetQ)):
        print(alphabetQ[i] + ":", eTable[i])

    #  Создание масиива для хранения таблицы с S
    sTable = []
    for i in range(len(eTable)):
        sTable.append([0] * (len(alphabet) - 1))

    # Подсчет значений для таблицы S
    tempData = set()
    res = []
    curElem = []
    for i in range(len(alphabetQ)):
        for k in alphabet:
            if k == "E":
                continue
            for j in range(len(eTable[i])):
                res.append(countValue(alphabet, alphabetQ, graphTable, eTable[i][j], k))
            for f in res:
                for g in f:
                    tempData.add(g)

            # Проверка на вложенность
            column = alphabet.index(k)
            if len(tempData) == 0:
                curElem.append('0')
                sTable[i][column] = curElem
            else:
                for w in range(len(eTable)):
                    is_subset = False
                    is_subset = set(eTable[w]).issubset(tempData)
                    if is_subset:
                        curElem.append("S" + str(w))
                sTable[i][column] = curElem
            res = []
            curElem = []
            tempData = set()

    # Вывод таблицы с S
    alphabet2 = alphabet.copy()
    alphabet2.remove('E')

    mytable2 = PrettyTable()
    columns2 = alphabet2.copy()
    columns2.insert(0, "Состояние")
    mytable2.field_names = columns2
    for i in range(len(alphabetQ)):
        strName2 = "S" + str(i)
        string2 = sTable[i].copy()
        string2.insert(0, strName2)
        mytable2.add_row(string2)
    print(mytable2)

    # Определение начального состояния

    # Добавление начальных вершин, которые можно достичь по Е-переходу
    startVertex = set(startVertex)
    tempRes = []
    for j in startVertex:
        elem = j
        indx = alphabetQ.index(elem)
        for i in eTable[indx]:
            tempRes.append(i)
    for i in tempRes:
        startVertex.add(i)

    # Добавление конечных вершин, которые можно достичь по Е-переходу
    endVertex = set(endVertex)
    tempRes = []
    for j in endVertex:
        elem = j
        indx = alphabetQ.index(elem)
        for i in eTable[indx]:
            tempRes.append(i)
    for i in tempRes:
        endVertex.add(i)

    # Определение начальных S
    startS = set()
    for i in startVertex:
        for j in eTable:
            for k in j:
                if k == i:
                    startS.add("S" + str(eTable.index(j)))

    # Определение конечных S
    endS = set()
    for i in endVertex:
        for j in eTable:
            for k in j:
                if k == i:
                    endS.add("S" + str(eTable.index(j)))

    # Создание начального списка, который будет хранить из чего состоят элементы P
    pByS = []
    pByS.append(list(startS))

    # Создание начальной таблицы для хранения P
    pTable = []
    pTable.append([0] * len(alphabet2))

    # Нахождение элементов таблицы P
    res = set()
    count = 0
    for i in pByS:
        i = pByS.index(i)
        for k in alphabet2:
            for j in pByS[i]:
                tempRes = countValueForP(int(j[-1]), k, sTable, alphabet2)
                for w in tempRes:
                    if w == '0':
                        continue
                    res.add(w)
            for t in res:
                if t == '0':
                    count += 1
            if count == len(res):
                curElem = '0'
            else:
                localFlag = True
                for w in pByS:
                    if set(w) == res:
                        localFlag = False
                        curElem = "P" + str(pByS.index(w))
                if localFlag:
                    curElem = "P" + str(len(pByS))
                    pByS.append(list(res))
                    pTable.append([0] * len(alphabet2))
            pTable[i][alphabet2.index(k)] = curElem  # Заполнение таблицы P
            res = set()

    # Вывод таблицы P
    mytable3 = PrettyTable()
    columns3 = alphabet2.copy()
    columns3.insert(0, "Состояние")
    mytable3.field_names = columns3
    for i in range(len(pByS)):
        strName3 = "P" + str(i)
        string3 = pTable[i].copy()
        string3.insert(0, strName3)
        mytable3.add_row(string3)
    print(mytable3)

    # Определение начальных P
    startP = "P0"

    # Определение конечных P
    endP = set()
    for i in endS:
        for j in pByS:
            for k in j:
                if k == i:
                    endP.add(
                        "P" + str(pByS.index(j)))  # Добавляет P3 в список конечных вершин, а оно не является таковым

    # Вывод всех начальных и конечных состояний для q, S, P
    print("Начальные состояния q:", startVertex)
    print("Конечные состояния q:", endVertex, '\n')
    print("Начальные состояния S:", startS)
    print("Конечные состояния S:", endS, '\n')
    print("Начальные состояния Р:", startP)
    print("Конечные состояния P:", endP)

    # Цикл для проверки цепочек
    while True:
        # Ввод цепочки символов и проверки
        while True:
            inputData = input("Введите цепочку символов без пробелов:")
            symbols = list(inputData)

            flag = False
            for i in symbols:
                if i == 'q':
                    print("Алфавит не должен содержать q, т.к. через него обозначаются состояния. Повторите ввод:")
                    flag = True
                    break
                if i == ' ':
                    print("Алфавит содержит пробел. Повторите ввод:")
                    flag = True
                    break
            if flag:
                continue

            count = 0
            for j in symbols:
                for i in alphabet:
                    if j == i:
                        count += 1
            if count != len(symbols):
                print("Некоторых символов не поддерживаются автоматом. Повторите ввод: ")
                continue

            flag2 = False
            print(symbols)
            while True:
                isContinue = input(
                    "Продолжить с этим алфавитом? Введите 1, чтобы продолжить, или 0, чтобы повторить ввод.\n")
                if isContinue == "1":
                    break
                if isContinue == "0":
                    flag2 = True
                    break
                else:
                    print("Можно ввести только 1 или 0. Повторите выбор:")
                    continue
            if flag2:
                continue

            if int(isContinue):
                break

        # Проверка допускает ли автомат цепочку
        localFlag = False
        tempI = "P0"
        for j in symbols:
            res = tryСhain(tempI, j, pTable, alphabet2)
            if res == '1':
                for i in endP:
                    if i == tempI:
                        localFlag = True
                if localFlag:
                    break
            tempI = res

        if not localFlag:
            for i in endP:
                if i == tempI:
                    localFlag = True
        if localFlag:
            print("Цепочка допустима")
        else:
            print("Цепочка недопустима")

        data = input("Попробовать другую цепочку? Да - 1, Нет - любой другой символ: ")
        if data != '1':
            break
    return  pTable

matrix = [['q1', 'q4'],
          ['q5', 'q2'],
          ['q6', 'q2'],
          ['q3', 'q6'],
          ['q1', 'q0'],
          ['q6', 'q2'],
          ['q3', 'q6'],
          ['q3', 'q6']]

colNames = ['a', 'b']
strNames = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7']
startClasses = [['q0', 'q1', 'q2', 'q4', 'q5'], ['q3', 'q6', 'q7']]


'''
# Ввод алфавита входных символов
flag = False
while True:
    inputData = input("Введите все символы алфавита подряд без пробелов(Е - принимается за эпислон):")
    colNames = list(inputData)


    # Проверки алфавита
    if len(colNames) < 2:
        print("Алфавит содержит менее 2 элементов. Повторите ввод:")
        continue

    flag = False
    for i in colNames:
        if i == 'q':
            print("Алфавит не должен содержать q, т.к. через него обозначаются состояния. Повторите ввод:")
            flag = True
            break
        if i == ' ':
            print("Алфавит содержит пробел. Повторите ввод:")
            flag = True
            break
        if colNames.count(i) > 1:
            print("Алфавит содержит повторяющиеся элементы. Повторите Ввод:")
            flag = True
            break
    if flag:
        continue

    flag2 = False
    print(colNames)
    while True:
        isContinue = input("Продолжить с этим алфавитом? Введите 1, чтобы продолжить, или 0, чтобы повторить ввод.\n")
        if isContinue == "1":
            break
        if isContinue == "0":
            flag2 = True
            break
        else:
            print("Можно ввести только 1 или 0. Повторите выбор:")
            continue
    if flag2:
        continue

    if int(isContinue):
        break


# Ввод состояний q
while True:
    inputData = input("Введите все состояния q подряд через пробел:")
    strNames = inputData.split()

    # Проверки
    if len(strNames) < 2:
        print("Алфавит содержит менее 2 элементов. Повторите ввод:")
        continue

    flag = False
    for i in strNames:
        if len(i) < 2:
            print("Состояния должны начинаться с q и заканчиваться цифрой. Повторите ввод:")
            flag = True
            break
        elif not i[1].isnumeric():
            print("Состояния должны начинаться с q и заканчиваться цифрой. Повторите ввод:")
            flag = True
            break
        if i[0] != 'q':
            print("Состояния должны начинаться с q и заканчиваться цифрой. Повторите ввод:")
            flag = True
            break
        if strNames.count(i) > 1:
            print("Алфавит содержит повторяющиеся элементы. Повторите Ввод:")
            flag = True
            break
    if flag:
        continue

    flag2 = False
    print(strNames)
    while True:
        isContinue = input("Продолжить с этим алфавитом? Введите 1, чтобы продолжить, или 0, чтобы повторить ввод.\n")
        if isContinue == "1":
            break
        if isContinue == "0":
            flag2 = True
            break
        else:
            print("Можно ввести только 1 или 0. Повторите выбор:")
            continue
    if flag2:
        continue

    if int(isContinue):
        break


# Выбор начальной и конечной вершин
startVertex = []
while True:
    inputDt = input("Укажите какая вершина является начальной:")


    flag = True
    for i in strNames:
        if i == inputDt:
            flag = False
            break
    if flag:
        print("Данной вершины нет в указанном графе. Повторите ввод этой вершины")
        continue
    startVertex.append(inputDt)

    while True:
        choice = input("Закончить ввод начальных вершин? Да - 1, Нет - 0: ")
        if choice == "1":
            break
        if choice == "0":
            flag2 = True
            break
        else:
            print("Можно ввести только 1 или 0. Повторите выбор:")
            continue
    if choice == '1':
        break

endVertex = []
while True:
    inputDt2 = input("Укажите какая вершина является конечной:")

    flag = True
    for i in strNames:
        if i == inputDt2:
            flag = False
            break
    if flag:
        print("Данной вершины нет в указанном графе. Повторите ввод этой вершины")
        continue
    endVertex.append(inputDt2)

    while True:
        choice = input("Закончить ввод конечных вершин? Да - 1, Нет - 0: ")
        if choice == "1":
            break
        if choice == "0":
            flag2 = True
            break
        else:
            print("Можно ввести только 1 или 0. Повторите выбор:")
            continue
    if choice == '1':
        break
startClasses = [startVertex, endVertex]
print(startClasses)

# Создаем массив, который хранит граф
matrix = []
for i in range(len(strNames)):
    matrix.append([0] * len(colNames))


# Заполнение таблицы, которая описывает граф
for (i, a) in zip(strNames, range(len(strNames))):
    for (j, b) in zip(colNames, range(len(colNames))):
        while True:
            currentValue = input("Введите в какое состояние можно пойти из " + i + " по " + j + " (Если это невозможно, укажите 0)(Если для Е нужно написать более 1 элемента, то напишите их через пробел):")
            if ((inputData.find(currentValue) == -1) and (currentValue != '0')) or currentValue == 'q':
                print("Данной вершины нет в графе. Введите корректную вершину:")
                continue
            break
        if j == 'E' or j == 'Е':
            if currentValue == '0':
                matrix[a][b] = ['0']
            else:
                matrix[a][b] = currentValue.split()
        else:
            matrix[a][b] = currentValue
'''
'''
matrix = [['q1', 'q4'],
          ['q4', 'q2'],
          ['q5', 'q3'],
          ['q3', 'q5'],
          ['q4', 'q2'],
          ['q3', 'q5'],
          ['q3', 'q5']]

colNames = ['a', 'b']
strNames = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7']
startClasses = [['q0', 'q1', 'q2', 'q4'], ['q3', 'q5', 'q6']]
'''


def isDeterm(colNames, matrix):
    flag1 = False
    for i in colNames:
        if i == 'E' or i == 'Е':
            flag1 = True
            matrix = determ(strNames, colNames, matrix, startClasses[0], startClasses[1])
    flag2 = False
    for j in matrix:
        if len(j) > len(colNames):
            flag2 = True
            matrix = determ(strNames, colNames, matrix, startClasses[0], startClasses[1])
    if not flag1:
        print("Граф детерминирован")
    elif not flag2:
        print("Граф детерминирован")

def changeData(matrix, colNames, strNames, startClasses):
    elem = set()
    flag = False
    for i in matrix:
        for j in i:
            if set(j).issubset(elem):
                flag = True
            else:
                elem.add(j)

    for i in strNames:
        flag = False
        for j in elem:
            if j == i:
                flag = True
        if not flag:
            strNames.remove(i)
            indx = i[1:]
            indx = int(indx)
            matrix.pop(indx)
            for t in startClasses:
                for c in t:
                    if c == i:
                        t.remove(c)

    res = [[], [], []]
    res[0] = matrix
    res[1] = strNames
    res[2] = startClasses
    return res

def findVal(q, val, matrix, strNames, colNames):
    strindx = strNames.index(q)
    colIndx = colNames.index(val)

    return matrix[strindx][colIndx]


def findClasses(startClasses, matrix, strNames, colNames):
    resClass = []
    counter = 0
    temp = set()
    temp2 = set()
    for a in startClasses:
        if len(a) == 1:
            resClass.append([])
            resClass[-1].append(a[0])
            continue
        counter2 = 0
        counter += 1
        temps = 0
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
                        temp.add(i)
                        flag3 = True
                else:
                    temp2.add(i)
            newA = set(a)
            if temp == newA:
                temps += 1
                temp = set()
            else:
                if len(temp) > 0:
                    resClass.append([])
                    for k in temp:
                        resClass[-1].append(k)
                resClass.append([])
                for k in temp2:
                    resClass[-1].append(k)
                temp = set()
                temp2 = set()
        if temps == len(colNames):
            resClass.append([])
            for i in a:
                resClass[-1].append(i)

    for v in range(len(resClass)):
        for b in range(v + 1, len(resClass)-1):
            set1 = set(resClass[v])
            set2 = set(resClass[b])
            if set1 == set2:
                resClass.pop(b)

    return resClass



def buildGraph(matrix, resClasses, strNames, colNames):
    resMatrix = []
    for i in range(len(resClasses)):
        resMatrix.append([0]*len(matrix[0]))
    for j in colNames:
        for i in resClasses:
            if len(i) == 1:
                res = findVal(i[0], j, matrix, strNames, colNames)
                for t in resClasses:
                    for k in t:
                        if res == k:
                            res = t[0]
                strIndx = resClasses.index(i)
                colIndx = colNames.index(j)
                resMatrix[strIndx][colIndx] = res
            else:
                res = findVal(i[0], j, matrix, strNames, colNames)
                flag = False
                for t in resClasses:
                    for k in t:
                        if res == k:
                            res = t[0]
                            break
                    if flag:
                        break
                strIndx = resClasses.index(i)
                colIndx = colNames.index(j)
                resMatrix[strIndx][colIndx] = res
    return resMatrix



isDeterm(colNames, matrix)

res = changeData(matrix, colNames, strNames, startClasses)
matrix = res[0]
strNames = res[1]
startClasses = res[2]


print("Класс эквивалентности 1:", startClasses)
print("Класс эквивалентности 2:", findClasses(startClasses, matrix, strNames, colNames))
resClasses = findClasses(startClasses, matrix, strNames, colNames)
print("Класс эквивалентности 3:", findClasses(resClasses, matrix, strNames, colNames))
resClasses2 = findClasses(resClasses, matrix, strNames, colNames)
print("Минимизированный граф:")
table = buildGraph(matrix, resClasses2, strNames, colNames)

# Вывод таблицы графа
mytable = PrettyTable()
columns = colNames.copy()
columns.insert(0, "Состояние")
mytable.field_names = columns
for i in range(len(resClasses) + 1):
    strName = strNames[i]
    string = table[i].copy()
    string.insert(0, strName)
    mytable.add_row(string)
print(mytable)
