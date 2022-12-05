"""Calculator"""

def rpn(s):
    lex = parse(s)
    s2 = []
    r = []
    oper = ["+", "-", "*", "/", "(", ")", "^", ">"]
    for elem in lex:
        if elem == "(":
            s2 = [elem] + s2
        elif elem in oper:
            if s2 == []:
                s2 = [elem]
            elif elem == ")":
                while (True):
                    q = s2[0]
                    s2 = s2[1:]
                    if q == "(":
                        break
                    r += [q]
            elif priority(s2[0]) < priority(elem):
                s2 = [elem] + s2
            else:
                while (True):
                    if s2 == []:
                        break
                    q = s2[0]
                    r += [q]
                    s2 = s2[1:]
                    if priority(q) == priority(elem):
                        break
                s2 = [elem] + s2
        else:
            r += [elem]
    while (s2 != []):
        q = s2[0]
        r += [q]
        s2 = s2[1:]
    return r

def priority(oper):
    if oper == "+" or oper == "-":
        return 1
    elif oper == "*" or oper == "/":
        return 2
    elif oper == "^" or oper == ">":
        return 3
    elif oper == "(":
        return 0

def translate(num, base):
    num_ver = num
    inc = 1
    result = 0
    while num_ver > 0:
        result += num_ver % base * inc
        inc *= 10
        num_ver //= base
    return result

def convert(num):
    """Перевод из string в целое, вещественное число"""
    if num.count(".") == 1:
        return float(num)
    return int(num)

def parse(s):
    delims = ["+", "-", "*", "/", "(", ")", "^", ">"]
    lex = []
    tmp = ""
    for elem in s:
        if elem != " ":
            if elem in delims:
                if tmp != "":
                    lex += [tmp]
                lex += [elem]
                tmp = ""
            else:
                tmp += elem
    if tmp != "":
        lex += [tmp]
    return lex


def rpn_calc(formula):
    res = []
    for lex in formula:
        if lex[0].isdigit():
            res.append(convert(lex))
        else:
            num2 = res.pop()
            num1 = res.pop()
            if lex == '+':
                res.append(num1 + num2)
            if lex == '-':
                res.append(num1 - num2)
            if lex == '*':
                res.append(num1 * num2)
            if lex == '/':
                if num2 == 0:
                    return "На ноль делить нельзя!"
                res.append(num1 / num2)
            if lex == "^":
                res.append(num1 ** num2)
            if lex == ">":
                if num2 > 9:
                    return "Некорректный ввод! Чисо не должно быть отрицательным и снование не должно превышать 9!"
                res.append(translate(num1, num2))
    return res.pop()

print(rpn_calc(rpn(input())))
#print(eval("2/0"))
