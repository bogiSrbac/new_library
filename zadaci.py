


def reverse_integer(number):
    to_string = str(number)
    to_string = list(to_string)
    to_reverse_list = []
    print(len(to_string))
    for i in range(len(to_string) - 1, -1, -1):
        print(i)
        to_reverse_list.append(to_string[i])
    reversed_integer = ''.join(to_reverse_list)
    reversed_integer = int(reversed_integer)
    return reversed_integer


# provjeri da li je amstrongov broj

def amstrong_number(number):
    to_string = str(number)
    to_string = list(to_string)
    list_of_numbers = []
    for i in to_string:
        list_of_numbers.append(int(i))
    list_of_cubes = []
    for j in list_of_numbers:
        cubes = j ** 5
        list_of_cubes.append(cubes)
    sum_of_integers = 0
    for k in list_of_cubes:
        sum_of_integers = sum_of_integers + k
    print(list_of_cubes)
    if number == sum_of_integers:
        print(f'Number {number} is Amstrongs number!')
    else:
        print(f'Number {number} is not Amstrongs number!')


# if number is prime number
def prime_numbers():
    list_of_primes = []
    help_list = []
    for i in range(2, 1000):
        for j in range(2, i + 1):
            num = i % j
            if num == 0:
                help_list.append(i)
        if len(help_list) <= 1:
            list_of_primes.append(help_list[0])
        help_list = []
    print(list_of_primes)


# fibonacci iteration method

def print_fibonacci_iterate(number):
    list_of_fibonacci = [0, 1]
    print(list_of_fibonacci[-2])
    for i in range(1, number):
        next_fib = list_of_fibonacci[-2] + list_of_fibonacci[-1]
        list_of_fibonacci.append(next_fib)
    print(list_of_fibonacci)


# fibonacci recursive

# def recur_fibo(n):
#    if n <= 1:
#        return n
#    else:
#        return(recur_fibo(n-1) + recur_fibo(n-2))
#
# nterms = 10
#
# # check if the number of terms is valid
# if nterms <= 0:
#    print("Plese enter a positive integer")
# else:
#    print("Fibonacci sequence:")
#    for i in range(nterms):
#        print(recur_fibo(i))


# find max number

def find_max(x, y, z):
    max_list = [x, y, z]
    max = 0
    for i in max_list:
        if i > max:
            max = i
    return max


# check if number is binary
binary_num = '01070110000'


def checkBinary(number):
    for i in number:
        if i not in '01':
            print(i)
            return f'Number {number} is not bynary'
    return f'Number {number} is bynary'


# sum using recursive

def sum_of_digit(n):
    if n < 10:
        return n
    print(n % 10, 'm')
    print(sum_of_digit(n // 10), 'fun')
    return n % 10 + sum_of_digit(n // 10)


# swap two numbers

def swap_two_numbers(x, y):
    print(f'x = {x} , y = {y}')
    x = x - y
    y = y + x
    x = y - x

    print(f'x = {x} , y = {y}')


# swap_two_numbers with third var

def swap_two_third(x, y):
    print(f'x = {x} , y = {y}')
    c = y
    y = x
    x = c
    print(f'x = {x} , y = {y}')


# add two integers without operat
def Add(x, y):
    while (y != 0):
        carry = x & y
        print(carry, 'carry')
        x = x ^ y
        print(x, 'x')

        y = carry << 1
        print(y, 'y')
    return x


# check if number is perfect number

def perfect_number(x):
    all_numbers = []
    for i in range(1, x):
        if x % i == 0:
            all_numbers.append(i)
    if sum(all_numbers) == x:
        print(f'{x} is perfect number')
    else:
        print(f'{x} is not perfect number')


# factorial iteration
def fact_itera(x):
    number = 1
    for i in range(1, x + 1):
        number = number * i
    return number


# fact recursion

def fact_recurs(x):
    if x == 1:
        print(x)
        return x
    else:
        print(x)
        return x * fact_recurs(x - 1)


# check is number even or odd
def even_or_odd(x):
    if x % 2 == 0:
        return f'Number {x} is even!'
    else:
        return f'Number {x} is odd!'


# find smallest number within three numbers
from random import randint

listOfNumbers = [47, 45, 78]


# for i in range(1000):
#     num = randint(1, 100000)
#     if num not in listOfNumbers:
#         listOfNumbers.append(num)
# print(listOfNumbers)
# print(len(listOfNumbers))

def find_min(list_of_number=[]):
    min = list_of_number[0]
    for i in list_of_number:
        if i < min:
            min = i
    return min


# power in for loop

def power(x, y):
    pow = x
    for i in range(1, y):
        x = x * pow
    return x


# power with while loop

def pow_while(x, y):
    counter = 0
    num = x
    while counter != y:
        x = x * num
        counter = counter + 1
    return x


# find LCM

def lcm(x, y, z):
    listOfX = []
    listOfY = []
    for i in range(1, z):
        modulo1 = i % x
        modulo2 = i % y
        if modulo1 == 0:
            listOfX.append(i)
        if modulo2 == 0:
            listOfY.append(i)
    for i in listOfX:
        if i in listOfY:
            return i
    return f'There is no LCM for numbers {x} {y}'


# GCD

def gcd(x, y):
    minimum = min(x, y)
    listX = []
    listy = []
    for i in range(1, minimum):
        modulo1 = x % i
        modulo2 = y % i
        if modulo1 == 0:
            listX.append(i)
        if modulo2 == 0:
            listy.append(i)
    listOfGCD = []
    for j in listX:
        if j in listy:
            listOfGCD.append(j)
    listOfGCD.sort()
    print(listOfGCD)
    if listOfGCD[-1]:
        gcdNum = listOfGCD[-1]
        return gcdNum
    else:
        return 'No GCD for this numbers'


# replace char in string

def char_replace(string, char):
    name = string.replace(char, '')
    return name


# count occurrence of char in string

def count_occurrence(string, char):
    count = 0
    for i in string:
        if i == char:
            count = count + 1
    return count


def anagram(first, second):
    firstList = {}
    secondList = {}
    for i in first:
        if i in firstList:
            firstList[i] = firstList[i] + 1
        else:
            firstList[i] = 1
    for i in second:
        if i in secondList:
            secondList[i] = secondList[i] + 1
        else:
            secondList[i] = 1

    if firstList == secondList:
        return 'Is anagram'
    else:
        return 'Is not anagram'


# palindrom

def palindrom(word):
    L = list(word)
    K = []
    wordLenght = len(L)
    for i in range(wordLenght):
        K.append(L[-1])
        L.pop(-1)
    wordToCheck = ''.join(K)
    if word == wordToCheck:
        return 'Word is palindrom'
    else:
        return 'Word is not palindrom'

# vowel or consonant

def vowel(char):
    if char in 'aoieu':
        return 'Char is vowel'
    else:
        return 'Char is consonant'

# id digit
def checkIfDigit():
    ch = input("Enter a character : ")
    if ch >= '0' and ch <= '9': #comparing the value of ‘ch’
        print("Given Character ", ch, "is a Digit")
    else:
        print("Given Character ", ch, "is not a Digit")

# is digit with method isDigit()

def isDigitFunc(x):
    if x.isdigit():
        return 'String is digit'
    else:
        return 'String is not digit'

# replace space with char

def setCharInSpace(char, word):
    result = ''
    for i in word:
        if i == " ":
            i = char
        result += i
    return result


def setCharInSpaceReplace(char, word):
    x = word.replace(" ", char)
    return x

# vowel to uppercase
def voewlToUppercase(word):
    vowels = 'AOEIU'
    vowelsLower = 'aoeiu'
    result = ''
    for i in word:
        if i in vowelsLower:
            ind = vowelsLower.find(i)
            i = vowels[ind]
        result += i
    return result

# delete volwe from string

def deleteVolwe(word):
    result = ''
    vowels = 'AOEIU'
    vowelsLower = 'aoeiu'
    for i in word:
        if i not in vowels:
            if i not in vowelsLower:
                result += i

    return result

# count volwes and consonants

def countChar(word):
    countVolwes = 0
    countConsonants = 0
    vowelsLower = 'aoeiuAOEIU'
    for i in word:
        if i in vowelsLower:
            countVolwes += 1
        elif i == " ":
            pass
        else:
            countConsonants += 1

    return f'Volwes: {countVolwes}, Consonants: {countConsonants}'

# count most frequent char

def countCharFrequency(word):
    freq = {}
    for i in word:
        if i in freq and i != ' ':
            freq[i] = freq[i] + 1
        else:
            if i != ' ':
                freq[i] = 1

    max = 0
    key = ''
    mostFreq = {}
    for i in freq:
        if freq[i] > max:
            max = freq[i]
            key = i
    mostFreq[key] = max
    return mostFreq, freq

# find missing integer
def findMissingInteger():
    arr = []
    n = int(input("enter size of array : "))
    for x in range(n-1):
        x=int(input("enter element of array : "))
        arr.append(x)
    sum = (n*(n+1))/2
    sumArr = 0
    for i in range(n-1):
        sumArr = sumArr+arr[i]
    print(int(sum-sumArr))


# find repeated integers
def countRepeated():
    arr, occur = [], []
    n = int(input("please enter the size of array: "))
    for x in range(n):
        occur.append(0)
    for x in range(n):
        element = int(input(f"please enter the element of array element between 0 to {n-1} :"))
        arr.append(element)
        occur[arr[x]]=occur[arr[x]]+1
        print(x)
        print(arr)
        print(arr[x])
    print(arr)
    print(occur)
    for x in range(n):
        if occur[x]>1:
            print(f"{x} is repeated {occur[x]} times")

# find sum of pairs equal to given number

def findPairs(num, list=[]):
    listOfpairs = []
    for i in list:
        for j in list:
            sumOfNumbers = j + i
            if j==i:
                pass
            elif sumOfNumbers == num:
                tup = (i, j)
                listOfpairs.append(tup)
    return listOfpairs

L = [11, 2, 4, 8, 6, 3, 15]
numX = 12

# find max and min in array

def findMaxMin(lista=[]):
    max = 0
    min = lista[0]
    for i in lista:
        if i > max:
            max = i
        elif i < min:
            min = i
    return f'Highest number in list is {max}, and lowest is {min} '

K = [158, 60, 100, 1000, 99, 82, 36, 2900, 47, 51]

# secon largest in array

def secondLarg(lista=[]):
    x = []
    duzina = len(lista)
    lenOfX = 0
    p = 0
    while lenOfX < duzina:
        min = lista[0]
        for i in lista:
            if i < min:
                min = i
        x.append(min)
        p = lista.index(min)
        lista.pop(p)
        lenOfX = len(x)
    return x[-2]

# remove duplicates

def removeDuplicates(lista=[]):
    newList = []
    listOfIndex = []
    count = 0
    for i in lista:
        if i not in newList:
            print(i)
            newList.append(i)
        elif i in newList:
            listOfIndex.append(count)
        count += 1
    count2 = 0
    for j in listOfIndex:
        lista.pop(j-count2)
        count2 += 1
    print(listOfIndex)


    return lista

T = [25, 14, 3, 25, 18, 7, 68, 18, 18, 69, 25, 77, 7]

# reverse list
def reverseList(lista=[]):
    newList = []
    lastIndex = -1
    for i in range(len(lista)):
        newList.append(lista[lastIndex])
        lastIndex -= 1
    return newList

def swap_case(s):
    result = ''
    for i in s:
        if i.isupper():
            result = result + i.lower()
        else:
            result = result + i.upper()

    return result

def split_and_join(line):
    result = line.split(" ")
    result = "-".join(result)
    return result


prod = ['narandze', 'jabuke', 'sljive', 'breskve']
pPrice = [25.00, 35.23, 15.25, 39.21]
pSold = ['narandze', 'narandze', 'jabuke', 'breskve']
sPrice = [25.00, 25.32, 35.23, 35.23]
def priceCheck(products, productPrices, productSold, soldPrice):
    dictOfGoods = {}
    counter = 0
    for i in products:
        dictOfGoods[i] = productPrices[counter]
        counter += 1
    result = 0
    for item in range(len(productSold)):
        chekcItem = dictOfGoods[productSold[item]]
        checkPrice = soldPrice[item]
        if chekcItem != checkPrice:
            result += 1
    return result

rt = [1, 14, 5, 7, 9, 3]

def minimizeBias(ratings):
    lista = sorted(ratings)
    lista.reverse()
    minimumB = 0
    for i in range(0, len(lista), 2):
        num1 = lista[i] - lista[i+1]
        minimumB = minimumB + num1
    return minimumB

def getUsernames(threshold):
    import urllib.request
    import json
    listOfUsers = []
    listOf10Users = []
    for i in range(1, 3):
        url = f'https://jsonmock.hackerrank.com/api/article_users?page={i}'
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode('utf8'))
            print(data)
            for i in range(len(data['data'])):
                if data['data'][i]['submission_count'] > threshold:
                    listOfUsers.append(data['data'][i]['username'])
    if threshold > 9:
        for i in range(10):
            listOf10Users.append(listOfUsers[i])
        return listOf10Users
    else:
        return listOfUsers, 'kkdkkd'




def countMax(upRight):
    listOfCordinates = []
    for i in upRight:
        P = []
        word = ''
        for j in i:
            print(j)
            if j.isdigit():
                word = word + j

            elif j == ' ':

                P.append(int(word))
                word = ""
            print(P)
        tup = tuple(P)
        listOfCordinates.append(tup)
    r = 0
    c = 0
    print(listOfCordinates)

    for i in range(len(listOfCordinates)):
        if listOfCordinates[i][0] > r:
            r = listOfCordinates[i][0]
        if listOfCordinates[i][1] > c:
            c = listOfCordinates[i][1]
    print(r, c)
    twoD_array = [[0 for i in range(c)] for j in range(r)]

    for i in range(len(listOfCordinates)):
        rows = listOfCordinates[i][0]
        columns = listOfCordinates[i][1]
        for row in range(len(twoD_array)):
            for col in range(len(twoD_array[row])):
                if row > r - rows - 1 and col < columns:
                    twoD_array[row][col] += 1

    max = 0
    for row in range(len(twoD_array)):
        for col in range(len(twoD_array[row])):
            if twoD_array[row][col] > max:
                max = twoD_array[row][col]

    counter = 0
    for row in range(len(twoD_array)):
        for col in range(len(twoD_array[row])):
            if twoD_array[row][col] == max:
                counter += 1

    # return counter


    for r in twoD_array:
        for c in r:
            print(c, end=" ")
        print()
Y = ['234 458', '124 214', '111 259', '457 368', '368 147']
countMax(Y)









